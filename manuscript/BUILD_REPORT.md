# Stage 2.5 Manuscript Build and Integrity Report

Date: 2026-07-22

OpenReview submission number: **44503**

Status: **STAGE 2.5 COMPLETE — PASS WITH NOTES; OWNER CHECKPOINT REQUIRED**

## Locked submission metadata

- Title and abstract match `docs/AAAI27_ABSTRACT_SUBMISSION.md` under the
  manuscript checker's whitespace/typesetting normalization.
- The paper is anonymous and uses the unmodified official AAAI-27 style and
  bibliography files recorded in `AUTHOR_KIT_MANIFEST.md`.
- Submission mode remains `submission`; author and affiliation metadata are
  absent.

## Build commands

Run from `manuscript/`:

```bash
python3 figures/make_economics_figure.py
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=build main.tex
bibtex build/main
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=build main.tex
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=build main.tex
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=build reproducibility_checklist.tex
python3 check_manuscript.py
```

The local minimal TeX Live installation required `newtx`, `placeins`,
`xstring`, `mweights`, `fontaxes`, `kastrup`, `courier`, and `tex-gyre`.

## Verified outputs

| Property | Result |
|---|---|
| Main paper | 8 pages total; pages 1--7 content; page 8 references only |
| Page geometry | US Letter |
| Bibliography | 21 cited keys; all resolved and checked against primary records |
| Fonts | embedded; no Type 3 fonts |
| Figure 2 | 1995 x 640 RGB PNG; embedded at 300 x 300 ppi |
| Figure contrast | minimum recorded white-background ratio 5.185:1 |
| Layout diagnostics | no overfull box; no undefined citation/reference |
| Checklist | 31/31 applicable response slots filled; 2-page standalone PDF; separate OpenReview upload |
| Abstract/title lock | PASS |
| Local-path/identity leakage | none detected in PDF text/metadata |

Generated PDFs remain ignored build products. Their verified local hashes were:

- `build/main.pdf`:
  `c80e67e694e448a1b4aa3a2a2002c969059cf3dd2df72bdbfa69eb9fe235bb68`.
- `build/reproducibility_checklist.pdf`:
  `d3a68508bc0e0eaabcb654c32944ed3e744f840d2f259dee22014fc5d782cba5`.

Regenerate both from the committed sources for any submission package rather
than treating ignored local build products as release artifacts.

## Stage 2.5 integrity gate

One correction round was used. The primary-source citation audit, independent
raw recount, claim audit, bounded originality screen, package/anonymity test,
and seven-failure-mode review are recorded in:

- `CITATION_AUDIT.md` and `CITATION_AUDIT.json`;
- `PAPER_CLAIM_AUDIT.md` and `PAPER_CLAIM_AUDIT.json`;
- `ORIGINALITY_AUDIT.md`;
- `STAGE2_5_INTEGRITY_REVIEW.md`;
- `stage2_5/descriptive_counts.json` and its tested recomputation script.

The recount distinguishes 6/8 next-response differences from 4/8 parsed
next-command differences, records 4,968 registered block--agent incidences and
the 3,876-incidence downstream sensitivity, and replaces the legacy mixed-row
citation diagnostic with a 763-document-pair estimand. These corrections do
not change the C3 or C6 verdicts.

## Supplement and checklist disposition

The tracked optional Code/Data Supplement is
`supplement/aaai27_code_data_supplement.zip`:

- SHA-256:
  `d73c6fa6949e70c3f5a97c19f163247bf2190ed990b422a563f78fdbd5e3629d`;
- size: 76,847 bytes;
- members: 32;
- deterministic rebuild and per-member hash verification: PASS;
- forbidden identity/path/email and unsafe-member scan: PASS;
- extracted focused tests: 6 C3 + 5 C6 + 6 selective-audit + 3 D0 + 1
  Stage 2.5 parser test: PASS.

`ReproducibilityChecklist.tex` is the immutable blank author-kit source;
`reproducibility_checklist.tex` is the completed source. Only the completed
standalone PDF is uploaded in OpenReview's checklist field. Neither source is
included in the supplement. See `CHECKLIST_SUBMISSION.md`.

## Scientific and reproducibility boundary

The manuscript introduces no new model result. Its numerical claims come from
committed machine-readable results or frozen evidence enumerated by SHA-256.
Clean-clone fixtures reproduce parsers and invariants, not every aggregate.
Several aggregate raw inputs remain separately preserved external artifacts;
the paper and manifests disclose this limitation.

Stage 2.5 passed with disclosed limitations: the optional archive does not
redistribute every aggregate raw input, the Q rubric lacks independent
inter-rater validation, and the originality screen is bounded. No model, GPU,
new trajectory, cache/replay arm, or mutation experiment was run. Proceeding to
the next writing/review stage requires responsible-owner acceptance of this
checkpoint; experiment authorization remains `NONE`.
