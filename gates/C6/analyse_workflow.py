#!/usr/bin/env python3
"""C6 revision-eligibility gate analysis.

CPU-only, Python 3 standard library only. Reads the real 4-agent RAG workflow
traces (taskA_e0.jsonl) and computes the pre-registered statistics from
protocol.md: artifact/edge counts, repeated-consumer coverage, incidence
density, used-region statistics (substring + 3-gram Jaccard robustness),
sentence-level mutation simulation (exact-replay vs query-relative), and
from-scratch oracle availability. Writes results.json next to this script.
"""

import json
import os
import random
import re
import statistics
from collections import Counter, defaultdict

TRACE_PATH = "/Users/zijian_nong/research/aaai2027/runs/traces/taskA_e0.jsonl"
OUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results.json")

SEED = 20260721
MAX_MUT_POSITIONS = 8
MIN_SENT_WORDS = 8
JACCARD_THRESHOLD = 0.5

PRODUCER = {
    "sys": "framework",
    "cite": "retriever",
    "doc": "retriever",
    "plan": "reader",
    "evid": "verifier",
    "verify": "writer",
}
MUTATION_CLASSES = ("doc", "cite")
N_AGENTS = 4


def block_class(block_id):
    return block_id.split("-", 1)[0]


def normalize(text):
    """Lowercase, map non-alphanumeric runs to a single space, strip."""
    return re.sub(r" +", " ", re.sub(r"[^a-z0-9]+", " ", text.lower())).strip()


_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+|[\r\n]+")


def split_sentences(text):
    return [s.strip() for s in _SENT_SPLIT.split(text) if s.strip()]


def word_count(normalized_sentence):
    return len(normalized_sentence.split())


def ngrams(tokens, n=3):
    if not tokens:
        return set()
    if len(tokens) < n:
        return {tuple(tokens)}
    return {tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1)}


def mutation_positions(n_sentences, rng):
    """Up to MAX_MUT_POSITIONS sentence indices; uniform sample beyond that.

    Deterministic given a fixed-seed rng and a fixed call order.
    """
    if n_sentences <= MAX_MUT_POSITIONS:
        return list(range(n_sentences))
    return sorted(rng.sample(range(n_sentences), MAX_MUT_POSITIONS))


def percentile(sorted_vals, p):
    if not sorted_vals:
        return None
    k = (len(sorted_vals) - 1) * p
    lo = int(k)
    hi = min(lo + 1, len(sorted_vals) - 1)
    frac = k - lo
    return sorted_vals[lo] + (sorted_vals[hi] - sorted_vals[lo]) * frac


class ConsumerUsage:
    """Used-region measurement for one consumer's output."""

    def __init__(self, output_text):
        self.norm_output = normalize(output_text)
        out_sents = split_sentences(output_text)
        self.out_ngram_sets = [ngrams(normalize(s).split()) for s in out_sents]
        self.out_ngram_sets = [g for g in self.out_ngram_sets if g]

    def used_substring(self, norm_sentence):
        return norm_sentence in self.norm_output

    def used_jaccard(self, sent_ngrams):
        if not sent_ngrams or not self.out_ngram_sets:
            return False
        best = 0.0
        for out_set in self.out_ngram_sets:
            inter = len(sent_ngrams & out_set)
            if not inter:
                continue
            union = len(sent_ngrams | out_set)
            best = max(best, inter / union)
            if best >= JACCARD_THRESHOLD:
                return True
        return best >= JACCARD_THRESHOLD


