#!/usr/bin/env python3
"""Export minimal gate fixtures from the frozen-evidence repo (P1 reproducibility).

Usage:
    python3 scripts/export_gate_inputs.py [--src-root /Users/zijian_nong/research/aaai2027] [--dest .]

Writes trimmed fixture files into gates/C3/fixtures/ and gates/C6/fixtures/.
Only the fields the gate scripts actually read are kept; token-id arrays are dropped.
Deterministic: fixed seed, explicit selection rules below.
"""
import argparse, hashlib, json, random
from pathlib import Path

SRC = Path("/Users/zijian_nong/research/aaai2027")
SEED = 20260721
N_TASKB_FIXTURE = 30          # all flip pairs + sampled non-flip
N_TASKA_CONTROL = 20
N_TASKA_TRACES = 2

# fields each script reads
TASKB_E0_FIELDS = ["pair_id", "trace_id", "d3_flip_reuse", "d3_flip_repair", "cost"]
TASKB_ID_FIELDS = ["pair_id", "orig_correct", "identity_pass_repair"]
TASKA_CTRL_FIELDS = ["trace_id", "orig_correct", "reuse_correct", "repair_correct"]


def load(p):
    return [json.loads(l) for l in p.open() if l.strip()]


def sha256(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def write_jsonl(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src-root", default=str(SRC))
    ap.add_argument("--dest", default=str(Path(__file__).resolve().parent.parent))
    args = ap.parse_args()
    src = Path(args.src_root)
    dest = Path(args.dest)
    rng = random.Random(SEED)

    manifest = {"source_repo": str(src), "files": []}

    # ---- C3 fixtures ----
    tb = load(src / "runs/pairs/taskB_e0.jsonl")
    tbi = {r["pair_id"]: r for r in load(src / "runs/pairs/taskB_e0_identity_ctrl.jsonl")}
    flip_ids = {p["pair_id"] for p in tb if p["d3_flip_reuse"] or p["d3_flip_repair"]}
    rest = [p["pair_id"] for p in tb if p["pair_id"] not in flip_ids]
    rng.shuffle(rest)
    keep = sorted(flip_ids | set(rest[: max(0, N_TASKB_FIXTURE - len(flip_ids))]))
    tb_out = [{k: p[k] for k in TASKB_E0_FIELDS if k in p} for p in tb if p["pair_id"] in keep]
    tbi_out = [{k: tbi[pid][k] for k in TASKB_ID_FIELDS if k in tbi[pid]} for pid in keep]
    write_jsonl(dest / "gates/C3/fixtures/taskB_e0.jsonl", tb_out)
    write_jsonl(dest / "gates/C3/fixtures/taskB_e0_identity_ctrl.jsonl", tbi_out)

    ctrl = load(src / "runs/pairs/taskA_e0_control.jsonl")
    rng.shuffle(ctrl)
    ctrl_out = [{k: r[k] for k in TASKA_CTRL_FIELDS if k in r} for r in ctrl[:N_TASKA_CONTROL]]
    write_jsonl(dest / "gates/C3/fixtures/taskA_e0_control.jsonl", ctrl_out)

    # ---- C6 fixtures ----
    traces = load(src / "runs/traces/taskA_e0.jsonl")
    keep_ids = {t["trace_id"] for t in traces[:N_TASKA_TRACES]}
    tr_out = []
    for t in traces[:N_TASKA_TRACES]:
        tr_out.append({
            "trace_id": t["trace_id"], "gold_answer": t["gold_answer"],
            "full_recompute_answer": t.get("full_recompute_answer"),
            "agents": [{"agent_id": a["agent_id"], "output_text": a["output_text"],
                        "output_len": a["output_len"],
                        "blocks": [{"block_id": b["block_id"], "text": b["text"],
                                    "span": b["span"]} for b in a["blocks"]]}
                       for a in t["agents"]],
        })
    write_jsonl(dest / "gates/C6/fixtures/taskA_e0.jsonl", tr_out)

    pairs = load(src / "runs/pairs/taskA_e0_identity_ctrl.jsonl")
    pairs_out = [p for p in pairs if p["trace_id"] in keep_ids]
    write_jsonl(dest / "gates/C6/fixtures/taskA_e0_identity_ctrl.jsonl", pairs_out)

    for rel in ("runs/pairs/taskA_e0_control.jsonl",
                "runs/pairs/taskA_e0_identity_ctrl.jsonl",
                "runs/pairs/taskB_e0.jsonl",
                "runs/pairs/taskB_e0_identity_ctrl.jsonl",
                "runs/traces/taskA_e0.jsonl"):
        p = src / rel
        manifest["files"].append({"relpath": rel, "bytes": p.stat().st_size,
                                  "sha256": sha256(p)})
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
