# C6 Gate Protocol — Provenance-Artifact Reuse + Query-Relative Incremental Maintenance (Revision Eligibility)

Status: pre-registered by the science chair; analysis executed by the data-analysis subagent (CPU-only, Python 3 stdlib only, no model calls, no GPU).

## 1. Data

- Source (read-only): `/Users/zijian_nong/research/aaai2027/runs/traces/taskA_e0.jsonl`
- 100 traces of a **real agent workflow**: E0 Task A, 4-agent RAG pipeline
  (Retriever → Reader → Verifier → Writer), real Qwen2.5 runs.
- Each line: `trace_id`, `question`, `gold_answer`, `full_recompute_answer`
  (from-scratch oracle), `agents[4] × {agent_id, output_text, output_len, blocks[{block_id, text, span}]}`.

This is a real workflow, not a synthetic one. Doc/cite block routing is the pipeline's native design.

### Natural vs manufactured sparsity

Incidence in this workflow is **dense**: every agent receives all ~10 doc blocks (plus sys/cite and
the upstream plan/evid/verify blocks) — nothing is routed away. The query-relative sparsity measured
here therefore comes **only from the regions each consumer actually uses** (measured from its
`output_text`), not from any manufactured narrow-context routing. Any invalidation reduction we
measure is a property of consumption, not of an artificially sparse graph.

## 2. Definitions

- **Artifact** = `(trace_id, block_id)`. Block classes are derived from the `block_id` prefix:
  `sys`, `cite`, `doc`, `plan`, `evid`, `verify`.
- **Producer mapping**: `sys` → framework (**excluded from mutation analysis**),
  `cite`/`doc` → retriever, `plan` → reader, `evid` → verifier, `verify` → writer.
- **Consumer edge** = a `(block, agent)` pair appearing in `agent.blocks`. All 4 agents are
  consumers of every block they carry, including the producer itself.
- **Used region** of an artifact for a consumer: the artifact's sentences (split on sentence-final
  punctuation / newlines) that appear in that consumer's `output_text` after normalization
  (lowercase, non-alphanumeric → space, whitespace collapsed), as a substring match.
  Sentences with **< 8 words are not counted** (neither as used nor in the denominator).
  Robustness variant: a sentence counts as used if its word-level **3-gram Jaccard ≥ 0.5**
  against at least one sentence of the consumer's output.
- **Mutation simulation**: for every `doc`/`cite` artifact, split into sentences; take up to
  **8 positions** per artifact (if more sentences, uniformly sample 8 with the fixed seed below).
  For each mutated sentence:
  - **exact-replay** (Rosen & Rosen identity semantics): artifact content changed → **all** its
    consumers are invalidated;
  - **query-relative**: only consumers whose used spans intersect the mutated sentence are
    invalidated.
- **Cost weight**: consumer recompute cost ∝ its `output_len` (cost-weighted invalidation =
  sum of `output_len` over invalidated consumers).
- Reproducibility: `random.Random(20260721)`, sampling order fixed by trace file order and
  in-trace block order.

## 3. Pre-registered decision criteria

GO iff all of:

- (a) repeated-consumer coverage (fraction of non-`sys` artifacts consumed by ≥ 2 consumers) ≥ 30%;
- (b) cost-weighted invalidation reduction of query-relative vs exact-replay,
  `(exact − qr) / exact`, ≥ 20%;
- (c) oracle availability (`full_recompute_answer` present) ≥ 95%;
- (d) used-region measurement non-degenerate: median used-sentence ratio over mutation-relevant
  (`doc`/`cite`) (artifact, consumer) pairs satisfies 0 < median < 1 (neither everything-used nor
  nothing-used). If (d) is degenerate → `FAIL_MEASUREMENT`.

Reporting discipline (NEG-19): exact-replay hits and query-relative increments are reported as
**separate fields**; the increment `(exact − qr) / exact` is derived, never conflated.

## 4. External-project note

The gate protocol asks for an independent external project where possible. This run uses internal
real traces only; the limitation and its implication (conclusions restricted to the 4-agent RAG
structure) are recorded in `verdict.md`.

## 5. Outputs

`analyse_workflow.py` (stdlib only) → `results.json`; `test_gate.py` (focused asserts);
`verdict.md` (DRAFT — pending chair sign-off).
