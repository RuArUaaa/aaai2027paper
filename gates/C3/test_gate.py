#!/usr/bin/env python3
"""Focused tests for the C3 revised gate (stdlib only)."""
import json, subprocess, sys
from pathlib import Path

D = Path(__file__).parent


def run_analysis():
    subprocess.run([sys.executable, str(D / "reanalyse_or_simulate.py")],
                   check=True, capture_output=True)


def load():
    return json.loads((D / "results.json").read_text())


def test_rho_in_unit_interval():
    r = load()
    for task in ("taskA", "taskB"):
        for arm in ("reuse", "repair"):
            for k in ("rho_outcome", "rho_blame", "rescue"):
                assert 0.0 <= r[task][arm][k] <= 1.0, (task, arm, k)


def test_case_counts_consistent():
    r = load()
    # blameworthy rollbacks must exist (>=1 per arm on taskB) and accept cases exist
    for arm in ("reuse", "repair"):
        assert r["taskB"][arm]["rho_blame"] * 164 >= 1
        assert r["taskB"][arm]["acc_reconstructed"] * 164 >= 1


def test_breakeven_monotone_in_v():
    r = load()
    stars = [r["economics"]["taskB_reuse_rho_outcome"]["per_v"][v]["breakeven_rho_star"]
             for v in ("0.001", "0.01", "0.1", "0.5")]
    assert all(a >= b for a, b in zip(stars, stars[1:])), stars


def test_pass_reconstruction_sanity():
    r = load()
    # identity pass == orig_correct for the large majority of pairs
    assert r["taskB"]["sanity_identity_pass_eq_orig_frac"] > 0.85


def test_verdict_matches_criteria():
    r = load()
    assert r["criteria"]["overall"] == "FAIL"


if __name__ == "__main__":
    run_analysis()
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print("PASS", fn.__name__)
    print(f"{len(fns)} tests passed")
