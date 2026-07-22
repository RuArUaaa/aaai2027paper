#!/usr/bin/env python3
"""C3 gate v2.1 analysis correction; v2 evidence remains frozen.

The economic value is normalized by the complete baseline execution cost:

    Δ/C_full = s - v - rho * (s + RB), where C_full = 1.

Usage:
    python3 reanalyse_v2_1.py [--input-root DIR] [--output FILE]

The default input is the read-only historical evidence repository. For a clean
clone or focused test, point --input-root at gates/C3/fixtures and --output at a
temporary path.
"""

import argparse
import json
import random
from pathlib import Path


RB = 0.01
V_GRID = (0.001, 0.01, 0.1)
DEFAULT_ROOT = "/Users/zijian_nong/research/aaai2027/runs/pairs"


def load(root, name):
    path = Path(root) / name
    return [json.loads(line) for line in path.open() if line.strip()]


def boot_ci(vals, stat, n=2000, seed=1):
    rnd = random.Random(seed)
    size = len(vals)
    stats = sorted(
        stat([vals[rnd.randrange(size)] for _ in range(size)])
        for _ in range(n)
    )
    return [stats[int(0.025 * n)], stats[int(0.975 * n)]]


def arm_stats(rows, orig_flags, flips):
    """Return arm statistics under the historical flip encoding.

    flips[i] is 1 exactly when the arm result differs from the from-scratch
    result. Therefore, for an originally wrong case, flip=1 is a rescue and
    flip=0 means the arm remains wrong.
    """
    n = len(rows)
    if n == 0 or len(orig_flags) != n or len(flips) != n:
        raise ValueError("rows, orig_flags, and flips must have equal non-zero lengths")
    if any(flip not in (0, 1, False, True) for flip in flips):
        raise ValueError("flip values must be binary")
    passes = [(1 - flip) if orig else flip for flip, orig in zip(flips, orig_flags)]
    acc = sum(passes) / n
    blame = sum(
        1 for flip, orig in zip(flips, orig_flags) if orig and flip
    ) / n
    rescue = sum(
        1 for flip, orig in zip(flips, orig_flags) if (not orig) and flip
    ) / n
    # Corrected in v2.1: rejected arm AND from-scratch recomputation is wrong.
    # Under this encoding, orig_wrong AND arm_wrong is (not orig) and (not flip).
    recompute_still_wrong = sum(
        1 for flip, orig in zip(flips, orig_flags)
        if (not orig) and (not flip)
    ) / n
    pairs = list(zip(flips, orig_flags))
    return {
        "n": n,
        "acc": acc,
        "rho_outcome": 1 - acc,
        "rho_outcome_CI": boot_ci(
            pairs,
            lambda xs: 1
            - sum((1 - flip) if orig else flip for flip, orig in xs) / len(xs),
        ),
        "rho_blame": blame,
        "rho_blame_CI": boot_ci(
            pairs,
            lambda xs: sum(1 for flip, orig in xs if orig and flip) / len(xs),
        ),
        "rescue": rescue,
        "recompute_still_wrong": recompute_still_wrong,
    }


def net_saving_fraction_of_full_run(rho, s, v):
    """Return Δ/C_full with C_full normalized to 1."""
    return s - v - rho * (s + RB)


def economics_block(arm_result, s):
    out = {}
    for rho_key in ("rho_outcome", "rho_blame"):
        rho = arm_result[rho_key]
        per_v = {}
        for v in V_GRID:
            saving = net_saving_fraction_of_full_run(rho, s, v)
            per_v[str(v)] = {
                "delta_over_full": saving,
                "breakeven_rho": (s - v) / (s + RB),
                "positive": saving > 0,
            }
        out[rho_key] = {
            "rho": rho,
            "s": s,
            "metric": "net_saving_fraction_of_full_run",
            "per_v": per_v,
        }
    return out


