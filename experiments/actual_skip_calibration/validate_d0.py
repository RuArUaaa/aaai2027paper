#!/usr/bin/env python3
"""Validate the D0 static-audit manifest and arithmetic without running models."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
MANIFEST_PATH = HERE / "d0_source_manifest.json"
RESULTS_PATH = HERE / "d0_results.json"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def reconstruct_budget(tasks: int, arms: int, conditions: int) -> dict[str, int]:
    cells = tasks * arms * conditions
    two_stage_no_hit = cells * 2
    identity_response_hits_saved = tasks * 2 * 2
    optimistic_executed = two_stage_no_hit - identity_response_hits_saved
    warmup = tasks * 2
    return {
        "condition_cells": cells,
        "hypothetical_two_stage_no_hit_calls": two_stage_no_hit,
        "optimistic_identity_response_hits_saved_calls": identity_response_hits_saved,
        "optimistic_two_stage_executed_calls": optimistic_executed,
        "separate_warmup_calls": warmup,
        "optimistic_two_stage_with_separate_warmup_calls": optimistic_executed + warmup,
        "native_four_node_no_hit_calls": cells * 4,
    }


def validate(source_root: Path, verify_hashes: bool = True) -> dict:
    manifest = load_json(MANIFEST_PATH)
    results = load_json(RESULTS_PATH)
    errors: list[str] = []

    budget = results["fable5_budget_reconstruction"]
    reconstructed = reconstruct_budget(
        budget["tasks"], budget["arms"], budget["conditions"]
    )
    for field, expected in reconstructed.items():
        if budget.get(field) != expected:
            errors.append(f"budget mismatch for {field}: {budget.get(field)} != {expected}")

    if budget["fable5_cap_sufficient"] is not False:
        errors.append("Fable 5 cap must be marked insufficient")
    if budget["optimistic_two_stage_executed_calls"] <= budget["fable5_cap"]:
        errors.append("optimistic lower bound unexpectedly fits the Fable 5 cap")

    usage = results["authorization_and_usage"]
    for field in (
        "model_experiment_calls",
        "gpu_runs",
        "new_agent_trajectories",
        "experimental_mutations",
    ):
        if usage[field] != 0:
            errors.append(f"{field} must remain zero")
    if usage["experiment_authorization"] != "NONE":
        errors.append("experiment authorization must remain NONE")

    hash_checks = 0
    if verify_hashes:
        for entry in manifest["files"]:
            path = source_root / entry["path"]
            if not path.is_file():
                errors.append(f"missing source file: {path}")
                continue
            observed = sha256_file(path)
            if observed != entry["sha256"]:
                errors.append(
                    f"sha256 mismatch for {entry['path']}: {observed} != {entry['sha256']}"
                )
            hash_checks += 1

    return {
        "ok": not errors,
        "errors": errors,
        "source_root": str(source_root),
        "source_hashes_checked": hash_checks,
        "budget": reconstructed,
        "verdict": results["verdict"],
    }


def main() -> int:
    manifest = load_json(MANIFEST_PATH)
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source-root",
        type=Path,
        default=Path(manifest["source_repository"]),
        help="read-only historical source repository",
    )
    parser.add_argument(
        "--skip-source-hashes",
        action="store_true",
        help="validate local arithmetic/invariants when historical source is unavailable",
    )
    args = parser.parse_args()
    report = validate(args.source_root, verify_hashes=not args.skip_source_hashes)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
