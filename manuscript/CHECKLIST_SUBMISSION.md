# AAAI-27 Checklist and Supplement Disposition

Verified against the official AAAI-27 submission instructions and author kit
on 2026-07-22.

## Reproducibility checklist

- `ReproducibilityChecklist.tex` is the immutable official author-kit
  template. Its SHA-256 remains
  `06a3459158089bf1c64b738986118f1d1566e816da4b710c6397561e33c3d5e6`.
- `reproducibility_checklist.tex` is the completed submission source. All 31
  response slots are filled with allowed values. The official questions,
  ordering, and commands are unchanged.
- Compile the completed lower-case source as a standalone PDF and upload only
  that PDF in OpenReview's designated reproducibility-checklist field.
- Do not append the checklist to `main.pdf`. Do not upload the blank template,
  either TeX source, or checklist auxiliaries in the Code/Data Supplement.

The two source files intentionally coexist: one pins the official form, and
the other is the completed response artifact. Neither should be deleted.

Official rule:
<https://aaai.org/conference/aaai/aaai-27/submission-instructions/#reproducibility-guidelines>

## Optional supplementary material

The code/data archive is
`supplement/aaai27_code_data_supplement.zip`. It is a deterministic allowlist
package, not a repository archive. It excludes Git metadata, internal handoffs,
the OpenReview number, local paths, repository-owner strings, author metadata,
and both checklist TeX files. Its manifest and test record the anonymity scan.

AAAI-27 treats the optional supplementary document and Code/Data archive as
separate uploads. The conference page states a July 31, 2026 AoE supplementary
deadline and requires anonymity and no external web pointers inside the
submission artifact:
<https://aaai.org/conference/aaai/aaai-27/supplementary-material/>.