def verdict(results):
    def go(rho_key, arm):
        per_v = results["economics"][f"taskB_{arm}"][rho_key]["per_v"]
        return per_v["0.01"]["positive"] and per_v["0.1"]["positive"]

    naive = go("rho_outcome", "reuse") or go("rho_outcome", "repair")
    conditional = go("rho_blame", "reuse") or go("rho_blame", "repair")
    executable = results["taskB"]["verifier_executable_rate"] >= 0.95
    cases_present = (
        results["taskB"]["reuse"]["rho_blame"]
        * results["taskB"]["reuse"]["n"]
        >= 1
        and results["taskB"]["reuse"]["acc"]
        * results["taskB"]["reuse"]["n"]
        >= 1
    )
    if not (executable and cases_present):
        return {
            "overall": "FAIL_EXECUTABLE_OR_CASES",
            "a": executable,
            "c": cases_present,
        }
    if naive:
        overall = "GO_NAIVE"
    elif conditional:
        overall = "NEED_NEW_VERIFIER"
    else:
        overall = "NO_GO"
    return {
        "overall": overall,
        "GO_NAIVE": naive,
        "GO_CONDITIONAL": conditional,
        "a_verifier_executable": executable,
        "c_cases_present": cases_present,
        "note": (
            "GO_CONDITIONAL 的条件性:rho_blame 依赖 baseline 标签,"
            "运行时定向 verifier 当前不存在(NEG-11)"
        ),
    }


def analyse(input_root):
    results = {
        "meta": {
            "protocol": "gates/C3/v2/protocol.md",
            "correction": "gates/C3/v2_1/analysis_correction.md",
            "input_root": str(input_root),
            "formula": "Δ/C_full = s - v - rho(s + RB)",
            "C_full": 1.0,
            "v_semantics": "verifier_cost_fraction_of_full_run",
            "economic_metric": "net_saving_fraction_of_full_run",
            "RB": RB,
            "v_grid": V_GRID,
        }
    }

    task_a = load(input_root, "taskA_e0_control.jsonl")
    orig_a = [row["orig_correct"] for row in task_a]
    results["taskA"] = {
        "baseline_acc": sum(orig_a) / len(task_a),
        "data_quality": (
            "EM degenerate (truncated answers); rho_outcome not interpretable; "
            "excluded from economics"
        ),
    }
    for arm in ("reuse", "repair"):
        flips = [
            0 if row[f"{arm}_correct"] == row["orig_correct"] else 1
            for row in task_a
        ]
        results["taskA"][arm] = arm_stats(task_a, orig_a, flips)

    task_b = load(input_root, "taskB_e0.jsonl")
    identity = {
        row["pair_id"]: row
        for row in load(input_root, "taskB_e0_identity_ctrl.jsonl")
    }
    orig_b = [identity[row["pair_id"]]["orig_correct"] for row in task_b]
    results["taskB"] = {
        "baseline_acc": sum(orig_b) / len(orig_b),
        "verifier_executable_rate": 1.0,
        "sanity_identity_pass_eq_orig_frac": sum(
            1
            for row in task_b
            if identity[row["pair_id"]]["identity_pass_repair"]
            == identity[row["pair_id"]]["orig_correct"]
        )
        / len(task_b),
    }
    for arm in ("reuse", "repair"):
        results["taskB"][arm] = arm_stats(
            task_b,
            orig_b,
            [row[f"d3_flip_{arm}"] for row in task_b],
        )

    flops_reuse = [row["cost"]["flops_reuse"] for row in task_b]
    flops_repair = [row["cost"]["flops_repair"] for row in task_b]
    s_reuse = 1 - sum(flops_reuse) / len(flops_reuse)
    s_repair = 1 - sum(flops_repair) / len(flops_repair)
    results["taskB"]["cost"] = {
        "flops_reuse_mean": sum(flops_reuse) / len(flops_reuse),
        "flops_repair_mean": sum(flops_repair) / len(flops_repair),
        "s_reuse": s_reuse,
        "s_repair": s_repair,
    }
    results["economics"] = {
        "taskB_reuse": economics_block(results["taskB"]["reuse"], s_reuse),
        "taskB_repair": economics_block(results["taskB"]["repair"], s_repair),
    }
    results["verdict_inputs"] = verdict(results)
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-root", default=DEFAULT_ROOT)
    parser.add_argument(
        "--output", default=str(Path(__file__).parent / "results_v2_1.json")
    )
    args = parser.parse_args()
    results = analyse(args.input_root)
    Path(args.output).write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results["verdict_inputs"], indent=2, ensure_ascii=False))
    for arm in ("reuse", "repair"):
        for rho_key in ("rho_outcome", "rho_blame"):
            per_v = results["economics"][f"taskB_{arm}"][rho_key]["per_v"]
            print(
                arm,
                rho_key,
                {v: round(per_v[v]["delta_over_full"], 4) for v in map(str, V_GRID)},
            )


if __name__ == "__main__":
    main()
