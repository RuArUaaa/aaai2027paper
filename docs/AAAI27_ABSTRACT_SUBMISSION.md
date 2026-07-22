# AAAI-27 Abstract Submission Text

```text
STATUS = READY_FOR_MANUAL_SUBMISSION
OWNER_DECISION = OPTION_A
PAPER_TYPE = MEASUREMENT_AND_METHODOLOGY
OPENREVIEW_SUBMISSION = NOT_PERFORMED
EXPERIMENT_AUTHORIZATION = NONE
LAST_UPDATED = 2026-07-22T12:44:00+08:00
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

> **Measure Before You Reuse: An Identifiability-First Study of Computation
> Reuse in LLM Agent Workflows**

## TL;DR

> We show why final-text proxies alone do not identify native use or
> reuse-caused effects,
> provide a preregistered evidence ladder and bounded framework audit, and
> formalize verifier-aware reuse economics together with an outcome-grounded
> measurement protocol.

## Abstract

> Reusing previously completed computation can reduce the cost of LLM agent
> workflows, but a reuse claim is meaningful only if one can identify what was
> delivered, what was accessed, what execution was skipped, and whether reuse
> changed the outcome. We study this measurement problem. First, our gate
> analyses show that text-based similarity, normalized overlap, and citation
> signals did not provide validated evidence for the equivalence or
> downstream-dependence claims tested. Second, we
> introduce a preregistered evidence ladder that separates non-delivery, typed
> projection, and read-level access, and apply it at pinned commits to three
> open-source agent frameworks. Within this bounded audit, none provides public
> runtime traces sufficient for a strong selective-consumption testbed. Third,
> we derive a cost model for speculative reuse that makes verifier cost and
> post-hoc blame attribution explicit. Finally, we specify an outcome-grounded
> protocol for measuring realized computation skips, validation overhead, and
> outcome agreement under controlled reuse, without treating final-text
> similarity as evidence of use. Together, these results provide an auditable
> standard for deciding when an agent-workflow reuse claim is
> supported, when it is only code-possible, and when the available measurement
> cannot identify the claim.

## Topics and keywords

- Primary topic: Intelligent Agents / LLM-based Agents — evaluation and
  analysis, using the closest available OpenReview taxonomy label.
- Secondary topics: Evaluation and Benchmarks; Reproducibility; ML Systems and
  efficiency.
- Keywords: LLM agents; computation reuse; measurement validity; testbed
  qualification; verification cost; reproducibility.

## Claim lock

The submission text commits to four contributions that already have repository
evidence or an authorized design artifact:

1. failures of final-text usage proxies;
2. the Q0–Q3/QX evidence ladder and bounded three-framework audit;
3. the verifier-cost and post-hoc attribution model;
4. an outcome-grounded measurement protocol.

It does **not** claim that:

- a new cache or reuse mechanism exists;
- a strong C6 testbed was found;
- a C3 directed verifier was found;
- an actual-skip model experiment has been completed;
- the three-framework audit represents the entire ecosystem.

A later controlled run, if separately authorized, is an evaluation of the
fourth contribution rather than a new primary contribution. Failure to run it
does not require deleting an empirical contribution claim from this abstract.

## Manual submission checklist

- [ ] All authors and author order confirmed by the responsible author.
- [ ] Title, abstract, TL;DR, topics, and keywords pasted exactly.
- [ ] OpenReview submission ID recorded.
- [ ] Saved submission reopened and checked for truncation or encoding damage.
- [ ] Confirmation retained outside the repository if it contains identity or
  account information.

No assistant has opened, edited, or submitted an OpenReview record in this
stage.
