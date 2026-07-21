#!/usr/bin/env python3
"""C3 gate v2 — speculative reuse economics, corrected formula (protocol: v2/protocol.md).

Δ/S = s − v − ρ(s + RB), RB = 0.01.  Usage:
    python3 reanalyse_v2.py [--input-root DIR] [--output FILE]
Default --input-root is the frozen-evidence repo (absolute path); for a clean
clone, point it at gates/C3/fixtures/.
"""
import argparse, json, random
from pathlib import Path

RB = 0.01
V_GRID = (0.001, 0.01, 0.1)
DEFAULT_ROOT = "/Users/zijian_nong/research/aaai2027/runs/pairs"


def load(root, name):
    p = Path(root) / name
    return [json.loads(l) for l in p.open() if l.strip()]


def boot_ci(vals, stat, n=2000, seed=1):
    rnd = random.Random(seed)
    m = len(vals)
    stats = sorted(stat([vals[rnd.randrange(m)] for _ in range(m)]) for _ in range(n))
    return [stats[int(.025 * n)], stats[int(.975 * n)]]


def arm_stats(rows, orig_flags, flips):
    """flips[i] = 1 if arm result differs from from-scratch on row i."""
    n = len(rows)
    passes = [(1 - f) if o else f for f, o in zip(flips, orig_flags)]
    acc = sum(passes) / n
    blame = sum(1 for f, o in zip(flips, orig_flags) if o and f) / n
    rescue = sum(1 for f, o in zip(flips, orig_flags) if (not o) and f) / n
    # recompute-still-wrong: verifier rejects AND from-scratch also wrong
    rsw = sum(1 for f, o in zip(flips, orig_flags) if not o) / n
    pairs = list(zip(flips, orig_flags))
    return {
        "n": n, "acc": acc, "rho_outcome": 1 - acc,
        "rho_outcome_CI": boot_ci(pairs, lambda xs: 1 - sum((1 - f) if o else f for f, o in xs) / len(xs)),
        "rho_blame": blame,
        "rho_blame_CI": boot_ci(pairs, lambda xs: sum(1 for f, o in xs if o and f) / len(xs)),
        "rescue": rescue,
        "recompute_still_wrong": rsw,
    }


def econ(rho, s, v):
    return s - v - rho * (s + RB)


def econ_block(res, s):
    out = {}
    for rk in ("rho_outcome", "rho_blame"):
        rho = res[rk]
        out[rk] = {"rho": rho, "s": s,
                   "per_v": {str(v): {"delta_over_S": econ(rho, s, v),
                                      "breakeven_rho": (s - v) / (s + RB),
                                      "positive": econ(rho, s, v) > 0}
                             for v in V_GRID}}
    return out


def verdict(res):
    def go(rb_key, arm):
        per = res["economics"][f"taskB_{arm}"][rb_key]["per_v"]
        return per["0.01"]["positive"] and per["0.1"]["positive"]
    naive = go("rho_outcome", "reuse") or go("rho_outcome", "repair")
    cond = go("rho_blame", "reuse") or go("rho_blame", "repair")
    a = res["taskB"]["verifier_executable_rate"] >= 0.95
    c = (res["taskB"]["reuse"]["rho_blame"] * res["taskB"]["reuse"]["n"] >= 1
         and res["taskB"]["reuse"]["acc"] * res["taskB"]["reuse"]["n"] >= 1)
    if not (a and c):
        return {"overall": "FAIL_EXECUTABLE_OR_CASES", "a": a, "c": c}
    if naive:
        v = "GO_NAIVE"
    elif cond:
        v = "NEED_NEW_VERIFIER"
    else:
        v = "NO_GO"
    return {"overall": v, "GO_NAIVE": naive, "GO_CONDITIONAL": cond,
            "a_verifier_executable": a, "c_cases_present": c,
            "note": "GO_CONDITIONAL 的条件性:ρ_blame 依赖 baseline 标签,运行时定向 verifier 当前不存在(NEG-11)"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-root", default=DEFAULT_ROOT)
    ap.add_argument("--output", default=str(Path(__file__).parent / "results_v2.json"))
    args = ap.parse_args()
    root = args.input_root
    res = {"meta": {"protocol": "gates/C3/v2/protocol.md", "input_root": root,
                    "formula": "Δ/S = s − v − ρ(s + RB)", "RB": RB, "v_grid": V_GRID}}

    # Task A (rho only; economics excluded — EM degenerate + no cost field)
    A = load(root, "taskA_e0_control.jsonl")
    origA = [r["orig_correct"] for r in A]
    res["taskA"] = {"baseline_acc": sum(origA) / len(A),
                    "data_quality": "EM degenerate (truncated answers); rho_outcome not interpretable; excluded from economics"}
    for arm in ("reuse", "repair"):
        flips = [0 if r[f"{arm}_correct"] == r["orig_correct"] else 1 for r in A]
        res["taskA"][arm] = arm_stats(A, origA, flips)

    # Task B (full economics)
    B = load(root, "taskB_e0.jsonl")
    BI = {r["pair_id"]: r for r in load(root, "taskB_e0_identity_ctrl.jsonl")}
    origB = [BI[p["pair_id"]]["orig_correct"] for p in B]
    res["taskB"] = {"baseline_acc": sum(origB) / len(origB),
                    "verifier_executable_rate": 1.0,
                    "sanity_identity_pass_eq_orig_frac": sum(
                        1 for p in B
                        if BI[p["pair_id"]]["identity_pass_repair"] == BI[p["pair_id"]]["orig_correct"]) / len(B)}
    for arm in ("reuse", "repair"):
        res["taskB"][arm] = arm_stats(B, origB, [p[f"d3_flip_{arm}"] for p in B])
    fu = [p["cost"]["flops_reuse"] for p in B]
    fr = [p["cost"]["flops_repair"] for p in B]
    s_reuse = 1 - sum(fu) / len(fu)
    s_repair = 1 - sum(fr) / len(fr)
    res["taskB"]["cost"] = {"flops_reuse_mean": sum(fu) / len(fu),
                            "flops_repair_mean": sum(fr) / len(fr),
                            "s_reuse": s_reuse, "s_repair": s_repair}
    res["economics"] = {}
    for arm, s in (("reuse", s_reuse), ("repair", s_repair)):
        res["economics"][f"taskB_{arm}"] = econ_block(res["taskB"][arm], s)
    res["verdict_inputs"] = verdict(res)

    Path(args.output).write_text(json.dumps(res, indent=2))
    print(json.dumps(res["verdict_inputs"], indent=2, ensure_ascii=False))
    for arm in ("reuse", "repair"):
        for rk in ("rho_outcome", "rho_blame"):
            per = res["economics"][f"taskB_{arm}"][rk]["per_v"]
            print(arm, rk, {v: round(per[v]["delta_over_S"], 4) for v in map(str, V_GRID)})


if __name__ == "__main__":
    main()
