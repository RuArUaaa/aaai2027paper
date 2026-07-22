#!/usr/bin/env python3
"""Focused regression tests for the D0 static audit."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from validate_d0 import HERE, load_json, reconstruct_budget, validate


class D0StaticAuditTests(unittest.TestCase):
    def test_budget_reconstruction(self) -> None:
        self.assertEqual(
            reconstruct_budget(164, 4, 3),
            {
                "condition_cells": 1968,
                "hypothetical_two_stage_no_hit_calls": 3936,
                "optimistic_identity_response_hits_saved_calls": 656,
                "optimistic_two_stage_executed_calls": 3280,
                "separate_warmup_calls": 328,
                "optimistic_two_stage_with_separate_warmup_calls": 3608,
                "native_four_node_no_hit_calls": 7872,
            },
        )

    def test_authorization_invariants(self) -> None:
        results = load_json(HERE / "d0_results.json")
        usage = results["authorization_and_usage"]
        self.assertEqual(usage["experiment_authorization"], "NONE")
        self.assertEqual(usage["model_experiment_calls"], 0)
        self.assertEqual(usage["gpu_runs"], 0)
        self.assertEqual(usage["new_agent_trajectories"], 0)
        self.assertEqual(usage["experimental_mutations"], 0)

    def test_local_validation_does_not_write_tracked_outputs(self) -> None:
        manifest = load_json(HERE / "d0_source_manifest.json")
        with tempfile.TemporaryDirectory() as tmpdir:
            source_root = Path(tmpdir)
            for entry in manifest["files"]:
                path = source_root / entry["path"]
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b"fixture")
            report = validate(source_root, verify_hashes=False)
        self.assertTrue(report["ok"], json.dumps(report, indent=2))
        self.assertEqual(report["source_hashes_checked"], 0)


if __name__ == "__main__":
    unittest.main()
