#!/usr/bin/env python3
"""Recompute the manuscript's load-bearing descriptive counts.

This is a CPU-only, read-only Stage 2.5 audit.  It reads the two preserved
historical repositories, but writes only the explicitly requested output.
The output records logical source names and SHA-256 values, never local paths.
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import importlib.util
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from types import ModuleType


HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parents[1]
ROUTE_TASKS = (
    "astropy__astropy-12907",
    "matplotlib__matplotlib-18869",
    "pallets__flask-4045",
    "pydata__xarray-3364",
    "pytest-dev__pytest-11143",
    "sphinx-doc__sphinx-10325",
)
ROUTE_VARIANTS = ("old", "new_no_change", "new_dependent_source_change")
_DOTDOT_RE = re.compile(r"^[+-]d[rwxst-]{9}.*\s\.\.\s*$")
_LEGACY_DOC_TITLE_RE = re.compile(r"^Document \(([^)]+)\):")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, ensure_ascii=False, indent=2, default=str
    ).encode("utf-8")


def stripped_sha(messages: list[dict]) -> str:
    stripped = [{key: value for key, value in message.items() if key != "extra"}
                for message in messages]
    return hashlib.sha256(canonical_bytes(stripped)).hexdigest()


def extract_turns(trajectory: dict) -> list[dict]:
    messages = trajectory.get("messages", [])
    turns: list[dict] = []
    index = 2
    while index < len(messages):
        message = messages[index]
        if message.get("role") != "assistant":
            break
        actions = message.get("extra", {}).get("actions", [])
        command = "\n".join(action.get("command", "") for action in actions)
        observation = (
            messages[index + 1]
            if index + 1 < len(messages)
            and messages[index + 1].get("role") == "user"
            else None
        )
        turns.append(
            {
                "command": command,
                "assistant": message,
                "observation": observation,
            }
        )
        index += 2
    return turns


def oracle_diff(old: str, new: str) -> tuple[float, int, list[str]]:
    old_lines, new_lines = old.splitlines(), new.splitlines()
    matcher = difflib.SequenceMatcher(a=old_lines, b=new_lines, autojunk=False)
    changed = 0
    changed_lines: list[str] = []
    for tag, old_start, old_end, new_start, new_end in matcher.get_opcodes():
        if tag == "equal":
            continue
        changed += (old_end - old_start) + (new_end - new_start)
        changed_lines.extend(f"-{line}" for line in old_lines[old_start:old_end])
        changed_lines.extend(f"+{line}" for line in new_lines[new_start:new_end])
    denominator = len(old_lines)
    ratio = changed / denominator if denominator else (0.0 if not changed else float("inf"))
    return ratio, changed, changed_lines


def full_invocation_same(old_messages: list[dict], new_messages: list[dict], turn: int) -> bool:
    end = 2 + 2 * turn
    if len(old_messages) < end or len(new_messages) < end:
        return False
    return stripped_sha(old_messages[:end]) == stripped_sha(new_messages[:end])


def route_a_counts(route_root: Path) -> tuple[dict, list[dict]]:
    trajectory_dir = route_root / "runs/route_a_plus_v7/g1_pilot/matrix_v2/trajectories"
    expected_files = [
        trajectory_dir / f"{task}_{variant}_attempt1.json"
        for task in ROUTE_TASKS
        for variant in ROUTE_VARIANTS
    ]
    missing = [path.name for path in expected_files if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing frozen Route A+ trajectories: {missing}")

    events: list[dict] = []
    for task in ROUTE_TASKS:
        old_path = trajectory_dir / f"{task}_old_attempt1.json"
        old = load_json(old_path)
        old_turns = extract_turns(old)
        for stratum, variant in (
            ("no_change", "new_no_change"),
            ("dependent_source_change", "new_dependent_source_change"),
        ):
            new_path = trajectory_dir / f"{task}_{variant}_attempt1.json"
            new = load_json(new_path)
            new_turns = extract_turns(new)
            first_command_difference = None
            comparable = min(len(old_turns), len(new_turns))
            for position in range(comparable):
                old_turn = old_turns[position]
                new_turn = new_turns[position]
                if old_turn["command"] != new_turn["command"] and first_command_difference is None:
                    first_command_difference = position
                if first_command_difference is not None:
                    continue
                old_obs = old_turn["observation"]
                new_obs = new_turn["observation"]
                if old_obs is None or new_obs is None:
                    continue
                old_node = (
                    old_obs.get("extra", {}).get("returncode"),
                    old_obs.get("extra", {}).get("raw_output"),
                )
                new_node = (
                    new_obs.get("extra", {}).get("returncode"),
                    new_obs.get("extra", {}).get("raw_output"),
                )
                ratio, changed, changed_lines = oracle_diff(
                    old_obs.get("content", ""), new_obs.get("content", "")
                )
                node_differs = old_node != new_node
                oracle = node_differs and (ratio <= 0.05 or changed <= 2)
                if not oracle:
                    continue
                has_next = position + 1 < comparable
                next_assistant_same = has_next and (
                    old_turns[position + 1]["assistant"].get("content")
                    == new_turns[position + 1]["assistant"].get("content")
                )
                next_command_same = has_next and (
                    old_turns[position + 1]["command"]
                    == new_turns[position + 1]["command"]
                )
                suffix_old = [
                    (turn["command"], turn["assistant"].get("content"))
                    for turn in old_turns[position + 1:]
                ]
                suffix_new = [
                    (turn["command"], turn["assistant"].get("content"))
                    for turn in new_turns[position + 1:]
                ]
                events.append(
                    {
                        "task": task,
                        "stratum": stratum,
                        "turn": position + 1,
                        "dotdot_parent_mtime_only": bool(changed_lines)
                        and all(_DOTDOT_RE.match(line) for line in changed_lines),
                        "next_command_same": next_command_same,
                        "next_assistant_same": next_assistant_same,
                        "suffix_same": suffix_old == suffix_new,
                        "full_invocation_same": full_invocation_same(
                            old["messages"], new["messages"], position + 1
                        ),
                        "exit_status_same": (
                            old.get("info", {}).get("exit_status")
                            == new.get("info", {}).get("exit_status")
                        ),
                    }
                )

    source_records = [
        {
            "logical_path": f"route_a_plus:{path.relative_to(route_root)}",
            "bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        }
        for path in expected_files
    ]
    return (
        {
            "expected_frozen_runs": len(expected_files),
            "observed_frozen_runs": len(expected_files),
            "candidate_events": len(events),
            "dotdot_parent_mtime_only": sum(
                event["dotdot_parent_mtime_only"] for event in events
            ),
            "next_command_disagreements": sum(
                not event["next_command_same"] for event in events
            ),
            "next_assistant_response_disagreements": sum(
                not event["next_assistant_same"] for event in events
            ),
            "suffix_disagreements": sum(not event["suffix_same"] for event in events),
            "exit_status_disagreements": sum(
                not event["exit_status_same"] for event in events
            ),
            "full_invocation_matches": sum(
                event["full_invocation_same"] for event in events
            ),
            "next_assistant_response_definition": "next assistant content differs",
            "full_invocation_definition": (
                "byte identity of the complete prompt prefix for the next assistant turn "
                "after removing production-only extra metadata"
            ),
            "event_rows": events,
        },
        source_records,
    )


def _block_class(block_id: str) -> str:
    return block_id.split("-", 1)[0]


def _document_title(text: str, *, legacy: bool = False) -> str | None:
    stripped = text.strip()
    if legacy:
        match = _LEGACY_DOC_TITLE_RE.match(stripped)
        return match.group(1) if match else None

    prefix = "Document ("
    if not stripped.startswith(prefix):
        return None
    depth = 1
    for index in range(len(prefix), len(stripped)):
        char = stripped[index]
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                if stripped[index + 1:index + 2] != ":":
                    return None
                return stripped[len(prefix):index]
    return None


def document_proxy_counts(trace_path: Path, pairs_path: Path) -> dict:
    """Recompute the title-mention diagnostic on its stated document estimand.

    The frozen C6 implementation is retained unchanged.  Its validation helper
    treated every non-document pair as "not cited" and its title regex stopped
    at the first closing parenthesis.  This Stage 2.5 recount both reproduces
    those legacy cells and reports the corrected document-only cells.
    """

    traces = {row["trace_id"]: row for row in load_jsonl(trace_path)}
    rows = load_jsonl(pairs_path)
    block_type_pairs: Counter[str] = Counter()
    block_type_real_flips: Counter[str] = Counter()
    corrected = {
        "title_mentioned": Counter(),
        "title_unmentioned": Counter(),
    }
    legacy = {
        "cited": Counter(),
        "not_cited": Counter(),
    }
    legacy_parser_failures = 0
    reclassified_pair_ids: list[str] = []

    for row in rows:
        block_type = _block_class(row["block_id"])
        block_type_pairs[block_type] += 1
        block_type_real_flips[block_type] += int(row["real_flip_repair"])

        trace = traces.get(row["trace_id"])
        if trace is None:
            raise ValueError(f"pair references unknown trace: {row['pair_id']}")
        agents = {agent["agent_id"]: agent for agent in trace["agents"]}
        retriever = agents.get("retriever")
        receiver = agents.get(row["receiver_agent"])
        if retriever is None or receiver is None:
            raise ValueError(f"pair has unknown producer/receiver: {row['pair_id']}")

        blocks = {
            block["block_id"]: block
            for block in retriever["blocks"]
            if block["block_id"].startswith("doc-")
        }
        block = blocks.get(row["block_id"])

        # Exact reproduction of the frozen helper: a non-document row or a
        # failed title parse is silently assigned to the negative stratum.
        legacy_title = (
            _document_title(block["text"], legacy=True) if block is not None else None
        )
        legacy_cited = bool(legacy_title) and (
            f"({legacy_title})" in receiver["output_text"]
        )
        legacy_key = "cited" if legacy_cited else "not_cited"
        legacy[legacy_key]["pairs"] += 1
        legacy[legacy_key]["real_flips"] += int(row["real_flip_repair"])

        if block_type != "doc":
            continue
        if block is None:
            raise ValueError(f"document pair has no retriever block: {row['pair_id']}")
        title = _document_title(block["text"])
        if title is None:
            raise ValueError(f"document title cannot be parsed: {row['pair_id']}")
        if legacy_title is None:
            legacy_parser_failures += 1

        title_mentioned = f"({title})" in receiver["output_text"]
        key = "title_mentioned" if title_mentioned else "title_unmentioned"
        corrected[key]["pairs"] += 1
        corrected[key]["real_flips"] += int(row["real_flip_repair"])
        corrected[key]["identity_flips"] += int(row["identity_flip_repair"])
        if title_mentioned and not legacy_cited:
            reclassified_pair_ids.append(row["pair_id"])

    document_pairs = block_type_pairs["doc"]
    non_document_pairs = len(rows) - document_pairs
    mentioned = corrected["title_mentioned"]
    unmentioned = corrected["title_unmentioned"]
    if mentioned["pairs"] + unmentioned["pairs"] != document_pairs:
        raise AssertionError("document strata do not partition the document pairs")

    def rate(counter: Counter[str], numerator: str) -> float | None:
        return (
            counter[numerator] / counter["pairs"]
            if counter["pairs"]
            else None
        )

    return {
        "estimand": "document perturbation pair with reader/verifier/writer receiver",
        "all_pair_rows": len(rows),
        "block_type_pair_counts": dict(sorted(block_type_pairs.items())),
        "block_type_real_flip_counts": dict(sorted(block_type_real_flips.items())),
        "document_pairs": document_pairs,
        "non_document_pairs_excluded": non_document_pairs,
        "title_mentioned": {
            **dict(mentioned),
            "real_flip_rate": rate(mentioned, "real_flips"),
            "identity_flip_rate": rate(mentioned, "identity_flips"),
        },
        "title_unmentioned": {
            **dict(unmentioned),
            "real_flip_rate": rate(unmentioned, "real_flips"),
            "identity_flip_rate": rate(unmentioned, "identity_flips"),
        },
        "parser_correction": {
            "legacy_regex": _LEGACY_DOC_TITLE_RE.pattern,
            "corrected_parser": (
                "balanced-parenthesis scan after 'Document (' followed by ':'"
            ),
            "legacy_failures_among_document_pairs": legacy_parser_failures,
            "pairs_reclassified_as_title_mentioned": len(reclassified_pair_ids),
            "reclassified_pair_ids": reclassified_pair_ids,
        },
        "legacy_reproduction": {
            "scope": (
                "all pair rows; non-document rows and failed document-title parses "
                "were assigned to not_cited"
            ),
            "cited_pairs": legacy["cited"]["pairs"],
            "cited_real_flips": legacy["cited"]["real_flips"],
            "not_cited_pairs": legacy["not_cited"]["pairs"],
            "not_cited_real_flips": legacy["not_cited"]["real_flips"],
        },
        "measurement_status": "INVALID_TEXT_PROXY_UNCHANGED",
    }


def downstream_sentence_sensitivity(trace_path: Path, c6_module: ModuleType) -> dict:
    """Exclude retriever-side cite/doc incidences from a sensitivity recount.

    The registered C6 population deliberately counts every block-agent
    incidence, including the retriever's own cite/document inputs.  Generated
    plan/evidence/verification blocks first appear in a later agent's input, so
    all of those observed incidences remain downstream.
    """

    ratios: dict[str, list[float]] = defaultdict(list)
    excluded = Counter()
    included = Counter()
    for trace in load_jsonl(trace_path):
        for agent in trace["agents"]:
            usage = c6_module.ConsumerUsage(agent["output_text"])
            for block in agent["blocks"]:
                block_type = _block_class(block["block_id"])
                if block_type == "sys":
                    continue
                if agent["agent_id"] == "retriever" and block_type in {"cite", "doc"}:
                    excluded[block_type] += 1
                    continue
                sentences = c6_module.split_sentences(block["text"])
                normalized = [c6_module.normalize(sentence) for sentence in sentences]
                measurable = [
                    index
                    for index, sentence in enumerate(normalized)
                    if c6_module.word_count(sentence) >= c6_module.MIN_SENT_WORDS
                ]
                if not measurable:
                    continue
                substring_hits = sum(
                    usage.used_substring(normalized[index]) for index in measurable
                )
                jaccard_hits = sum(
                    usage.used_jaccard(
                        c6_module.ngrams(normalized[index].split())
                    )
                    for index in measurable
                )
                ratios["substring"].append(substring_hits / len(measurable))
                ratios["jaccard"].append(jaccard_hits / len(measurable))
                included[block_type] += 1

    result = {
        "definition": (
            "sensitivity analysis excluding retriever-side cite/document "
            "incidences; this does not replace the frozen registered population"
        ),
        "excluded_retriever_incidences": dict(sorted(excluded.items())),
        "included_by_class": dict(sorted(included.items())),
        "non_system_downstream_incidences": sum(included.values()),
    }
    for variant in ("substring", "jaccard"):
        values = sorted(ratios[variant])
        result[variant] = {
            "zero_count": sum(value == 0 for value in values),
            "zero_fraction_raw": sum(value == 0 for value in values) / len(values),
            "zero_fraction_display_percent": round(
                100 * sum(value == 0 for value in values) / len(values), 2
            ),
            "median": c6_module.percentile(values, 0.5),
            "p90": c6_module.percentile(values, 0.9),
        }
    return result


def historical_counts(historical_root: Path) -> tuple[dict, list[dict]]:
    pairs = historical_root / "runs/pairs"
    traces = historical_root / "runs/traces/taskA_e0.jsonl"

    c6_module = load_module("stage25_c6", PROJECT_ROOT / "gates/C6/analyse_workflow.py")
    c6_module.TRACE_PATH = str(traces)
    sentence = c6_module.analyse()

    document = document_proxy_counts(
        traces, pairs / "taskA_e0_identity_ctrl.jsonl"
    )
    downstream_sensitivity = downstream_sentence_sensitivity(traces, c6_module)

    c3_module = load_module(
        "stage25_c3", PROJECT_ROOT / "gates/C3/v2_1/reanalyse_v2_1.py"
    )
    c3 = c3_module.analyse(pairs)
    c3["meta"]["input_root"] = "historical:runs/pairs"

    identity_rows = load_jsonl(pairs / "taskA_e0_identity_ctrl.jsonl")
    identity_repair_flips = sum(row["identity_flip_repair"] for row in identity_rows)

    source_paths = (
        pairs / "taskA_e0_control.jsonl",
        pairs / "taskA_e0_identity_ctrl.jsonl",
        pairs / "taskB_e0.jsonl",
        pairs / "taskB_e0_identity_ctrl.jsonl",
        traces,
    )
    source_records = [
        {
            "logical_path": f"historical:{path.relative_to(historical_root)}",
            "bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        }
        for path in source_paths
    ]

    table_one = {
        "sentence_proxy": {
            "frozen_traces": sentence["meta"]["n_traces"],
            "registered_non_system_block_agent_incidences": sentence["edges"]["non_sys_total"],
            "registered_population_includes_retriever_cite_doc_incidences": True,
            "substring_zero_fraction_raw": sentence["used_region"]["substring"]["all"]["frac_zero_use"],
            "substring_zero_fraction_display_percent": round(
                100 * sentence["used_region"]["substring"]["all"]["frac_zero_use"], 2
            ),
            "jaccard_zero_fraction_raw": sentence["used_region"]["jaccard"]["all"]["frac_zero_use"],
            "jaccard_zero_fraction_display_percent": round(
                100 * sentence["used_region"]["jaccard"]["all"]["frac_zero_use"], 2
            ),
            "substring_median": sentence["used_region"]["substring"]["all"]["median"],
            "substring_p90": sentence["used_region"]["substring"]["all"]["p90"],
            "jaccard_median": sentence["used_region"]["jaccard"]["all"]["median"],
            "jaccard_p90": sentence["used_region"]["jaccard"]["all"]["p90"],
            "generation_aligned_downstream_sensitivity": downstream_sensitivity,
        },
        "citation_proxy": {
            **document,
            "all_pair_identity_control_repair_flips": identity_repair_flips,
            "all_pair_identity_control_pairs": len(identity_rows),
            "all_pair_identity_control_repair_rate_raw": identity_repair_flips / len(identity_rows),
        },
    }
    return {"table_one": table_one, "c3": c3}, source_records


def d0_counts(historical_root: Path) -> dict:
    module = load_module(
        "stage25_d0", PROJECT_ROOT / "experiments/actual_skip_calibration/validate_d0.py"
    )
    report = module.validate(historical_root, verify_hashes=True)
    report["source_root"] = "historical:repository-root"
    return report


def recompute(historical_root: Path, route_root: Path) -> dict:
    route, route_sources = route_a_counts(route_root)
    historical, historical_sources = historical_counts(historical_root)
    table_one = {"diff_proxy": route, **historical["table_one"]}
    return {
        "schema_version": "stage2.5-descriptive-count-audit/v2",
        "status": "complete",
        "inputs": sorted(
            historical_sources + route_sources, key=lambda item: item["logical_path"]
        ),
        "table_1": table_one,
        "c3_recomputed": historical["c3"],
        "d0_recomputed": d0_counts(historical_root),
        "paper_bindings": {
            "18_frozen_agent_runs": table_one["diff_proxy"]["observed_frozen_runs"],
            "4968_registered_non_system_block_agent_incidences": table_one["sentence_proxy"]["registered_non_system_block_agent_incidences"],
            "763_document_perturbation_pairs": table_one["citation_proxy"]["document_pairs"],
            "table_1_all_cells_recomputed": True,
            "table_1_semantic_corrections_applied": True,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--historical-root", type=Path, required=True)
    parser.add_argument("--route-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=HERE / "descriptive_counts.json")
    args = parser.parse_args()
    result = recompute(args.historical_root, args.route_root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(result["paper_bindings"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
