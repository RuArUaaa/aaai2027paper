# AAAI-27 Abstract Submission Text

```text
STATUS = READY_FOR_MANUAL_SUBMISSION
OWNER_DECISION = OPTION_A
PAPER_TYPE = MEASUREMENT_AND_METHODOLOGY
OPENREVIEW_SUBMISSION = NOT_PERFORMED
EXPERIMENT_AUTHORIZATION = NONE
LAST_UPDATED = 2026-07-22T15:14:55+08:00
```

This file supersedes the proposed submission text in
`docs/FABLE5_ABSTRACT_SUBMISSION_RECOMMENDATION.md`. The Fable 5 document is
retained as an independent review artifact; it is not the authoritative text
to paste into OpenReview.

The official deadline is 2026-07-21 23:59 UTC-12, i.e. 2026-07-22 19:59 in
Beijing. AAAI-27 requires a complete title and abstract and warns that a
substantive title or abstract change may lead to rejection without review:

- [AAAI-27 Submission Instructions](https://aaai.org/conference/aaai/aaai-27/submission-instructions/)
- [AAAI-27 Paper Modification Guidelines](https://aaai.org/conference/aaai/aaai-27/paper-modification-guidelines/)

## Title

> **Measure Before You Reuse: Qualifying Computation-Reuse Claims in LLM
> Agent Workflows**

Revision note (2026-07-22T15:14:55+08:00, owner-confirmed): title option B was
accepted and the Fable 5 wording was narrowed after claim audit, before any
OpenReview submission. The final text scopes the proxy failures to the tested
analyses, names the precise SWE-agent component, makes the verifier distinction
conditional, and describes D0 as an executed static gate rather than a
validated end-to-end experiment. No numerical result or new contribution was
added.

## TL;DR

> In our analyses, final-text proxies did not validate native use or
> reuse-caused effects. We provide an evidence ladder, a pinned three-framework
> audit, verifier-aware economics, and an outcome-grounded protocol with an
> executed static gate.

## Abstract

> Reusing previously completed computation—such as cached tool results, recorded
> model responses, or repaired intermediate state—can reduce the cost of LLM
> agent workflows. Yet a reuse claim is meaningful only if one can identify
> what was delivered, what was actually accessed, which executions were
> skipped, at what validation cost, and whether reuse changed the outcome. We
> study this measurement problem. First, across three proxy analyses, output
> similarity, lexical overlap, and citation mentions did not provide validated
> evidence for the equivalence or downstream-dependence claims tested. Second,
> we introduce a preregistered evidence ladder that separates non-delivery,
> typed projection, and read-level access, and apply it at pinned commits to
> AutoGen, LangGraph, and SWE-agent's RetryAgent; within this bounded audit,
> none of the located public artifacts provides a qualifying runtime trace for
> a strong selective-consumption testbed. Third, we derive a cost model for
> speculative reuse that shows that the feasible cost regime depends on
> verifier cost and on whether a verifier can distinguish reuse-induced damage
> from baseline error. Finally, we specify an outcome-grounded protocol for
> measuring realized skips, validation overhead, and outcome agreement, and
> apply its static qualification gate, which rejects a proposed testbed as
> ineligible under the stated counterfactual and implementation criteria.
> Together, these results provide an auditable standard for deciding when an
> agent-workflow reuse claim is supported, when it is only code-possible, and
> when the available measurement cannot identify the claim.

## Topics and keywords

- Primary topic: `MAS: LLM-based Agents & Agentic Systems`.
- Secondary topics:
  - `ML: Evaluation, Benchmarking, Datasets & Analysis`;
  - `ML: Efficient, Edge, Green & Hardware-aware ML`;
  - `MAS: Tool Use, Orchestration & Multi-Agent Coordination for LLMs`.
- Keywords: LLM agents; computation reuse; measurement validity; testbed
  qualification; verification cost; reproducibility.

## Claim lock

The submission text commits to four contributions that already have repository
evidence or an authorized design artifact:

1. three bounded failure analyses of final-text usage proxies;
2. the Q0–Q3/QX evidence ladder and bounded three-framework audit;
3. the verifier-cost and post-hoc attribution model;
4. an outcome-grounded measurement protocol, together with its executed
   static qualification gate (D0).

It does **not** claim that:

- a new cache or reuse mechanism exists;
- a strong C6 testbed was found;
- a C3 directed verifier was found;
- an actual-skip model experiment has been completed;
- the three-framework audit represents the entire ecosystem.

A later controlled run, if separately authorized, is an evaluation of the
fourth contribution rather than a new primary contribution. Failure to run it
does not change the executed D0 qualification-gate claim in this abstract.

## Manual submission checklist

- [ ] All authors and author order confirmed by the responsible author.
- [ ] Title, abstract, TL;DR, topics, and keywords pasted exactly.
- [ ] OpenReview submission ID recorded.
- [ ] Saved submission reopened and checked for truncation or encoding damage.
- [ ] Confirmation retained outside the repository if it contains identity or
  account information.

No assistant has opened, edited, or submitted an OpenReview record in this
stage.
