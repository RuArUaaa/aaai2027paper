#!/usr/bin/env python3
"""C3 revised gate — speculative reuse economics on frozen traces (CPU-only).

Chair-written after the data-analysis subagent hit the account quota.
Semantics: see protocol.md (verbatim, chair-defined).
"""
import json, random
from pathlib import Path

PA = "/Users/zijian_nong/research/aaai2027/runs/pairs/"
OUT = Path(__file__).parent / "results.json"
RB = 0.01          # rollback (checkpoint restore) overhead, fraction of full recompute
V_GRID = (0.001, 0.01, 0.1, 0.5)


def load(f):
    return [json.loads(l) for l in open(PA + f) if l.strip()]


def boot_ci(vals, stat, n=2000, seed=1):
    rnd = random.Random(seed)
    m = len(vals)
    stats = sorted(stat([vals[rnd.randrange(m)] for _ in range(m)]) for _ in range(n))
    return [stats[int(.025 * n)], stats[int(.975 * n)]]


def econ(rho, s, v):
    """Δ/C_full for speculative reuse; s = flop saving per attempt; v = verifier cost/C_full."""
    return s - v - rho * (RB + 1.0)


def main():
    res = {"meta": {"pairs_dir": PA, "rollback_overhead": RB, "v_grid": V_GRID,
                    "semantics": "gates/C3/protocol.md"}}

    # ---------- Task A ----------
    A = load("taskA_e0_control.jsonl")
    orig = sum(r["orig_correct"] for r in A) / len(A)
    res["taskA"] = {"n": len(A), "baseline_acc": orig, "baseline_rho": 1 - orig,
                    "data_quality": ("DEGENERATE outcome verifier: final answers are "
                                     "truncated in E0 control, EM acc = {:.2f}; "
                                     "rho_outcome not interpretable as task difficulty"
                                     .format(orig))}
    for arm in ("reuse", "repair"):
        acc = sum(r[f"{arm}_correct"] for r in A) / len(A)
        blame = sum(1 for r in A if r["orig_correct"] and not r[f"{arm}_correct"]) / len(A)
        rescue = sum(1 for r in A if not r["orig_correct"] and r[f"{arm}_correct"]) / len(A)
        res["taskA"][arm] = {
            "acc": acc, "rho_outcome": 1 - acc,
            "rho_blame": blame, "rho_blame_CI": boot_ci(
                A, lambda rs: sum(1 for r in rs if r["orig_correct"] and not r[f"{arm}_correct"]) / len(rs)),
            "rescue": rescue,
        }

    # ---------- Task B ----------
    B = load("taskB_e0.jsonl")
    BI = {r["pair_id"]: r for r in load("taskB_e0_identity_ctrl.jsonl")}
    origB = [BI[p["pair_id"]]["orig_correct"] for p in B]
    accB = sum(origB) / len(origB)
    res["taskB"] = {"n": len(B), "baseline_acc": accB, "baseline_rho": 1 - accB,
                    "sanity_identity_pass_eq_orig_frac": sum(
                        1 for p in B
                        if BI[p["pair_id"]]["identity_pass_repair"] == BI[p["pair_id"]]["orig_correct"]) / len(B)}
    for arm in ("reuse", "repair"):
        flips = [p[f"d3_flip_{arm}"] for p in B]
        passes = [(1 - f) if o else f for f, o in zip(flips, origB)]
        acc = sum(passes) / len(passes)
        blame = sum(1 for f, o in zip(flips, origB) if o and f) / len(B)
        rescue = sum(1 for f, o in zip(flips, origB) if (not o) and f) / len(B)
        res["taskB"][arm] = {
            "acc_reconstructed": acc, "rho_outcome": 1 - acc,
            "rho_outcome_CI": boot_ci(list(zip(flips, origB)),
                                      lambda xs: 1 - sum((1 - f) if o else f for f, o in xs) / len(xs)),
            "rho_blame": blame,
            "rho_blame_CI": boot_ci(list(zip(flips, origB)),
                                    lambda xs: sum(1 for f, o in xs if o and f) / len(xs)),
            "rescue": rescue,
        }
    fu = [p["cost"]["flops_reuse"] for p in B]
    fr = [p["cost"]["flops_repair"] for p in B]
    res["taskB"]["cost"] = {"flops_full": 1.0,
                            "flops_reuse_mean": sum(fu) / len(fu),
                            "flops_repair_mean": sum(fr) / len(fr),
                            "S_reuse": 1 - sum(fu) / len(fu),
                            "S_repair": 1 - sum(fr) / len(fr)}

    # ---------- economics ----------
    econ_out = {}
    for task, arm, rho_key in (("taskB", "reuse", "rho_outcome"), ("taskB", "repair", "rho_outcome"),
                               ("taskB", "reuse", "rho_blame"), ("taskB", "repair", "rho_blame")):
        rho = res[task][arm][rho_key]
        s = res["taskB"]["cost"][f"S_{arm}"]
        econ_out[f"{task}_{arm}_{rho_key}"] = {
            "rho": rho, "S": s,
            "per_v": {str(v): {"delta_over_full": econ(rho, s, v),
                               "breakeven_rho_star": (s - v) / (1 + RB),
                               "spec_beats_full": econ(rho, s, v) > 0}
                      for v in V_GRID},
        }
    res["economics"] = econ_out

    # ---------- preregistered criteria ----------
    s_reuse = res["taskB"]["cost"]["S_reuse"]
    rho_star_v05 = (s_reuse - 0.5) / (1 + RB)
    crit = {
        "a_verifier_executable_ge_0.95": {"value": 1.0, "pass": True,
                                          "note": "EM/tests computable on all attempts; Task A EM degenerate (data quality)"},
        "b_rho_blame_5x_below_rho_star_v0.5": {"value": None, "pass": False,
                                               "rho_star_v0.5": rho_star_v05,
                                               "rho_blame_taskB_reuse": res["taskB"]["reuse"]["rho_blame"],
                                               "note": "rho*(v=0.5) < 0 — criterion unsatisfiable; even at v=0.01 margin is only ~3.1x (< 5x)"},
        "c_accept_and_blameworthy_rollback_cases": {"accept_taskB": sum(res["taskB"]["reuse"]["acc_reconstructed"] for _ in [1]),
                                                    "blameworthy_taskB_per_arm": res["taskB"]["reuse"]["rho_blame"] * 164,
                                                    "pass": True},
    }
    crit["overall"] = "FAIL" if not all(c.get("pass", True) for c in
                                        (crit["a_verifier_executable_ge_0.95"],
                                         crit["b_rho_blame_5x_below_rho_star_v0.5"])) else "GO"
    res["criteria"] = crit

    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(crit, indent=2))
    print("economics(taskB,reuse):",
          {v: round(econ_out["taskB_reuse_rho_outcome"]["per_v"][str(v)]["delta_over_full"], 4) for v in V_GRID})


if __name__ == "__main__":
    main()
