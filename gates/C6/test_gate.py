#!/usr/bin/env python3
"""Focused tests for the C6 revised gate (stdlib only)."""
import json, subprocess, sys
from pathlib import Path

D = Path(__file__).parent


def setup():
    subprocess.run([sys.executable, str(D / "analyse_doc_level.py")],
                   check=True, capture_output=True)
    return json.loads((D / "results_doc_level.json").read_text()), \
           json.loads((D / "results.json").read_text())


DOC, MERGED = setup()


def test_counts_consistent():
    assert DOC["artifacts"]["doc_total"] == 992
    m = DOC["mutation_sim_doc_level"]
    assert m["exact_invalidations"] == 3 * m["n_mutations"]
    assert m["query_relative_invalidations"] <= m["exact_invalidations"]


def test_ratios_in_unit_interval():
    for k in ("citation_rate",):
        assert 0.0 <= DOC["incidence"][k] <= 1.0
    for k in ("docs_cited_ge2_frac", "docs_cited_ge1_frac", "docs_dead_frac"):
        assert 0.0 <= DOC["multi_consumer"][k] <= 1.0
    assert 0.0 <= DOC["mutation_sim_doc_level"]["cost_reduction"] <= 1.0


def test_exact_fields_separated():
    # NEG-19 discipline: exact and query-relative are separate fields
    m = DOC["mutation_sim_doc_level"]
    for k in ("exact_invalidations", "query_relative_invalidations",
              "exact_cost", "qr_cost"):
        assert k in m


def test_sentence_level_degenerate_documented():
    ur = MERGED["sentence_level"]["used_region"]["substring"]["all"]
    assert ur["median"] == 0.0 and ur["frac_zero_use"] > 0.9


def test_validation_recorded():
    v = DOC["validation_vs_real_flips"]
    assert v["cited"]["n"] + v["not_cited"]["n"] == 1000
    # the chair verdict depends on this: citation does NOT show elevated flip rate
    assert v["cited"]["real_flip_repair_rate"] <= v["not_cited"]["real_flip_repair_rate"]


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print("PASS", fn.__name__)
    print(f"{len(fns)} tests passed")
