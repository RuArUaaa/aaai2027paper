#!/usr/bin/env python3
"""Deterministic descriptive analysis for the selective-consumption audit.

This script consumes normalized, source-backed observations from
``raw_locators.json``. It does not execute candidate code, access the network,
infer semantic use, assign Q levels, or issue a scientific verdict.
"""

import argparse
import json
from collections import defaultdict
from pathlib import Path


REQUIRED_LOCATOR_ROLES = {
    "artifact_creation",
    "routing_or_projection",
    "consumer_input",
    "raw_bypass",
    "trace_serialization",
}

PROHIBITED_PROXY_NAMES = {
    "substring",
    "jaccard",
    "citation_mention",
    "title_mention",
    "embedding",
    "attention",
    "llm_self_report",
    "llm_judge",
    "final_text_semantic_proxy",
}

EDGE_KINDS = {"delivery", "access"}
OBSERVATION_KINDS = EDGE_KINDS | {"non_delivery"}
INPUT_REPRESENTATIONS = {
    "full",
    "typed_projection",
    "access_subset",
    "none",
    "unknown",
}
RAW_BYPASS_STATUSES = {"ABSENT", "PRESENT_MODELLED", "PRESENT_UNMODELLED", "UNKNOWN"}


def load_json(path):
    return json.loads(Path(path).read_text())


def _require(candidate, key):
    if key not in candidate:
        raise ValueError(f"{candidate.get('id', '<unknown>')}: missing {key}")
    return candidate[key]


def validate(raw):
    if raw.get("schema_version") != "1.0":
        raise ValueError("raw_locators schema_version must be 1.0")
    candidate_ids = []
    for candidate in raw.get("candidates", []):
        candidate_id = _require(candidate, "id")
        candidate_ids.append(candidate_id)
        _require(candidate, "repository")
        _require(candidate, "pinned_commit")
        if candidate.get("semantic_proxy_used") is not False:
            raise ValueError(f"{candidate_id}: semantic_proxy_used must be false")
        signals = set(candidate.get("measurement_signals", []))
        prohibited = signals & PROHIBITED_PROXY_NAMES
        if prohibited:
            raise ValueError(f"{candidate_id}: prohibited proxy signals: {sorted(prohibited)}")
        bypass = _require(candidate, "raw_bypass")
        if bypass.get("status") not in RAW_BYPASS_STATUSES:
            raise ValueError(f"{candidate_id}: invalid raw_bypass status")
        for locator in candidate.get("source_locators", []):
            for key in ("id", "role", "path", "symbol", "start_line", "end_line", "sha256", "fact"):
                if key not in locator:
                    raise ValueError(f"{candidate_id}: locator missing {key}")
            if locator["start_line"] < 1 or locator["end_line"] < locator["start_line"]:
                raise ValueError(f"{candidate_id}: invalid locator line range")
        for trace in candidate.get("trace_instances", []):
            for key in ("trace_id", "public_locator", "machine_readable", "observations"):
                if key not in trace:
                    raise ValueError(f"{candidate_id}: trace missing {key}")
            for observation in trace["observations"]:
                if observation.get("kind") not in OBSERVATION_KINDS:
                    raise ValueError(f"{candidate_id}: invalid observation kind")
                if observation.get("input_representation") not in INPUT_REPRESENTATIONS:
                    raise ValueError(f"{candidate_id}: invalid input representation")
                if observation.get("scientific_consumer") not in (True, False):
                    raise ValueError(f"{candidate_id}: scientific_consumer must be boolean")
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("candidate ids must be unique")


