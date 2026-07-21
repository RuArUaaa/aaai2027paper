#!/usr/bin/env python3
"""C6 gate — doc-granularity query-relative analysis (citation channel).

Chair-written extension after the sentence-level verbatim measure was found
degenerate (see results.json: sentence_level). Usage here = the workflow's own
citation addressing scheme ("refer to it by its title in parentheses"), not a
post-hoc text heuristic.
"""
import json, random, re
from collections import defaultdict

TRACE = "/Users/zijian_nong/research/aaai2027/runs/traces/taskA_e0.jsonl"
PAIRS = "/Users/zijian_nong/research/aaai2027/runs/pairs/taskA_e0_identity_ctrl.jsonl"
OUT = "/Users/zijian_nong/research/aaai2027-new/gates/C6/results_doc_level.json"
SEED = 20260721
TITLE_RE = re.compile(r"^Document \(([^)]+)\):")

CONSUMERS = ("reader", "verifier", "writer")  # retriever = producer


def load_traces():
    with open(TRACE) as f:
        return [json.loads(l) for l in f if l.strip()]


def doc_titles(agent_blocks):
    """block_id -> title for doc-* blocks."""
    out = {}
    for b in agent_blocks:
        if b["block_id"].startswith("doc-"):
            m = TITLE_RE.match(b["text"].strip())
            out[b["block_id"]] = m.group(1) if m else None
    return out


def analyse():
    traces = load_traces()
    rng = random.Random(SEED)

    n_traces = 0
    total_docs = 0
    edges = 0                      # doc included in consumer context
    used_edges = 0                 # doc cited by consumer
    docs_used_ge2 = 0              # cited by >=2 consumers
    docs_used_ge1 = 0
    docs_used_0 = 0                # dead docs
    per_consumer_use = defaultdict(list)   # consumer -> [#docs cited per trace]

    exact_inv = 0                  # invalidations under identity replay
    qr_inv = 0                     # invalidations under doc-level query-relative
    exact_cost = 0
    qr_cost = 0
    n_mut = 0

    title_missing = 0

    for tr in traces:
        n_traces += 1
        agents = {a["agent_id"]: a for a in tr["agents"]}
        if not all(c in agents for c in CONSUMERS + ("retriever",)):
            continue
        titles = doc_titles(agents["retriever"]["blocks"])
        # verify doc blocks identical across agents (same ids)
        for bid, t in titles.items():
            if t is None:
                title_missing += 1
        # usage map: doc -> set(consumer) via citation
        usage = {bid: set() for bid in titles}
        for c in CONSUMERS:
            out = agents[c]["output_text"]
            n_used = 0
            for bid, t in titles.items():
                edges += 1
                if t and f"({t})" in out:
                    usage[bid].add(c)
                    used_edges += 1
                    n_used += 1
            per_consumer_use[c].append(n_used)
        total_docs += len(titles)
        for bid, users in usage.items():
            if len(users) >= 2:
                docs_used_ge2 += 1
            if len(users) >= 1:
                docs_used_ge1 += 1
            else:
                docs_used_0 += 1
        # mutation sim: mutate each doc entirely (content/field change)
        for bid in titles:
            n_mut += 1
            for c in CONSUMERS:
                cost = agents[c]["output_len"]
                exact_inv += 1
                exact_cost += cost
                if c in usage[bid]:
                    qr_inv += 1
                    qr_cost += cost

    res = {
        "meta": {"trace_path": TRACE, "seed": SEED, "n_traces": n_traces,
                 "usage_semantics": "citation channel: '(Title)' appears in consumer output_text (the workflow's own addressing rule)"},
        "artifacts": {
            "doc_total": total_docs,
            "per_trace_mean": total_docs / n_traces,
        },
        "incidence": {
            "doc_consumer_edges": edges,
            "doc_cited_edges": used_edges,
            "citation_rate": used_edges / edges,
        },
        "usage_per_consumer_per_trace": {
            c: {"mean": sum(v) / len(v), "max": max(v)}
            for c, v in per_consumer_use.items()
        },
        "multi_consumer": {
            "docs_cited_ge2_frac": docs_used_ge2 / total_docs,
            "docs_cited_ge1_frac": docs_used_ge1 / total_docs,
            "docs_dead_frac": docs_used_0 / total_docs,
        },
        "mutation_sim_doc_level": {
            "n_mutations": n_mut,
            "exact_invalidations": exact_inv,
            "query_relative_invalidations": qr_inv,
            "exact_mean_per_mutation": exact_inv / n_mut,
            "qr_mean_per_mutation": qr_inv / n_mut,
            "count_reduction": 1 - qr_inv / exact_inv,
            "exact_cost": exact_cost,
            "qr_cost": qr_cost,
            "cost_reduction": 1 - qr_cost / exact_cost,
            "note": "exact/identity replay invalidates all 3 downstream consumers of a mutated doc; query-relative invalidates only citers. BIAS: citation undercounts true usage (agents may use without citing) -> qr invalidations are a LOWER bound -> reductions are OPTIMISTIC.",
        },
        "title_missing": title_missing,
    }
    return res


def validate_against_real_flips():
    """Exploratory: does citation predict real downstream flips per (block, receiver)?"""
    flips = defaultdict(lambda: [0, 0])  # cited -> [flips, n]; not-cited -> same
    # build usage per (trace, block) from traces
    traces = {t["trace_id"]: t for t in load_traces()}
    n_pairs = 0
    with open(PAIRS) as f:
        for line in f:
            r = json.loads(line)
            tr = traces.get(r["trace_id"])
            if tr is None:
                continue
            agents = {a["agent_id"]: a for a in tr["agents"]}
            titles = doc_titles(agents["retriever"]["blocks"])
            t = titles.get(r["block_id"])
            recv = r["receiver_agent"]
            if recv not in agents:
                continue
            cited = bool(t) and f"({t})" in agents[recv]["output_text"]
            key = "cited" if cited else "not_cited"
            flips[key][0] += r["real_flip_repair"]
            flips[key][1] += 1
            n_pairs += 1
    out = {"n_pairs": n_pairs}
    for k, (fl, n) in flips.items():
        out[k] = {"n": n, "real_flip_repair_rate": fl / n if n else None}
    out["note"] = ("exploratory validation of the citation usage signal against "
                   "E0 real-perturbation downstream flips (per pair); not a "
                   "pre-registered criterion")
    return out


if __name__ == "__main__":
    res = analyse()
    res["validation_vs_real_flips"] = validate_against_real_flips()
    with open(OUT, "w") as f:
        json.dump(res, f, indent=2, ensure_ascii=False)
    print(json.dumps(res, indent=2, ensure_ascii=False))
