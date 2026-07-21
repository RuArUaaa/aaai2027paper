# Process Provenance Addendum(评审 P1 整改)

日期:2026-07-21 · 主协调代理

## 1. 关于"逐阶段预注册"的诚实说明

本轮五个 commit(`421c976`…`252c9b2`)的形式是 CP0→grounding→scoop-check→gates→decision,
但**它们是工作完成后的分阶段归档(archival decomposition),不是每阶段完成即冻结的 checkpoint**。
具体事实:

- 第一个 CP0 commit(`421c976`)中的 handoff 内容在提交时已包含后续阶段的最终状态
  (CP4 完成、PRIMARY=NONE、各 gate 结果);
- C3/C6 的 protocol、分析代码、results、verdict 全部在同一个 gate commit(`ab1ef00`)中加入;
- 因此,git 历史**不能**独立证明"protocol/阈值在查看结果前已冻结";pre-registered 目前
  只能依赖作者声明。

本文件不改变以上事实,仅将其如实记录。现有历史不改写、不 rebase
(tag `researchstudio-v1-gate-review-required` 冻结于 `252c9b2`)。

## 2. 自本文件起生效的强制流程

任何新 gate(含 C3 v2 及以后)必须采用四个独立 commit,顺序不可颠倒:

1. **protocol commit**(阈值/判据/语义冻结,此时不得存在任何结果文件);
2. **执行**(运行分析);
3. **raw result commit**(未经解读的 results.json + 脚本 + tests);
4. **verdict commit**(判定文档,允许引用 raw result,不得修改之)。

若在 verdict 阶段发现 protocol 缺陷:不得回改 protocol commit;
必须新开 v(N+1) protocol 并说明差异(本次 C3 v1→v2 即按此执行)。

## 3. 本轮评审裁决的落实位置

| 评审项 | 落实文件 |
|---|---|
| C3 公式与协议矛盾(P0) | `gates/C3/v2/`(protocol→raw→verdict 三 commit) |
| C6 "机制不安全"撤回(P0) | `gates/C6/verdict_v2.md`(FAIL_MEASUREMENT) |
| C6 novelty 降级 | `scoop_checks/C6_novelty_revision.md` |
| FULLTEXT_GROUNDING 降级 PARTIAL | 本文件 §4 + handoff |
| 可复现性(P1) | `data/SOURCE_MANIFEST.json`、`scripts/export_gate_inputs.py`、`gates/*/fixtures/`、`gates/C6/merge_results.py`、脚本参数化 |
| CP4 重跑 | `docs/final_research_direction_decision_v2.md` |

## 4. FULLTEXT_GROUNDING 状态更正

更正为:

```
SOURCE_RECORDS = 27
KEY_NEAREST_NEIGHBOR_FULLTEXT = PASS(Sherlock / Execution Lineage / Durable Artifacts / Prefill Notes / CacheBlend / Noria / DBSP / Differential Dataflow 等决定性近邻已全文或大全文阅读)
OVERALL_FULLTEXT_GROUNDING = PARTIAL
```

`source_manifest.json` 中 `full_text_obtained=false` 或 partial 的条目(Levy 1995、
Agent Workflow Memory、Prompt Cache、dKV-Cache、DroidSpeak、KEEP 等),
其机制描述与数字在引用时必须带 UNVERIFIED/PARTIAL 标签;凡进入论文的关键 claim
不得以这些条目为唯一证据。
