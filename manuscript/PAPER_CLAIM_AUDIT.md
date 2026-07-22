# Stage 2.5 Paper Claim Audit

Status: **PASS AFTER CORRECTION**

A fresh zero-context reviewer recomputed the displayed claims from the frozen
raw files rather than trusting the manuscript, gate verdicts, or derived JSON.
The coordinating reviewer then adjudicated every discrepancy against the
registered estimand and raw workflow schema.

## Corrections found by the recount

| Item | Legacy output | Correct manuscript unit | Final values | Verdict effect |
|---|---|---|---|---|
| Diff event | “next step” = 6/8 | next assistant response and parsed next command are distinct | response 6/8; command 4/8; suffix 8/8; exit 4/8; full invocation 0 | none |
| Overlap population | 4,968 described as producer--consumer edges | registered block--agent incidences, including 1,092 retriever-side cite/document incidences | registered 4,968 at 98.09%/95.69%; downstream sensitivity 3,876 at 97.70%/94.71%; medians/p90 zero | none |
| Citation population | 53/947 over “1,000 document pairs” | document-only sample plus balanced-title parsing | 61 mentioned/0 flips; 702 unmentioned/36 real and 35 identity flips | none; text proxy remains invalid |

The old citation helper assigned 237 non-document pairs to `not_cited` and its
regex failed on 105 document-pair rows with nested titles. Eight of those rows
were genuine mentions. The new Stage 2.5 analysis preserves the frozen C6
files, reproduces their 53/947 output as a legacy diagnostic, and reports the
corrected 763-row estimand separately.

## Claims that reproduced

- 18 frozen trajectories and every diff-event cell.
- 100 traces and the complete registered/sensitivity overlap denominators.
- All C3 outcome categories, logical-work estimates, verifier-cost thresholds,
  2,000-resample intervals, and displayed net-saving signs.
- Six prescreened selective-consumption candidates, three included audit units,
  Q1/Q0/Q1 code-only outcomes, and zero qualifying runtime instances.
- D0's four-node workflow reconstruction, 164/164 label agreement, resource
  arithmetic, and ineligible-as-proposed decision.

The exact logical-path and SHA-256 bindings are in
`stage2_5/descriptive_counts.json` and the machine-readable
`PAPER_CLAIM_AUDIT.json`.

## Reproducibility limit

The submission package is honest but not self-contained for full aggregates.
Its fixtures reproduce code paths and structural invariants. Reviewers need
the separately preserved raw inputs at the declared hashes to recompute the
full aggregate tables. The paper now states this directly.
