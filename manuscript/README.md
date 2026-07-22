# AAAI-27 Manuscript

The authoritative submission metadata is in
`docs/AAAI27_ABSTRACT_SUBMISSION.md`. The main anonymous paper is `main.tex`;
its bibliography is `references.bib`. Official AAAI-27 style assets are pinned
by `AUTHOR_KIT_MANIFEST.md`.

Compile from this directory after the TeX dependencies are installed:

```bash
python3 figures/make_economics_figure.py
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=build main.tex
bibtex build/main
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=build main.tex
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=build main.tex
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=build reproducibility_checklist.tex
python3 check_manuscript.py
```

Build products belong in `build/` during automated checks and are not tracked.
The submission PDF must be US Letter, at most nine pages, with references only
on pages eight and nine, embedded non-Type-3 fonts, and no identifying PDF
metadata.

`ReproducibilityChecklist.tex` is the immutable official template;
`reproducibility_checklist.tex` is the completed standalone submission copy.
Upload only its compiled PDF in the separate checklist field; do not append it
to the main paper or place either checklist source in the Code/Data Supplement.
`CHECKLIST_SUBMISSION.md` records the official disposition.

The optional anonymous Code/Data Supplement is built from an explicit
allowlist:

```bash
python3 supplement/build_anonymous_supplement.py
python3 supplement/test_supplement.py
```

Do not upload a repository archive. The generated ZIP excludes internal
handoffs, Git metadata, local paths, submission metadata, and unavailable raw
aggregate inputs. `BUILD_REPORT.md` records the final Stage 2.5 checks, and
`FIGURE_MANIFEST.json` binds Figure 2 to its committed machine-readable input.

No model, GPU, trajectory-generation, cache/replay, or mutation experiment is
authorized by this manuscript directory.
