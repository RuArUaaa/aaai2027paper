# Stage 2 Manuscript Build Report

Date: 2026-07-22

OpenReview submission number: **44503**

Status: **STAGE 2 COMPLETE; FORMAL STAGE 2.5 NOT STARTED**

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
| Bibliography | 19 cited keys; all resolved |
| Fonts | embedded; no Type 3 fonts |
| Figure 2 | 1995 x 640 RGB PNG; embedded at 300 x 300 ppi |
| Figure contrast | minimum recorded white-background ratio 5.185:1 |
| Layout diagnostics | no overfull box; no undefined citation/reference |
| Checklist | 31/31 applicable response slots filled; 2-page standalone PDF |
| Abstract/title lock | PASS |
| Local-path/identity leakage | none detected in PDF text/metadata |

Generated PDFs remain ignored build products. Their verified local hashes were:

- `build/main.pdf`:
  `0b24abd514d82fcb247909271744c5bae817f6351f2517c2f7e6240230ad33bf`.
- `build/reproducibility_checklist.pdf`:
  `108ad8556493e804795cfa2de9856b514a385cd71c96dcf1558a3a2874e5f7e3`.

Regenerate both from the committed sources for any submission package rather
than treating ignored local build products as release artifacts.

## Scientific and reproducibility boundary

The manuscript introduces no new model result. Its numerical claims come from
committed machine-readable results or frozen evidence enumerated by SHA-256.
Clean-clone fixtures reproduce parsers and invariants, not every aggregate.
Several aggregate raw inputs remain separately preserved external artifacts;
the paper and manifests disclose this limitation.

The Stage 2 draft incorporates preliminary independent claim and format audits,
but these do not replace the mandatory zero-context Stage 2.5 integrity gate.
No model, GPU, new trajectory, cache/replay arm, or mutation experiment was run.
