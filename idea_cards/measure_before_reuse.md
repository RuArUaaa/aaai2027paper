# Idea Card — Measure Before You Reuse

```text
STATUS = OWNER_APPROVED_PAPER_DIRECTION
EXECUTION_STATUS = DESIGN_ONLY
ACTUAL_SKIP_CALIBRATION = D0_INELIGIBLE_AS_PROPOSED
EXPERIMENT_AUTHORIZATION = NONE
DATE = 2026-07-22
```

## 1. One-sentence idea

Turn computation reuse in LLM agent workflows from a mechanism-first claim
into an identifiability-first measurement problem: require native evidence for
delivery/access, actual execution skips, validation cost, and outcome effects
before interpreting a reuse result.

## 2. Problem anchor

Existing agent-reuse studies and project prototypes can report cached outputs,
similar downstream text, or nominal cache hits without establishing four
different facts:

1. which consumer actually received or accessed an artifact;
2. whether a supposedly reused invocation was truly skipped;
3. whether verification cost erased the saved work;
4. whether an observed failure was caused by reuse rather than by the baseline
   task execution.

Conflating these facts produces claims that are not identifiable from the
logged evidence.

## 3. Paper thesis

A computation-reuse claim should be accepted only at the strongest evidence
level its native runtime records support. Final-text semantics are not a
substitute for routing/access evidence, and outcome success is not a substitute
for reuse-damage attribution.

## 4. Dominant and supporting claims

### Primary claim P1

The proposed evidence ladder separates claims that are routinely conflated:
non-delivery, typed projection, actual read access, actual execution skip, and
outcome agreement. Applying the frozen Q0–Q3/QX portion to three pinned
open-source frameworks yields only Q0/Q1 `CODE_ONLY` evidence; therefore the
bounded audit does not supply a strong C6 testbed.

Minimum convincing evidence:

- protocol committed before results;
- source locators and pinned commits;
- explicit CODE_ONLY versus TRACE_CONFIRMED distinction;
- no substring, Jaccard, citation, embedding, attention, or LLM-judge upgrade
  to native-use evidence;
- reproducible audit parser and focused tests.

### Supporting claim P2

The economics of speculative reuse depend on separately measured skip
fraction, verifier cost, and reuse-attributable damage. A post-hoc outcome
oracle can measure task agreement but does not become a runtime directed
verifier.

Minimum convincing evidence:

- frozen C3 traces and corrected v2.1 analysis;
- verifier cost normalized to full-run cost;
- `rho_outcome`, post-hoc `rho_blame`, rescue, and remaining-error terms kept
  distinct;
- all conclusions explicitly conditional on the verifier available.

## 5. Anti-claims

This paper does not claim:

- a new caching or reuse mechanism;
- receiver-conditioned validity or query-relative artifact reuse;
- ecosystem-wide absence of selective consumption;
- that CODE_ONLY paths occurred in a public execution;
- that task success attributes an error to reuse;
- that C3 or C6 has passed its strong gate.

## 6. Core contribution package

1. A failure analysis showing why final-text usage proxies do not identify
   downstream dependence.
2. A preregistered, mechanically applicable evidence ladder for qualifying
   agent-reuse measurements.
3. A bounded audit of AutoGen, LangGraph, and SWE-agent at pinned commits.
4. A verifier-aware cost model with explicit attribution limits.
5. An outcome-grounded actual-skip protocol plus a static qualification
   example. The proposed HumanEvalFix route failed that qualification before
   implementation; the protocol and auditable no-go, not a positive result,
   are the current contribution.

## 7. Optional calibration question

The now-closed HumanEvalFix calibration candidate asked:

> When an agent invocation is byte-identical at its explicit interface but
> relevant hidden environment state has changed, how much computation does
> exact replay actually skip, what validation overhead is incurred, and how
> often does the final task outcome agree with a from-scratch run?

