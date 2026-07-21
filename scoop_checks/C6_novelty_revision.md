# C6 Novelty Revision(评审落实)

日期:2026-07-21 · 主协调代理

原裁决:`C6_NOVELTY = CLEAR_GAP(附条件)`(`scoop_checks/C6_scoop_check.md`,保留原样)。

**更正为:`C6_NOVELTY = NARROW_GAP / CONDITIONAL_CLEAR_GAP`**

理由(接受评审意见):provenance、identity replay、增量视图维护、query-relative view
usability 各自均有成熟先例(P6/P8 已覆盖 [P];DB 域覆盖 [D];PODS'95 覆盖 [Q] 理论)。
真正可能的空位仅是三者在 **agent artifact 上的合流操作化**:

1. 真实依赖提取(而非文本代理推断);
2. 无群结构文本 artifact 的 delta 语义;
3. 相对 identity replay 的可证额外收益(需真实多 consumer + 原生选择性路由的 testbed)。

`CONDITIONAL` 的含义:若后续 testbed 审计发现 agent workflow 中原生选择性消费普遍存在,
空位恢复为 CLEAR_GAP;若不存在,空位仅剩理论趣味,不支持实验投入。

原 scoop-check 文件不回改;本文件为正式修订记录。
