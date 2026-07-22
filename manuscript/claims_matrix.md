# Claim--Evidence Matrix

| ID | Manuscript claim | Repository evidence | Forbidden inference |
|---|---|---|---|
| C1 | Reuse measurement is decomposed into consumption, execution, cost, outcome, and attribution | `idea_cards/measure_before_reuse.md`; `experiments/actual_skip_calibration/preregistration.md` | The decomposition is universally necessary and sufficient |
| C2 | In three bounded analyses, the tested text proxies did not validate the corresponding equivalence or dependence claims | `inputs/route_a_plus_negative_evidence_dossier.md`; `gates/C6/results_sentence_level.json`; `gates/C6/results_doc_level.json`; `gates/C6/verdict_v2.md` | All text proxies are invalid, or natural dependence is absent |
| C3 | The protocol froze Q0--Q3/QX and CODE_ONLY/TRACE_CONFIRMED before deep source results; the explicit precedence is a later verdict-invariant semantic clarification | `audits/selective_consumption/protocol.md`; `audits/selective_consumption/verdict.md` | The precedence was externally preregistered, or the rubric has measured inter-rater reliability |
| C4 | The AutoGen handoff example is Q1/code-only, the LangGraph two-consumer fixture Q0/code-only, and RetryAgent's optional Preselector path Q1/code-only | `audits/selective_consumption/framework_matrix.md`; `audits/selective_consumption/raw_locators.json`; `audits/selective_consumption/verdict.md` | The labels classify every path in those frameworks or occurred in a public execution |
| C5 | No located artifact supplied a qualifying runtime instance for the strong-testbed criteria within the three frozen audit units | `audits/selective_consumption/results.json`; `audits/selective_consumption/verdict.md` | The whole ecosystem lacks selective consumption or public telemetry |
| C6 | On archived HumanEvalPack code-repair pairs, the logical-work model is positive at low verifier cost and negative at 10% under outcome rejection; the post-hoc blame regime is wider | `gates/C3/v2_1/results_v2_1.json`; `gates/C3/v2_1/verdict_addendum.md` | These are realized skips, deployed savings, or general thresholds |
| C7 | Outcome rejection does not identify reuse-induced damage; no runtime directed verifier was found | `gates/C3/v2/protocol.md`; `gates/C3/v2_1/analysis_correction.md`; `audits/selective_consumption/verdict.md` | C3 is solved or `rho_blame` is available online |
| C8 | The work specifies an outcome-grounded actual-skip protocol and executed its D0 static qualification gate | `experiments/actual_skip_calibration/preregistration.md`; `experiments/actual_skip_calibration/d0_static_audit.md` | D0 is an actual-skip experiment or method validation |
| C9 | The proposed HumanEvalFix Route C design is ineligible as proposed | `experiments/actual_skip_calibration/d0_results.json`; `experiments/actual_skip_calibration/d0_static_audit.md` | Outcome-grounded skip studies are generally impossible |
| C10 | Clean-clone fixtures reproduce code paths and invariants; full aggregates require external raw files with recorded hashes | `data/SOURCE_MANIFEST.json`; `gates/C3/v2_1/analysis_correction.md` | The repository is already a self-contained aggregate-data artifact |

Every numerical statement in the manuscript must map to one of C2, C4--C6,
or C9. Every literature statement must map to a verified entry in
`references.bib`. Stage 2.5 must audit the mapping without relying on this
matrix's conclusions.
