#!/usr/bin/env python3
"""Focused tests for C3 gate v2 (stdlib only)."""
import json, subprocess, sys
from pathlib import Path

D = Path(__file__).parent


def setup():
    out = D.parent / "fixtures" / "results_v2_fixture.json"
    subprocess.run([sys.executable, str(D / "reanalyse_v2.py"),
                    "--input-root", str(D.parent / "fixtures"),
                    "--output", str(out)],
                   check=True, capture_output=True)
    return json.loads(out.read_text())


R = setup()


def test_formula_corrected():
    # Δ/S = s − v − ρ(s+RB): check one cell by hand
    e = R["economics"]["taskB_reuse"]["rho_outcome"]
    s, rho, RB = e["s"], e["rho"], 0.01
    expect = s - 0.01 - rho * (s + RB)
    got = e["per_v"]["0.01"]["delta_over_S"]
    assert abs(expect - got) < 1e-9, (expect, got)


def test_no_unsatisfiable_threshold():
    # v grid must not contain values > max saving s
    s = R["taskB"]["cost"]["s_reuse"]
    for v in R["meta"]["v_grid"]:
        assert v < s


def test_rho_fields_separated():
    for arm in ("reuse", "repair"):
        for k in ("rho_outcome", "rho_blame", "rescue", "recompute_still_wrong"):
            assert 0.0 <= R["taskB"][arm][k] <= 1.0, (arm, k)


def test_cases_present():
    for arm in ("reuse", "repair"):
        assert R["taskB"][arm]["rho_blame"] * R["taskB"][arm]["n"] >= 1
        assert R["taskB"][arm]["acc"] * R["taskB"][arm]["n"] >= 1


def test_verdict_consistency():
    vi = R["verdict_inputs"]
    naive = vi["GO_NAIVE"]; cond = vi["GO_CONDITIONAL"]
    expect = "GO_NAIVE" if naive else ("NEED_NEW_VERIFIER" if cond else "NO_GO")
    assert vi["overall"] == expect


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print("PASS", fn.__name__)
    print(f"{len(fns)} tests passed")
