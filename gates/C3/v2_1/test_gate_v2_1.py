#!/usr/bin/env python3
"""Focused, fixture-level regression tests for the C3 v2.1 correction."""

import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path


D = Path(__file__).parent
FIXTURES = D.parent / "fixtures"


def load_module():
    module_path = D / "reanalyse_v2_1.py"
    spec = importlib.util.spec_from_file_location("reanalyse_v2_1", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ANALYSIS = load_module()


def fixture_hashes():
    return {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(FIXTURES.glob("*"))
        if path.is_file()
    }


def run_fixture_analysis():
    before = fixture_hashes()
    with tempfile.TemporaryDirectory(prefix="c3-v2-1-test-") as tmp_dir:
        output = Path(tmp_dir) / "results.json"
        subprocess.run(
            [
                sys.executable,
                str(D / "reanalyse_v2_1.py"),
                "--input-root",
                str(FIXTURES),
                "--output",
                str(output),
            ],
            check=True,
            capture_output=True,
        )
        results = json.loads(output.read_text())
    assert before == fixture_hashes(), "focused test modified tracked fixture data"
    return results


RESULTS = run_fixture_analysis()


def test_recompute_still_wrong_excludes_rescue():
    rows = [{}, {}, {}, {}]
    orig_correct = [False, False, True, True]
    flips = [0, 1, 1, 0]
    stats = ANALYSIS.arm_stats(rows, orig_correct, flips)
    assert stats["recompute_still_wrong"] == 0.25
    assert stats["rescue"] == 0.25
    assert stats["rho_blame"] == 0.25


def test_recompute_partition_for_orig_wrong_cases():
    for task in ("taskA", "taskB"):
        baseline_wrong = 1 - RESULTS[task]["baseline_acc"]
        for arm in ("reuse", "repair"):
            observed = (
                RESULTS[task][arm]["recompute_still_wrong"]
                + RESULTS[task][arm]["rescue"]
            )
            assert abs(observed - baseline_wrong) < 1e-12, (task, arm)
            outcome_partition = (
                RESULTS[task][arm]["rho_blame"]
                + RESULTS[task][arm]["recompute_still_wrong"]
            )
            assert abs(outcome_partition - RESULTS[task][arm]["rho_outcome"]) < 1e-12


def test_fixture_corrected_counts():
    expected = {
        ("taskA", "reuse"): 19 / 20,
        ("taskA", "repair"): 19 / 20,
        ("taskB", "reuse"): 13 / 30,
        ("taskB", "repair"): 12 / 30,
    }
    for (task, arm), rate in expected.items():
        assert abs(RESULTS[task][arm]["recompute_still_wrong"] - rate) < 1e-12


def test_economic_value_unchanged_but_label_corrected():
    economics = RESULTS["economics"]["taskB_reuse"]["rho_outcome"]
    s = economics["s"]
    rho = economics["rho"]
    expected = s - 0.01 - rho * (s + 0.01)
    cell = economics["per_v"]["0.01"]
    assert abs(expected - cell["delta_over_full"]) < 1e-12
    assert "delta_over_S" not in cell
    assert economics["metric"] == "net_saving_fraction_of_full_run"


def test_verifier_cost_is_fraction_of_full_run():
    meta = RESULTS["meta"]
    assert meta["C_full"] == 1.0
    assert meta["v_semantics"] == "verifier_cost_fraction_of_full_run"
    assert 0.1 in meta["v_grid"]


def test_verdict_consistency():
    verdict_inputs = RESULTS["verdict_inputs"]
    naive = verdict_inputs["GO_NAIVE"]
    conditional = verdict_inputs["GO_CONDITIONAL"]
    expected = "GO_NAIVE" if naive else (
        "NEED_NEW_VERIFIER" if conditional else "NO_GO"
    )
    assert verdict_inputs["overall"] == expected


if __name__ == "__main__":
    tests = [value for key, value in sorted(globals().items()) if key.startswith("test_")]
    for test in tests:
        test()
        print("PASS", test.__name__)
    print(f"{len(tests)} tests passed")
