#!/usr/bin/env python3
"""Focused regression tests for the Stage 2.5 count audit."""

from __future__ import annotations

import json
import importlib.util
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parents[1]
HISTORICAL_ROOT = os.environ.get("AAAI27_HISTORICAL_ROOT")
ROUTE_ROOT = os.environ.get("AAAI27_ROUTE_A_PLUS_ROOT")

SPEC = importlib.util.spec_from_file_location(
    "stage25_recompute", HERE / "recompute_descriptive_counts.py"
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load Stage 2.5 recount module")
ANALYSIS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ANALYSIS)


class DescriptiveCountAuditTests(unittest.TestCase):
    def test_nested_parentheses_title_parser(self) -> None:
        text = "Document (Be the One (Poison song)): body later has (noise): text"
        self.assertEqual(
            ANALYSIS._document_title(text), "Be the One (Poison song)"
        )
        self.assertIsNone(ANALYSIS._document_title(text, legacy=True))

    @unittest.skipUnless(
        HISTORICAL_ROOT and ROUTE_ROOT,
        "set AAAI27_HISTORICAL_ROOT and AAAI27_ROUTE_A_PLUS_ROOT for full recount",
    )
    def test_full_recompute_uses_temporary_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "counts.json"
            subprocess.run(
                [
                    "python3",
                    str(HERE / "recompute_descriptive_counts.py"),
                    "--historical-root",
                    HISTORICAL_ROOT,
                    "--route-root",
                    ROUTE_ROOT,
                    "--output",
                    str(output),
                ],
                check=True,
                cwd=PROJECT_ROOT,
                capture_output=True,
                text=True,
            )
            result = json.loads(output.read_text())

        diff = result["table_1"]["diff_proxy"]
        self.assertEqual(diff["observed_frozen_runs"], 18)
        self.assertEqual(diff["candidate_events"], 8)
        self.assertEqual(diff["dotdot_parent_mtime_only"], 8)
        self.assertEqual(diff["next_command_disagreements"], 4)
        self.assertEqual(diff["next_assistant_response_disagreements"], 6)
        self.assertEqual(diff["suffix_disagreements"], 8)
        self.assertEqual(diff["exit_status_disagreements"], 4)
        self.assertEqual(diff["full_invocation_matches"], 0)

        sentence = result["table_1"]["sentence_proxy"]
        self.assertEqual(sentence["frozen_traces"], 100)
        self.assertEqual(
            sentence["registered_non_system_block_agent_incidences"], 4968
        )
        self.assertEqual(sentence["substring_zero_fraction_display_percent"], 98.09)
        self.assertEqual(sentence["jaccard_zero_fraction_display_percent"], 95.69)
        self.assertEqual(sentence["substring_median"], 0.0)
        self.assertEqual(sentence["substring_p90"], 0.0)
        self.assertEqual(sentence["jaccard_median"], 0.0)
        self.assertEqual(sentence["jaccard_p90"], 0.0)
        sensitivity = sentence["generation_aligned_downstream_sensitivity"]
        self.assertEqual(sensitivity["non_system_downstream_incidences"], 3876)
        self.assertEqual(
            sensitivity["substring"]["zero_fraction_display_percent"], 97.70
        )
        self.assertEqual(
            sensitivity["jaccard"]["zero_fraction_display_percent"], 94.71
        )

        citation = result["table_1"]["citation_proxy"]
        self.assertEqual(citation["all_pair_rows"], 1000)
        self.assertEqual(citation["document_pairs"], 763)
        self.assertEqual(citation["non_document_pairs_excluded"], 237)
        self.assertEqual(citation["title_mentioned"]["pairs"], 61)
        self.assertEqual(citation["title_mentioned"]["real_flips"], 0)
        self.assertEqual(citation["title_unmentioned"]["pairs"], 702)
        self.assertEqual(citation["title_unmentioned"]["real_flips"], 36)
        self.assertEqual(citation["title_unmentioned"]["identity_flips"], 35)
        self.assertEqual(
            round(100 * citation["title_unmentioned"]["real_flip_rate"], 2),
            5.13,
        )
        self.assertEqual(
            round(100 * citation["title_unmentioned"]["identity_flip_rate"], 2),
            4.99,
        )
        legacy = citation["legacy_reproduction"]
        self.assertEqual(legacy["cited_pairs"], 53)
        self.assertEqual(legacy["not_cited_pairs"], 947)
        self.assertEqual(legacy["not_cited_real_flips"], 48)
        self.assertEqual(
            citation["parser_correction"]["legacy_failures_among_document_pairs"],
            105,
        )
        self.assertEqual(
            citation["parser_correction"]["pairs_reclassified_as_title_mentioned"],
            8,
        )
        self.assertTrue(result["d0_recomputed"]["ok"])
        self.assertEqual(result["d0_recomputed"]["source_hashes_checked"], 11)


if __name__ == "__main__":
    unittest.main()
