# Final Research Direction Decision(CP4)

日期:2026-07-21 · 主协调代理/科学主席

## 选择结果

```
PRIMARY_CANDIDATE = NONE
BACKUP_CANDIDATE  = C6'(重述版:原生选择性消费 workflow 上的 provenance + query-relative 增量维护)
REJECTED_CANDIDATE = C4(HIGH_COLLISION,C4-P6 SAME 轴 13/15)
RECOMMENDATION    = RETURN_TO_IDEA_STAGE(有界重入,见下)——不建议 ARCHIVE
```

## 为什么 PRIMARY = NONE(逐条对照 CP4 必要条件)

| 条件 | C3 | C6 | C4 |
|---|---|---|---|
| novelty ≥ NARROW_GAP | ✔(NARROW) | ✔(CLEAR) | ✘(HIGH_COLLISION) |
| gate 不是 FAIL | ✘(FAIL,经济性) | ✘(FAIL,testbed/机制) | —(REQUIRES_AUTHORIZATION) |
| 清晰 falsification criterion | ✔ | ✔ | ✔ |
| 一周原型不要求复杂新框架 | ✔ | ✘(需新 workflow) | ✘(需 GPU+复现 P6) |
| correctness/outcome oracle 可获得 | ✔ | ✔ | ✔ |

没有任何候选同时满足全部五条。按任务书 §八,必须输出 NONE,不得为完成流程强选。

## 为什么没有产出最终 Idea Card

Idea Card 为主候选而设。PRIMARY=NONE 时,为任何候选写 30 字段 idea card 都会
制造"已有可执行方向"的假象,违反纪律 7(claim 与证据范围一致)。本备忘即最终产物。

## 为什么这不是旧 Route A+ 的简单延续

- Route A+ 的形式化(receiver-conditioned typed contract、K2 canonicalizer、
  v8 harness)没有任何一条被保留;本轮三个候选全部来自重新发散的 landscape。
- 本轮新增的证据反而**强化**了旧反例的普适性:NEG-25 的全上下文失效模式在第二个
  独立 testbed 家族(E0 4-agent RAG)复现;文本 usage 代理第三次失效。
- 本轮产出的三个 gate 失败全部是**新窄命题**(outcome verifier 混淆问题、
  query-relative 不安全性的直接证据、C4-P6 DIRECT 撞车),不是旧结论的复述。

## 为什么不是普通 cache / lineage / speculative execution 的改名

- 普通 cache/lineage:Rosen & Rosen(identity replay)与 ToolCacheAgent(identity 缓存)
  已在 agent 域占据;C6 的增量([D]+[Q])被 gate 证明在当前 testbed 不安全——
  改名与否的争议已被证据取代:机制在可得 testbed 上不成立。
- speculative execution:Sherlock 已占据运行时骨架;C3 的问题实例(状态变化后复用)
  虽无占用者,但其默认实验形式被经济性判死——同样由证据而非术语裁决。

## 旧负面证据仍然直接约束后续工作

- NEG-11(文本代理不可作 oracle/contract)→ C3' 的定向 verifier 不得用文本启发式;
- NEG-25(全上下文 prompt 消灭稀疏性)→ C6' 的 workflow 必须原生选择性路由;
- NEG-19(exact 与增量分报)→ 一切 coverage 报告纪律;
- NEG-24(outcome 必须真测)→ C3'/C6' 的 oracle 设计;
- NEG-14(cascade identity 不可默认)→ 一切双跑对照的先决自检。

## 给负责人的重大决定包

DECISION_EVENT = 6(没有候选满足最低条件)
CURRENT_PHASE = CP4 完成
VERDICT = PRIMARY=NONE;BACKUP=C6';REJECTED=C4;RECOMMENDATION=RETURN_TO_IDEA_STAGE(有界)

EVIDENCE:
- CP1:27 篇全文级核实(`literature/fulltext/`,manifest+bib),C4-P6 DIRECT 撞车、
  C6-P6 identity replay 基线确认、Sherlock 机制骨架确认;
- CP2:C3=NARROW_GAP、C6=CLEAR_GAP、C4=HIGH_COLLISION(`scoop_checks/`);
- CP3:C3_GATE=FAIL(ρ_outcome≈0.40 ≫ ρ*≤0.14,outcome verifier 混淆问题);
  C6_GATE=FAIL(引用不预测敏感度,未引用 doc 仍致 5% flip,query-relative 不安全);
  C4_GATE=REQUIRES_AUTHORIZATION(`gates/`)。

CANDIDATE_IMPACT:
三个候选在"全文+独立 scoop-check+严格 gate"下无一存活到主候选标准;
但失败全部转化为精确的新知识(两个判死机制 + 一个模式级结构约束 + 一个直接撞车),
并收敛出唯一的先决未知量:自然 agent workflow 中是否存在原生选择性消费。

OPTIONS:
A. **有界重入(RECOMMENDED)**:只做一件事先行——对 2–3 个公开真实 agent 框架
   trace 做"选择性消费审计"(CPU-only,零模型,约 1–2 天)。若存在原生选择性消费
   实例,C6' 立即重启为主候选,C3' 的定向 verifier 问题随之获得意义;若不存在,
   整个"复用有效性"研究线获得第三条独立结构负证据,转测量/立场论文后归档。
B. 直接转测量论文:把本轮两个判死机制 + 模式级结构约束写成测量论文
   ("Why reuse-validity is not yet measurable in real agent workflows"),然后归档。
C. 绕过先决未知量,直接授权 C4' 或 C3' 的 GPU 实验——**不推荐**:C4' 撞车未解,
   C3' 缺定向 verifier,都是已知死路的重复。

RECOMMENDATION: A(选项 A),理由:成本 1–2 天 CPU,直接裁决整个研究线的存废,
且无论正负结果都有发表路径。B 是 A 失败后的自然退路。

REQUESTED_AUTHORIZATION:
- 仅请求批准选项 A 的 trace 审计(公开数据,CPU-only);
- 不请求 GPU/模型/新框架;正式实验须待 A 的结果后另行裁决。

CURRENT_HEAD: (见 handoff LAST_COMMIT)
WORKTREE_STATUS: 干净(仅 .agents/ .claude/ 未跟踪)
HANDOFF: docs/RESEARCHSTUDIO_HANDOFF.md
