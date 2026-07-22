# Formal Stage 2.5 Integrity Review

**STATUS: PASS WITH NOTES — MANDATORY CHECKPOINT**

Date: 2026-07-22

This review used the committed paper and raw evidence as inputs, not the
manuscript's own conclusions. One correction round was used; the protocol
allows at most three. No model experiment, GPU run, new agent trajectory,
mutation treatment, or cache/reuse execution was performed.

## Phase A — Citation integrity

All 21 current citation contexts resolve to 21 bibliography entries and were
checked against primary records. Six load-bearing 2025--2026 sources received
full mechanism/status checks. Corrections updated AgentTrace v4 metadata,
AgentReuse journal metadata, AutoGen's title, exact AutoGen/SWE-agent repository
bindings, Agent Workflow Memory wording, and HumanEvalPack label attribution.

Sherlock remains an arXiv v1 preprint on the available primary records. Its
public mechanism is within-run verification/speculation/rollback, not cross-run
historical-artifact caching. The C3 scoop-check re-review trigger is not met.

Detailed artifacts: `CITATION_AUDIT.md`, `CITATION_AUDIT.json`.

## Phase B — Claim and raw-result integrity

The independent raw recount reproduced the economics, audit, and D0 claims but
found three Table 1 unit problems:

1. 6/8 refers to next assistant-response text, while parsed next-command
   disagreement is 4/8.
2. 4,968 is the frozen registered block--agent population, including 1,092
   retriever-side cite/document incidences. The downstream sensitivity has
   3,876 incidences; both versions remain degenerate.
3. The legacy citation helper mixed 237 non-document rows into `not_cited` and
   failed on 105 nested-title rows. The corrected document-only result is
   61 mentioned/0 flips and 702 unmentioned/36 flips, versus 35
   identity-control flips on those same 702 pairs.

The manuscript and machine-readable recount now use the corrected semantics.
The frozen historical C6 code/results remain untouched. None of these changes
alters `TEXT_USAGE_PROXY = INVALID`, `C6_STRONG_TESTBED = NOT_FOUND`, or
`C3 = NEED_NEW_VERIFIER`.

Detailed artifacts: `PAPER_CLAIM_AUDIT.md`, `PAPER_CLAIM_AUDIT.json`, and
`stage2_5/descriptive_counts.json`.

## Phase C — Reproducibility, package, and anonymity

The optional Code/Data Supplement now exists and is tracked:

- archive: `supplement/aaai27_code_data_supplement.zip`;
- SHA-256: `d73c6fa6949e70c3f5a97c19f163247bf2190ed990b422a563f78fdbd5e3629d`;
- size: 76,847 bytes;
- members: 32;
- deterministic rebuild: PASS;
- archive hash/member verification: PASS;
- forbidden identity/path/email scan: PASS;
- extracted focused tests: 6 C3 + 5 C6 + 6 selective-audit + 3 D0 + 1
  Stage 2.5 parser test passed; the full recount test correctly skips unless
  external SHA-matching roots are supplied.

The archive is intentionally not a clean-clone substitute for full aggregate
reproduction. External raw inputs remain enumerated by hash. The D0 source
manifest now also binds the host-side sandbox implementation and the resolved
HumanEvalPack revision `9a41762f73a8cb23bb5811b73d5aab164efcf378`.

The main paper and completed checklist PDFs are anonymous. The official blank
checklist is preserved; the completed checklist is a separate standalone
upload, not appended to the paper. See `CHECKLIST_SUBMISSION.md`.

## Phase D — Originality screen

Sixteen of approximately 45 prose paragraphs (35.6%) were sampled with quoted
searches. No meaningful exact match was found. Author-specific self-overlap was
not run because author identity was not provided to the anonymous reviewer.
See `ORIGINALITY_AUDIT.md`.

## Phase E — Seven failure modes

| Failure mode | Final assessment | Evidence |
|---|---|---|
| 1. Implementation bug | CLEAR AFTER CORRECTION | denominator/parser/unit bugs were found in correction round 1, fixed only in new Stage 2.5 analysis, and regression-tested |
| 2. Citation hallucination | CLEAR AFTER CORRECTION | all 21 keys verified; stale metadata and source bindings corrected |
| 3. Hallucinated experimental result | CLEAR | displayed quantitative claims bind to raw hashes and independent recounts |
| 4. Shortcut reliance | CLEAR | final-text proxies are reported as invalid measurements, not method success |
| 5. Bug reframed as insight | CLEAR AFTER CORRECTION | the corrected denominators retain the same bounded proxy-failure verdict; old frozen outputs are labeled legacy rather than promoted |
| 6. Methodology fabrication | CLEAR | protocol/code/results/version history and D0/static boundaries are explicit; no new model experiment is claimed |
| 7. Frame lock | CLEAR | negative gates changed the paper route to measurement/methodology; rejected C4 and ineligible D0 routes were not revived |

## Notes that remain

- Full aggregate raw inputs are not all distributable from the anonymous
  supplement; hash-only entries cannot provide independent reproduction to a
  reviewer who lacks those files.
- The generic workflow's preferred cross-model MCP reviewer was unavailable.
  A fresh zero-context independent subagent and direct coordinating-agent
  checks were used instead.
- The Q rubric still lacks independent inter-rater validation.
- The originality screen is bounded and author-specific self-overlap remains
  untested under anonymity.

## Gate decision

Stage 2.5 is complete with the notes above. The paper is eligible to proceed to
the next writing/review stage only after the responsible owner accepts this
checkpoint. Experiment authorization remains `NONE`.
