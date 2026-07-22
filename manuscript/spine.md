# Seven-Page Manuscript Spine

## Page budget

| Part | Budget | Purpose |
|---|---:|---|
| Title and abstract | 0.30 page | Preserve the submitted claim lock |
| 1. Introduction | 0.70 page | Problem, three research questions, four contributions |
| 2. Background and related work | 0.55 page | Position this as measurement, not a reuse mechanism |
| 3. Identifiability-first framework | 1.15 pages | Claim decomposition, Q rubric, trace qualification |
| 4. Applying the framework | 2.15 pages | Three proxy analyses and the frozen three-framework audit |
| 5. Verifier-aware economics | 0.90 page | Cost model, observed regimes, attribution boundary |
| 6. Outcome-grounded qualification | 0.65 page | Actual-skip criteria and the executed D0 static gate |
| 7. Discussion and limitations | 0.40 page | Bounded generalization and reproducibility limits |
| 8. Conclusion | 0.20 page | Claim-specific evidence before reuse claims |

References may occupy pages 8--9 only.

## Narrative spine

1. A cache or reuse hit does not itself reveal delivery, access, actual skip,
   validation cost, outcome effect, or reuse-induced damage.
2. The paper turns these into distinct estimands and maps each to admissible
   runtime records.
3. Three bounded analyses show why final-text proxies did not validate the
   equivalence or dependence claims tested here.
4. A preregistered Q0--Q3/QX rubric, crossed with
   CODE_ONLY/TRACE_CONFIRMED, is applied to a frozen universe: AutoGen,
   LangGraph, and SWE-agent RetryAgent.
5. The audit finds only Q0/Q1 code-level paths and no qualifying runtime
   instance in the located artifacts; this leaves natural selective
   consumption unresolved.
6. A verifier-aware cost model shows why outcome rejection and causal
   attribution are economically different regimes.
7. An outcome-grounded protocol then rejects an ineligible proposed testbed at
   D0 before model execution, demonstrating the practical role of a
   qualification gate without presenting D0 as a positive experiment.

## Core displays

- Figure 1: claim-to-record map, with consumption level and evidence level as
  separate axes and execution/cost/outcome/attribution as separate claims.
- Table 1: target estimand, tested text proxy, observed behavior, and admissible
  conclusion for the three proxy analyses.
- Table 2: frozen framework qualification matrix.
- Figure 2: verifier-cost sign map for reuse and repair, separating the
  executable outcome regime from the post-hoc blame regime.

## Anti-claim lock

Do not state or imply:

- that this paper introduces a new cache/reuse mechanism;
- that text proxies are universally unable to measure model use;
- that selective consumption is absent from agent frameworks;
- that no public traces exist;
- that any Q1 path was observed at runtime;
- that the evidence ladder has independent inter-rater validation;
- that a runtime directed verifier exists;
- that the project never executed a skip;
- that D0 is a positive actual-skip experiment;
- that a clean clone reproduces all aggregate statistics; or
- that Task B economic thresholds generalize beyond the frozen traces.

