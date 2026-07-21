#!/usr/bin/env python3
"""Deterministic merge of C6 sentence-level and doc-level analyses into results.json.

Replaces the manual merge recorded in v1. Usage:
    python3 merge_results.py [--root /Users/zijian_nong/research/aaai2027/runs]
"""
import argparse, json, subprocess, sys
from pathlib import Path

D = Path(__file__).parent
DEFAULT_ROOT = "/Users/zijian_nong/research/aaai2027/runs"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=DEFAULT_ROOT,
                    help="runs dir with traces/ and pairs/, or a fixtures dir")
    ap.add_argument("--output", default=str(D / "results.json"))
    args = ap.parse_args()
    root = Path(args.root)
    trace = root / "traces/taskA_e0.jsonl"
    if not trace.exists():
        trace = root / "taskA_e0.jsonl"   # fixture layout

    subprocess.run([sys.executable, str(D / "analyse_workflow.py"),
                    "--input", str(trace),
                    "--output", str(D / "results_sentence_level.json")], check=True)
    subprocess.run([sys.executable, str(D / "analyse_doc_level.py"),
                    "--input-root", str(root),
                    "--output", str(D / "results_doc_level.json")], check=True)

    merged = {
        "meta": {"note": "deterministic merge via merge_results.py (P1)",
                 "root": str(root)},
        "sentence_level": json.loads((D / "results_sentence_level.json").read_text()),
        "doc_level_citation": json.loads((D / "results_doc_level.json").read_text()),
    }
    Path(args.output).write_text(json.dumps(merged, indent=2, ensure_ascii=False))
    print("merged ->", args.output)


if __name__ == "__main__":
    main()
