#!/usr/bin/env python3
"""Focused tests for the C6 gate, runnable from a clean clone (fixtures only).

Full-data results live in results.json / results_doc_level.json (committed);
these tests re-run the analysis on gates/C6/fixtures/ into a temp file and
assert structural properties only (no absolute-path inputs, no direction-locking
assertions on descriptive flip rates).
"""
import json, subprocess, sys, tempfile
from pathlib import Path

D = Path(__file__).parent
FIX = D / "fixtures"


def run(script, *args):
    subprocess.run([sys.executable, str(D / script), *args],
                   check=True, capture_output=True)


def doc_results():
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
        out = tf.name
    run("analyse_doc_level.py", "--input-root", str(FIX), "--output", out)
    return json.loads(Path(out).read_text())


def sentence_results():
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
        out = tf.name
    run("analyse_workflow.py", "--input", str(FIX / "taskA_e0.jsonl"), "--output", out)
    return json.loads(Path(out).read_text())


DOC = doc_results()
SENT = sentence_results()


def test_counts_consistent():
    m = DOC["mutation_sim_doc_level"]
    assert m["n_mutations"] == DOC["artifacts"]["doc_total"] > 0
    assert m["exact_invalidations"] == 3 * m["n_mutations"]
    assert m["query_relative_invalidations"] <= m["exact_invalidations"]


def test_ratios_in_unit_interval():
    assert 0.0 <= DOC["incidence"]["citation_rate"] <= 1.0
    for k in ("docs_cited_ge2_frac", "docs_cited_ge1_frac", "docs_dead_frac"):
        assert 0.0 <= DOC["multi_consumer"][k] <= 1.0
    assert 0.0 <= DOC["mutation_sim_doc_level"]["cost_reduction"] <= 1.0


def test_exact_fields_separated():
    # NEG-19 discipline: exact and query-relative are separate fields
    m = DOC["mutation_sim_doc_level"]
    for k in ("exact_invalidations", "query_relative_invalidations",
              "exact_cost", "qr_cost"):
        assert k in m


def test_sentence_level_runs_and_records_usage():
    ur = SENT["used_region"]
    assert "substring" in ur and "all" in ur["substring"]
    assert 0.0 <= ur["substring"]["all"]["frac_zero_use"] <= 1.0


def test_validation_recorded_rates_bounded():
    v = DOC["validation_vs_real_flips"]
    for k in ("cited", "not_cited"):
        rate = v[k]["real_flip_repair_rate"]
        assert rate is None or 0.0 <= rate <= 1.0
    assert v["cited"]["n"] + v["not_cited"]["n"] == v["n_pairs"]


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print("PASS", fn.__name__)
    print(f"{len(fns)} tests passed")
