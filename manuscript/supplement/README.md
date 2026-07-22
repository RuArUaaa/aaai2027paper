# Anonymous Code and Data Supplement

This directory builds the optional anonymous Code and Data Supplement for the
paper.  It is deliberately an allowlist package, not an archive of the Git
repository.  The generated archive contains analysis code, focused fixtures,
machine-readable results, and SHA-256 ledgers; it excludes internal handoffs,
submission metadata, version-control history, build logs, and local paths.

## Submission artifacts

The AAAI-27 uploads are separate:

1. the main paper PDF;
2. the completed reproducibility-checklist PDF;
3. the optional `aaai27_code_data_supplement.zip` built here.

The official blank checklist source is retained for provenance but is not
included in the supplement.  The completed checklist is compiled from
`manuscript/reproducibility_checklist.tex` and uploaded in the designated
checklist field, not appended to the paper and not placed in this ZIP.

## Reproducibility boundary

The archive can reproduce focused parser paths, fixture-level tests, static
invariants, the committed selective-consumption audit, and arithmetic that
does not require the historical raw repositories.  It cannot reproduce every
aggregate in the paper by itself.  External aggregate inputs are not
redistributed; `EXTERNAL_INPUTS.json` records their logical identities,
byte sizes where known, and SHA-256 digests.  A hash can authenticate a file
already possessed by a reviewer, but cannot substitute for distributing it.

The Stage 2.5 recount also records two semantic corrections without changing
the paper's scientific verdict:

- the diff diagnostic distinguishes next assistant-response text (6/8) from
  the parsed next command (4/8);
- the citation diagnostic is restricted to 763 document pairs and uses a
  balanced-parentheses title parser (61 mentioned/0 flips versus 702
  unmentioned/36 flips, with 35 identity-control flips on the same 702 pairs).

The registered overlap population remains 4,968 non-system block--agent
incidences.  A generation-aligned sensitivity excluding 1,092 retriever-side
citation/document incidences has 3,876 downstream incidences; both definitions
retain zero median and 90th-percentile usage under the invalid text proxies.

## Build and verify

From the repository root:

```bash
python3 manuscript/supplement/build_anonymous_supplement.py
python3 manuscript/supplement/test_supplement.py
```

The builder uses deterministic member order, timestamps, permissions, and
compression settings.  It rejects the package if forbidden identity strings,
absolute home paths, the submission number, email addresses, or unsafe ZIP
member paths are detected.  The test builds twice in temporary directories,
checks byte identity, unpacks the archive, and verifies every member hash.

The generated artifacts are:

- `manuscript/supplement/aaai27_code_data_supplement.zip`;
- `manuscript/supplement/SUPPLEMENT_MANIFEST.json`.

No model, GPU, trajectory generation, mutation treatment, or cache/reuse
experiment is executed by the builder or tests.
