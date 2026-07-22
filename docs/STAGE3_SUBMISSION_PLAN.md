# AAAI-27 Stage 3 Submission Plan

Status: **ACTIVE — SUBMISSION PREPARATION ONLY**

Authorized by the responsible owner on 2026-07-23 after acceptance of the
Stage 2.5 `PASS_WITH_NOTES` checkpoint.

OpenReview submission number: **44503**

## Purpose and hard boundary

This project-specific Stage 3 is a bounded submission-preparation stage. It is
not an experimental stage and does not authorize a new scientific review loop.
Its complete scope is:

1. preserve the paper assets on the remote repository;
2. conduct one overnight-separated cold read of the rendered PDF;
3. make only wording or layout corrections that leave every number and
   scientific claim unchanged;
4. validate and upload the main-paper PDF, completed-checklist PDF, and
   anonymous Code/Data Supplement ZIP;
5. archive the post-upload hashes and submission record.

The following remain forbidden: studied-system model/API calls, GPU use, new
agent trajectories, new experiments, ToolSandbox D0-bis, new testbed search,
new citations, changes to quantitative values, changes to scientific claims,
and changes to the frozen C3/C6/C4 verdicts. If a cold reader finds an issue
that cannot be corrected within the permitted wording/layout boundary, record
it and stop for owner adjudication; do not silently broaden Stage 3.

## Remote-backup checkpoint

- Local `main` before Stage 3: `e3867d7b929bbbd7491da2ba27031d7589a3a571`.
- GitHub `main` after push: `e3867d7b929bbbd7491da2ba27031d7589a3a571`.
- Push completed: 2026-07-23 (Asia/Shanghai), fast-forward only.
- The task-preexisting `.agents/`, `.claude/`, and `.codex/` directories
  remain untracked and were not pushed.

## Dates and stop points

AAAI states that the full paper is due July 28, 2026 at 23:59 UTC-12 and
supplementary material/code is due July 31, 2026 at 23:59 UTC-12. These are
July 29 at 19:59 and August 1 at 19:59 in Beijing, respectively.

The stricter internal plan is:

| Local date | Required action | Stop condition |
|---|---|---|
| 2026-07-23 | Remote backup and Stage 3 plan | Do not upload the full paper today |
| 2026-07-24 to 2026-07-25 | Cold-read the rendered PDF after an overnight break | Log findings before editing; escalate anything substantive |
| 2026-07-26 | Apply allowed wording/layout fixes, rebuild, and run all submission checks | Numbers, claims, title, and abstract remain locked |
| 2026-07-27 by 18:00 Asia/Shanghai | Upload all three artifacts and reopen the saved submission | Leaves at least 48 hours before the full-paper deadline |
| Immediately after upload | Download/reinspect submitted artifacts and archive hashes/record | Do not treat an upload click alone as confirmation |

Official sources:

- <https://aaai.org/conference/aaai/aaai-27/submission-instructions/>
- <https://aaai.org/conference/aaai/aaai-27/supplementary-material/>

## Cold-read protocol

The cold reader is read-only. The first pass is performed against
`manuscript/build/main.pdf`, not against the LaTeX source, and records every
finding in `manuscript/stage3/cold_read_report.md` before any edit.

Allowed dispositions:

- `WORDING_ONLY`: grammar, typo, punctuation, or local clarity repair with no
  semantic change;
- `LAYOUT_ONLY`: overflow, collision, spacing, line break, table/figure
  legibility, or reference-page presentation;
- `NO_CHANGE`: stylistic preference that does not justify touching the frozen
  draft;
- `ESCALATE`: would alter a number, claim, method, citation interpretation,
  result, limitation, title, abstract, or reproducibility boundary.

Only `WORDING_ONLY` and `LAYOUT_ONLY` may be applied. After any permitted edit,
the complete PDF is reread and the Stage 2.5 checks are rerun. An `ESCALATE`
item pauses submission preparation for owner review.

## Three upload artifacts: current baseline

Generated PDFs remain ignored build products and must be rebuilt from committed
sources before upload. The ZIP is tracked. These hashes identify the Stage 2.5
baseline, not yet the final upload record.

| OpenReview field | Local artifact | Bytes | Baseline SHA-256 |
|---|---|---:|---|
| Main paper | `manuscript/build/main.pdf` | 320,391 | `c80e67e694e448a1b4aa3a2a2002c969059cf3dd2df72bdbfa69eb9fe235bb68` |
| Reproducibility checklist | `manuscript/build/reproducibility_checklist.pdf` | 95,691 | `d3a68508bc0e0eaabcb654c32944ed3e744f840d2f259dee22014fc5d782cba5` |
| Code/Data Supplement | `manuscript/supplement/aaai27_code_data_supplement.zip` | 76,847 | `d73c6fa6949e70c3f5a97c19f163247bf2190ed990b422a563f78fdbd5e3629d` |

No separate Supplementary Document PDF is planned. The Code/Data Supplement
is an anonymous allowlist package and must not be replaced with a repository
archive.

## Final pre-upload gate

All items must pass on the exact bytes to be uploaded:

- title and abstract match `docs/AAAI27_ABSTRACT_SUBMISSION.md`;
- immediately before final save, the responsible submitter compares the
  displayed OpenReview title and abstract with that authoritative text;
- anonymous main PDF, US Letter, embedded non-Type-3 fonts, eight pages total,
  pages 1--7 content, page 8 references only;
- 21/21 citation keys resolved and no undefined references;
- completed checklist is a standalone two-page PDF and is not appended to the
  main paper;
- supplement deterministic-build, member-hash, safe-path, and anonymity tests
  pass;
- `git diff --check` passes and every intended source change is committed and
  pushed;
- the saved OpenReview submission is reopened after upload, and the uploaded
  files are downloaded or otherwise re-inspected before recording completion.

## Submission record

Use `docs/AAAI27_FULL_SUBMISSION_RECORD.md`. The record remains internal and is
excluded from the anonymous supplement. Do not record account emails, author
identities, credentials, cookies, or other private OpenReview metadata in the
repository.

## Experiment counters

```text
EXPERIMENT_AUTHORIZATION = NONE
MODEL_EXPERIMENT_CALLS = 0
GPU_RUNS = 0
NEW_AGENT_TRAJECTORIES = 0
LARGE_EXPERIMENTS = 0
```