This is a measurement question. It does not ask whether exact caching is novel
or whether selective consumption exists. The D0 source audit found the proposed
testbed ineligible: the native workflow has four LLM nodes, includes source and
tests in every prompt, lacks the proposed tool-result consumer path, and would
require a new harness. No calibration execution is therefore planned under
this card.

## 8. Load-bearing variable and falsification

The load-bearing variable is **semantic eligibility under byte-identical
explicit input**: whether a relevant native environment change can occur while
the complete serialized model/tool invocation remains identical.

Static falsification condition:

- If every outcome-relevant state element is already serialized into the
  invocation, state change makes exact replay a miss by definition.
- If a proposed hit requires omitting a serialized dependency from the key, it
  is not exact full-invocation reuse.
- If the condition exists only after rewriting prompts or building a new
  workflow, the proposed testbed is ineligible for this paper cycle.

The D0 audit observed these stopping conditions and closed the calibration
branch without weakening P1 or P2. In particular, the all-condition budget was
also undercounted: 1,968 was a condition-cell count, while even an optimistic
unimplemented two-stage scenario requires 3,280 model calls under the stated
identity-only-hit, two-calls-per-cell assumptions.

Conditional execution falsification, requiring later authorization:

- compare each replay arm with a paired mutated-clean run;
- the decisive downstream metric is outcome agreement with mutated-clean;
- use an identity or outcome-irrelevant state twin as the negative control;
- disagreement in the negative control indicates harness instability, not a
  reuse effect;
- no positive speedup is required for the paper claim.

## 9. Existing evidence

- C3 v2/v2.1: a narrow economic window can exist, but no runtime directed
  verifier exists.
- C6 v2: text usage proxies are invalid; natural selective consumption remains
  unresolved.
- Selective-consumption audit: AutoGen Q1/CODE_ONLY, LangGraph Q0/CODE_ONLY,
  SWE-agent Q1/CODE_ONLY; public runtime trace count supporting Q2/Q3 is zero.
- C4 remains rejected because of high collision.

## 10. Novelty position

The defensible novelty is the joint measurement discipline: native evidence
qualification plus execution/outcome/cost separation. Exact response or tool
cache mechanics are prior art and are excluded from the novelty claim.

The remaining risk is that reviewers view the contribution as a well-organized
audit rather than a sufficiently substantive methodology. A later calibration
can strengthen the paper only if it exercises a non-tautological eligibility
condition; an identity-only cache replay would not help.

## 11. Feasibility and budget

Current authorized phase:

```text
MODEL_CALLS = 0
GPU_RUNS = 0
NEW_AGENT_TRAJECTORIES = 0
EXPERIMENTAL_MUTATIONS = 0
```

Potential future calls are not authorized. The HumanEvalFix branch is stopped,
not waiting for budget. A materially different testbed would require a new
scientific decision, a new preregistration, and a workflow-derived call count.
The 2,000-call number in the Fable 5 review is not adopted.

## 12. Success, null, and stop outcomes

- **Paper success without calibration:** evidence ladder, bounded audit, proxy
  failures, and verifier economics form a coherent measurement/methodology
  paper.
- **Calibration positive:** report realized skips, validation overhead, and
  outcome agreement without a mechanism-novelty claim.
- **Calibration null:** report that exact eligibility or net savings collapses
  under state change; this is a measurement boundary, not a failed method.
- **Static no-go — observed:** omit the run and document why the candidate
  testbed could not express the required condition without a new harness.
- **Mandatory stop:** any need for text usage proxies, prompt rewriting, an
  artificial consumer, a large service/container, or unapproved model/GPU use.

## 13. Reviewer-facing paper shape

1. Why reuse claims are measurement claims.
2. Failure modes of text-level usage/equivalence proxies.
3. Evidence ladder and qualification rules.
4. Three-framework bounded audit.
5. Verifier-aware cost and attribution model.
6. Static calibration-qualification no-go and the outcome-grounded protocol it
   tested; no model experiment.
7. Limitations: bounded candidate universe, CODE_ONLY evidence, historical
   traces, and absence of a directed verifier.
