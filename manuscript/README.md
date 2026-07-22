# AAAI-27 Manuscript

The authoritative submission metadata is in
`docs/AAAI27_ABSTRACT_SUBMISSION.md`. The main anonymous paper is `main.tex`;
its bibliography is `references.bib`. Official AAAI-27 style assets are pinned
by `AUTHOR_KIT_MANIFEST.md`.

Compile from this directory after the TeX dependencies are installed:

```bash
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error main.tex
```

Build products belong in `build/` during automated checks and are not tracked.
The submission PDF must be US Letter, at most nine pages, with references only
on pages eight and nine, embedded non-Type-3 fonts, and no identifying PDF
metadata.

No model, GPU, trajectory-generation, cache/replay, or mutation experiment is
authorized by this manuscript directory.