def analyse_candidate(candidate):
    locator_roles = {locator["role"] for locator in candidate.get("source_locators", [])}
    role_coverage = {
        role: role in locator_roles for role in sorted(REQUIRED_LOCATOR_ROLES)
    }
    traces = candidate.get("trace_instances", [])
    machine_traces = [trace for trace in traces if trace["machine_readable"]]
    observations = [
        (trace["trace_id"], observation)
        for trace in machine_traces
        for observation in trace["observations"]
        if observation["scientific_consumer"]
    ]

    unresolved_identity_count = sum(
        1
        for _, observation in observations
        if observation["kind"] in EDGE_KINDS
        and (
            not observation.get("artifact_id")
            or not observation.get("consumer_execution_id")
        )
    )

    edges = {}
    non_deliveries = set()
    artifact_consumers = defaultdict(set)
    artifact_projection_fingerprints = defaultdict(set)
    consumer_inputs = []

    for trace_id, observation in observations:
        artifact_id = observation.get("artifact_id")
        consumer_id = observation.get("consumer_execution_id")
        if not artifact_id or not consumer_id:
            continue
        if observation["kind"] == "non_delivery":
            non_deliveries.add((trace_id, artifact_id, consumer_id))
            continue
        edge_key = (trace_id, artifact_id, consumer_id)
        if edge_key in edges:
            continue
        edges[edge_key] = observation
        artifact_key = (trace_id, artifact_id)
        artifact_consumers[artifact_key].add(consumer_id)
        fingerprint = observation.get("input_sha256") or observation.get("projection_id")
        if fingerprint:
            artifact_projection_fingerprints[artifact_key].add(fingerprint)
        consumer_inputs.append(
            {
                "trace_id": trace_id,
                "artifact_id": artifact_id,
                "consumer_execution_id": consumer_id,
                "input_representation": observation["input_representation"],
                "delivered_fields": sorted(observation.get("delivered_fields", [])),
                "input_sha256": observation.get("input_sha256"),
                "full_input_reconstructable": observation.get("full_input_reconstructable"),
                "source_locator": observation.get("source_locator"),
            }
        )

    if machine_traces:
        producer_artifact_count = len(artifact_consumers)
        consumer_edge_count = len(edges)
        max_consumers = max((len(consumers) for consumers in artifact_consumers.values()), default=0)
        repeated_consumer_count = max_consumers if max_consumers >= 2 else 0
        repeated_artifact_count = sum(
            1 for consumers in artifact_consumers.values() if len(consumers) >= 2
        )
        typed_projection_observed = any(
            len(artifact_projection_fingerprints[artifact_key]) >= 2
            and any(
                observation["input_representation"] == "typed_projection"
                for edge_key, observation in edges.items()
                if edge_key[:2] == artifact_key
            )
            for artifact_key in artifact_consumers
        )
        access_record_observed = any(
            observation["kind"] == "access" for _, observation in observations
        )
        selective_non_delivery_observed = bool(non_deliveries)
    else:
        producer_artifact_count = None
        consumer_edge_count = None
        repeated_consumer_count = None
        repeated_artifact_count = None
        typed_projection_observed = None
        access_record_observed = None
        selective_non_delivery_observed = None

    return {
        "id": candidate["id"],
        "repository": candidate["repository"],
        "pinned_commit": candidate["pinned_commit"],
        "source_locator_count": len(candidate.get("source_locators", [])),
        "source_role_coverage": role_coverage,
        "all_required_source_roles_present": all(role_coverage.values()),
        "public_trace_count": len(traces),
        "machine_readable_trace_count": len(machine_traces),
        "trace_observed": bool(machine_traces),
        "producer_artifact_count": producer_artifact_count,
        "consumer_edge_count": consumer_edge_count,
        "repeated_consumer_count": repeated_consumer_count,
        "repeated_artifact_count": repeated_artifact_count,
        "selective_non_delivery_observed": selective_non_delivery_observed,
        "typed_projection_observed": typed_projection_observed,
        "access_record_observed": access_record_observed,
        "unresolved_identity_count": unresolved_identity_count,
        "raw_bypass_status": candidate["raw_bypass"]["status"],
        "consumer_inputs": sorted(
            consumer_inputs,
            key=lambda item: (
                item["trace_id"],
                item["artifact_id"],
                item["consumer_execution_id"],
            ),
        ),
        "outcome_oracle_possible": candidate["outcome_oracle"].get("possible"),
        "framework_modification_required": candidate["integration"].get(
            "framework_modification_required"
        ),
        "native_c3_certificate_present": candidate["c3_directed_verifier"].get(
            "native_certificate_present"
        ),
        "evidence_gaps": sorted(candidate.get("evidence_gaps", [])),
    }


def analyse(raw):
    validate(raw)
    return {
        "schema_version": "1.0",
        "protocol": raw["protocol"],
        "protocol_commit": raw["protocol_commit"],
        "candidate_order": [candidate["id"] for candidate in raw["candidates"]],
        "candidate_results": [
            analyse_candidate(candidate) for candidate in raw["candidates"]
        ],
        "interpretation": None,
        "q_levels": None,
        "c6_qualification": None,
        "c3_directed_verifier_verdict": None,
    }


def write_results(results, output):
    Path(output).write_text(
        json.dumps(results, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default=str(Path(__file__).parent / "raw_locators.json"),
    )
    parser.add_argument(
        "--output",
        default=str(Path(__file__).parent / "results.json"),
    )
    args = parser.parse_args()
    results = analyse(load_json(args.input))
    write_results(results, args.output)
    print(
        json.dumps(
            {
                candidate["id"]: {
                    "trace_observed": candidate["trace_observed"],
                    "producer_artifact_count": candidate["producer_artifact_count"],
                    "consumer_edge_count": candidate["consumer_edge_count"],
                }
                for candidate in results["candidate_results"]
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