def analyse():
    rng = random.Random(SEED)

    n_traces = 0
    oracle_present = 0

    node_counts = Counter()          # class -> total artifact nodes
    edge_counts = Counter()          # class -> total consumer edges (incl. sys)
    per_trace_nodes = []
    per_trace_edges = []
    consumers_per_artifact = Counter()  # class -> summed consumer counts
    artifact_instances = Counter()      # class -> number of artifacts
    text_mismatches = 0

    # Used-region distributions per population of (artifact, consumer) pairs.
    used_ratio = {"substring": defaultdict(list), "jaccard": defaultdict(list)}
    unused_pairs = {"substring": Counter(), "jaccard": Counter()}
    total_pairs = Counter()
    skipped_no_measurable = 0

    # Mutation simulation aggregates.
    mut = {
        variant: {
            "n_mutations": 0,
            "exact_count": 0,
            "qr_count": 0,
            "exact_cost": 0,
            "qr_cost": 0,
            "dead": 0,
            "dead_measurable": 0,
            "n_measurable_positions": 0,
            "per_class": defaultdict(lambda: {
                "n_mutations": 0, "exact_count": 0, "qr_count": 0,
                "exact_cost": 0, "qr_cost": 0, "dead": 0,
            }),
        }
        for variant in ("substring", "jaccard")
    }

    with open(TRACE_PATH) as fh:
        for line in fh:
            trace = json.loads(line)
            n_traces += 1
            if trace.get("full_recompute_answer"):
                oracle_present += 1

            agents = trace["agents"]
            usage = {a["agent_id"]: ConsumerUsage(a["output_text"]) for a in agents}
            out_len = {a["agent_id"]: a["output_len"] for a in agents}

            # artifact text + consumers, in first-seen block order
            art_text = {}
            art_consumers = defaultdict(list)
            for a in agents:
                for b in a["blocks"]:
                    bid = b["block_id"]
                    if bid in art_text:
                        if art_text[bid] != b["text"]:
                            text_mismatches += 1
                    else:
                        art_text[bid] = b["text"]
                    art_consumers[bid].append(a["agent_id"])

            trace_nodes = Counter()
            trace_edges = 0
            for bid, consumers in art_consumers.items():
                cls = block_class(bid)
                trace_nodes[cls] += 1
                node_counts[cls] += 1
                artifact_instances[cls] += 1
                consumers_per_artifact[cls] += len(consumers)
                trace_edges += len(consumers)
                edge_counts[cls] += len(consumers)
            per_trace_nodes.append(dict(trace_nodes))
            per_trace_edges.append(trace_edges)

            # Used-region measurement + mutation simulation
            for bid, text in art_text.items():
                cls = block_class(bid)
                if cls == "sys":
                    continue
                consumers = art_consumers[bid]
                sentences = split_sentences(text)
                norm_sents = [normalize(s) for s in sentences]
                measurable = [word_count(ns) >= MIN_SENT_WORDS for ns in norm_sents]
                sent_ngrams = [ngrams(ns.split()) for ns in norm_sents]

                # used[variant][consumer] = set of used sentence indices
                used = {variant: {} for variant in ("substring", "jaccard")}
                for cid in consumers:
                    u = usage[cid]
                    for variant in ("substring", "jaccard"):
                        idxs = set()
                        for i, ns in enumerate(norm_sents):
                            if not measurable[i]:
                                continue
                            hit = (u.used_substring(ns) if variant == "substring"
                                   else u.used_jaccard(sent_ngrams[i]))
                            if hit:
                                idxs.add(i)
                        used[variant][cid] = idxs

                    n_meas = sum(measurable)
                    if n_meas == 0:
                        skipped_no_measurable += 1
                        continue
                    for variant in ("substring", "jaccard"):
                        ratio = len(used[variant][cid]) / n_meas
                        pop = "mutation_classes" if cls in MUTATION_CLASSES else "other"
                        used_ratio[variant][pop].append(ratio)
                        used_ratio[variant]["all"].append(ratio)
                        total_pairs[pop] += 1 if variant == "substring" else 0
                        if not used[variant][cid]:
                            unused_pairs[variant][pop] += 1

                # Mutation simulation on doc/cite artifacts
                if cls not in MUTATION_CLASSES:
                    continue
                positions = mutation_positions(len(sentences), rng)
                for pos in positions:
                    for variant in ("substring", "jaccard"):
                        m = mut[variant]
                        m["n_mutations"] += 1
                        mc = m["per_class"][cls]
                        mc["n_mutations"] += 1
                        exact_c = list(consumers)
                        qr_c = [cid for cid in consumers if pos in used[variant][cid]]
                        m["exact_count"] += len(exact_c)
                        m["qr_count"] += len(qr_c)
                        m["exact_cost"] += sum(out_len[c] for c in exact_c)
                        m["qr_cost"] += sum(out_len[c] for c in qr_c)
                        mc["exact_count"] += len(exact_c)
                        mc["qr_count"] += len(qr_c)
                        mc["exact_cost"] += sum(out_len[c] for c in exact_c)
                        mc["qr_cost"] += sum(out_len[c] for c in qr_c)
                        if not qr_c:
                            m["dead"] += 1
                            mc["dead"] += 1
                        if measurable[pos]:
                            m["n_measurable_positions"] += 1
                            if not qr_c:
                                m["dead_measurable"] += 1

    # ---- aggregate ----
    non_sys_nodes = sum(v for k, v in node_counts.items() if k != "sys")
    non_sys_edges = sum(v for k, v in edge_counts.items() if k != "sys")
    density = non_sys_edges / (N_AGENTS * non_sys_nodes) if non_sys_nodes else 0.0

    results = {
        "meta": {
            "trace_path": TRACE_PATH,
            "seed": SEED,
            "max_mutation_positions": MAX_MUT_POSITIONS,
            "min_sentence_words": MIN_SENT_WORDS,
            "jaccard_threshold": JACCARD_THRESHOLD,
            "n_traces": n_traces,
        },
        "nodes": {
            "by_class": dict(node_counts),
            "non_sys_total": non_sys_nodes,
            "per_trace_mean": {k: v / n_traces for k, v in node_counts.items()},
        },
        "edges": {
            "by_class": dict(edge_counts),
            "non_sys_total": non_sys_edges,
            "per_trace_mean": sum(per_trace_edges) / n_traces,
        },
        "repeated_consumer_coverage": None,  # filled below
        "incidence_density": density,
        "used_region": {},
        "mutation": {},
        "oracle": {
            "present": oracle_present,
            "rate": oracle_present / n_traces,
        },
        "data_quality": {
            "block_text_mismatches_within_trace": text_mismatches,
            "pairs_skipped_no_measurable_sentence": skipped_no_measurable,
        },
    }

    # repeated-consumer coverage (exact per-artifact pass is folded into the
    # main loop via consumers_per_artifact; here we divide correctly)
    repeated = 0
    non_sys_artifacts_total = 0
    for cls in artifact_instances:
        if cls == "sys":
            continue
        non_sys_artifacts_total += artifact_instances[cls]
        # consumers_per_artifact[cls] counts total edges of the class; each
        # artifact of this class may have different consumer counts, so we
        # stored per-artifact counts implicitly — recompute from scratch below.
    results["repeated_consumer_coverage"] = repeated_consumer_coverage(TRACE_PATH)
    cov = results["repeated_consumer_coverage"]

    for variant in ("substring", "jaccard"):
        ur = {}
        for pop in ("mutation_classes", "other", "all"):
            vals = sorted(used_ratio[variant][pop])
            if not vals:
                continue
            ur[pop] = {
                "n_pairs": len(vals),
                "median": percentile(vals, 0.5),
                "p90": percentile(vals, 0.9),
                "frac_zero_use": sum(1 for v in vals if v == 0) / len(vals),
            }
        results["used_region"][variant] = ur

        m = mut[variant]
        n_mut = m["n_mutations"]
        entry = {
            "n_mutations": n_mut,
            "exact_total_invalidations": m["exact_count"],
            "qr_total_invalidations": m["qr_count"],
            "exact_mean_per_mutation": m["exact_count"] / n_mut,
            "qr_mean_per_mutation": m["qr_count"] / n_mut,
            "exact_total_cost": m["exact_cost"],
            "qr_total_cost": m["qr_cost"],
            "exact_mean_cost_per_mutation": m["exact_cost"] / n_mut,
            "qr_mean_cost_per_mutation": m["qr_cost"] / n_mut,
            "count_reduction": (m["exact_count"] - m["qr_count"]) / m["exact_count"]
                               if m["exact_count"] else None,
            "cost_reduction": (m["exact_cost"] - m["qr_cost"]) / m["exact_cost"]
                              if m["exact_cost"] else None,
            "dead_region_freq": m["dead"] / n_mut,
            "dead_region_freq_measurable_only": (
                m["dead_measurable"] / m["n_measurable_positions"]
                if m["n_measurable_positions"] else None
            ),
            "n_measurable_positions": m["n_measurable_positions"],
            "per_class": {
                cls: {
                    "n_mutations": mc["n_mutations"],
                    "exact_mean_per_mutation": mc["exact_count"] / mc["n_mutations"],
                    "qr_mean_per_mutation": mc["qr_count"] / mc["n_mutations"],
                    "cost_reduction": (
                        (mc["exact_cost"] - mc["qr_cost"]) / mc["exact_cost"]
                        if mc["exact_cost"] else None
                    ),
                    "dead_region_freq": mc["dead"] / mc["n_mutations"],
                }
                for cls, mc in m["per_class"].items()
            },
        }
        results["mutation"][variant] = entry

    # pre-registered criteria
    primary = results["mutation"]["substring"]
    med = results["used_region"]["substring"]["mutation_classes"]["median"]
    results["criteria"] = {
        "a_coverage_ge_0.30": {
            "value": cov["non_sys"],
            "pass": cov["non_sys"] >= 0.30,
        },
        "b_cost_reduction_ge_0.20": {
            "value": primary["cost_reduction"],
            "pass": primary["cost_reduction"] is not None
                    and primary["cost_reduction"] >= 0.20,
        },
        "c_oracle_ge_0.95": {
            "value": results["oracle"]["rate"],
            "pass": results["oracle"]["rate"] >= 0.95,
        },
        "d_used_region_nondegenerate": {
            "value": med,
            "pass": med is not None and 0.0 < med < 1.0,
        },
    }
    allpass = all(c["pass"] for c in results["criteria"].values())
    results["criteria"]["overall"] = "GO" if allpass else (
        "FAIL_MEASUREMENT" if not results["criteria"]["d_used_region_nondegenerate"]["pass"]
        else "NO_GO"
    )

    with open(OUT_PATH, "w") as fh:
        json.dump(results, fh, indent=2)
    return results


def repeated_consumer_coverage(trace_path):
    """Fraction of non-sys artifacts consumed by >= 2 consumers (exact pass)."""
    ge2 = 0
    total = 0
    per_class_ge2 = Counter()
    per_class_total = Counter()
    with open(trace_path) as fh:
        for line in fh:
            trace = json.loads(line)
            consumers = defaultdict(set)
            for a in trace["agents"]:
                for b in a["blocks"]:
                    consumers[b["block_id"]].add(a["agent_id"])
            for bid, cset in consumers.items():
                cls = block_class(bid)
                if cls == "sys":
                    continue
                total += 1
                per_class_total[cls] += 1
                if len(cset) >= 2:
                    ge2 += 1
                    per_class_ge2[cls] += 1
    return {
        "non_sys": ge2 / total if total else None,
        "n_ge2": ge2,
        "n_total": total,
        "by_class": {
            cls: per_class_ge2[cls] / per_class_total[cls]
            for cls in per_class_total
        },
    }


if __name__ == "__main__":
    res = analyse()
    print(json.dumps(res["criteria"], indent=2))
    print("mutation (substring):", json.dumps({
        k: v for k, v in res["mutation"]["substring"].items() if k != "per_class"
    }, indent=2))
