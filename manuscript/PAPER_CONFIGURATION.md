# Paper Configuration

```text
PIPELINE_STAGE = 2_COMPLETE_AWAITING_2_5
MODE = FULL
VENUE = AAAI-27_MAIN_TECHNICAL_TRACK
PAPER_TYPE = MEASUREMENT_AND_METHODOLOGY
LANGUAGE = ENGLISH
FORMAT = OFFICIAL_AAAI_2027_LATEX
CONTENT_PAGE_LIMIT = 7
REFERENCE_PAGE_LIMIT = 2
OPENREVIEW_SUBMISSION_NUMBER = 44503
ABSTRACT_LOCK = docs/AAAI27_ABSTRACT_SUBMISSION.md
EXPERIMENT_AUTHORIZATION = NONE
```

The paper asks one question: **What evidence is sufficient to identify a
computation-reuse claim in an LLM-agent workflow?** It reports each claim only
at the strongest level supported by native records and separates consumption,
execution, cost, outcome, and causal attribution.

The paper does not introduce a cache or reuse mechanism. It does not claim a
strong selective-consumption testbed, a runtime directed verifier, or a new
actual-skip experiment. The three native-path audit units are a prospectively
frozen, bounded sample and are not framework-wide classifications or an
ecosystem census.

The OpenReview title and abstract are authoritative. Any copy in `main.tex`
must remain semantically and numerically identical through the full-paper
deadline. Stage 2 ends at a complete compiled draft; Stage 2.5 is a separate
mandatory integrity gate.
