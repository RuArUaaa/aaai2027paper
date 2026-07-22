# Stage 2.5 Citation Audit

Status: **PASS AFTER CORRECTION**

The final manuscript contains 21 cited keys and 21 bibliography entries, with
no missing or orphan entries. A fresh zero-context read-only reviewer checked
all citation contexts against primary publication records, proceedings,
author-maintained records, or immutable official repository commits. The
cross-model MCP reviewer prescribed by the generic audit workflow was not
available; this is a process limitation, so the coordinating reviewer repeated
the six load-bearing checks directly against primary sources.

## Load-bearing 2025--2026 checks

| Key | Verified status | Mechanism/context verdict |
|---|---|---|
| `agentTraceProvenance2026` | arXiv 2606.04990 v4, revised 2026-06-28 | Context supported. The bibliography was stale: the v4 title adds “A Survey of,” and the current byline has 11 authors. Both are corrected. |
| `provenanceGuard2026` | arXiv 2606.18037 v1, 2026-06-16 | Stable MCP tool/source IDs and source-aware factuality are directly supported. |
| `stepcache2026` | arXiv 2603.28795 v1, 2026-03-24 | Retrieval, lightweight per-step verification, and selective patching/fallback are directly supported. |
| `kvflow2025` | NeurIPS 2025 main track, volume 38 | Workflow-aware prefix-KV caching is directly supported. |
| `agentWorkflowMemory2025` | ICML 2025, PMLR 267 | The paper induces textual workflows from past action trajectories. The unsupported contrast with “completed computation artifacts” was removed. |
| `sherlock2025` | arXiv 2511.00330 v1; no official MLSys proceedings record found as of 2026-07-22 | Selective verification, concurrent downstream speculation, and rollback are supported. The public paper has no cross-run cache or historical completed-artifact replay branch. C3 scoop re-review is not triggered. |

## Other corrections

- `agentreuse2024`: added Guoliang Chen and the journal volume, issue, and
  pages from the official journal record.
- `autogen2024`: corrected the title to singular “Multi-Agent Conversation”;
  `autogenRepo` now binds the exact handoff path to commit `027ecf0`.
- `sweagent2024`: retained for the base system; `sweagentRepo` now binds
  RetryAgent/Preselector to commit `3ea751c`.
- `octopack2023`: the manuscript now attributes source and tests to
  HumanEvalPack and explicitly attributes stored pass/fail labels to the local
  paired archive.
- `langgraphRepo`: added an explicit immutable-commit URL.

The machine-readable per-entry ledger is `CITATION_AUDIT.json`. No source was
removed, and no remaining context depends on a secondary survey when a primary
record was available.
