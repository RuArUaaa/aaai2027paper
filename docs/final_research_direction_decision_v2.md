# Final Research Direction Decision v2(CP4 重跑,评审整改后)

日期:2026-07-21 · 主协调代理/科学主席
本文件取代 `final_research_direction_decision.md` 的裁决部分(v1 保留原样作历史)。

## 裁决

```
PRIMARY_CANDIDATE = PENDING_GATE_REAUDIT
EXPERIMENT_AUTHORIZATION = NONE
BACKUP_CANDIDATE = C6'(重述版,条件见下)
REJECTED_CANDIDATE = C4(维持,HIGH_COLLISION,评审 ACCEPT)
```

## 修正后的候选状态

| 候选 | novelty | gate | 状态 |
|---|---|---|---|
| C3 | NARROW_GAP(保留) | **NEED_NEW_VERIFIER**(v2,UNRESOLVED 类) | naive 形态微利窗极薄(v≲8%);全部科学重量落在"定向 verifier 是否存在"这一可证伪问题上;不是被证伪,也未通过 |
| C6 | NARROW_GAP / CONDITIONAL_CLEAR_GAP(已降级) | **FAIL_MEASUREMENT**(v2) | 机制 UNRESOLVED;usage/dependency 信号的合法来源已重新定义(原生路由/access log/显式 input,禁用文本代理) |
| C4 | HIGH_COLLISION | REQUIRES_AUTHORIZATION | 维持拒绝 |

## 为什么 CP4 仍不能选出主候选

- C3:gate 从 FAIL 修正为 UNRESOLVED,但"定向 verifier"本身尚无机制候选
  (NEG-11 封死文本启发式路线)——它需要先作为一个独立研究问题被回答,
  而不是作为 C3 的组件被假设存在。
- C6:机制未被判死,但也未获得任何正面证据;其合法 testbed(原生选择性路由)
  尚未被证明存在。
- 评审明确:PRIMARY=NONE 只能作为"暂不授权实验"的操作冻结,不能作为
  "三候选均已被科学淘汰"的最终裁决。本文件按此执行。

## 下一步(分析级,已获评审授权的范围内)

**唯一合法的下一步**:修正后的选择性消费审计(原"选项 A",按 C6 verdict_v2 §约束修订):

- 对象:2–3 个公开真实 agent 框架 trace(ToolSandbox 场景、公开 SWE 轨迹、
  代码分析型 agent 框架);
- usage/dependency 信号**仅允许**:workflow 原生路由、artifact access log、
  tool call/read trace、framework 显式 consumer input;
- **禁止**:最终文本 substring、Jaccard、引用提及、LLM 输出标题匹配;
- 若候选 testbed 只能提供文本代理 → 该 testbed 直接 FAIL_MEASUREMENT,
  其 flip 数据不得解释为机制证据;
- CPU-only,零模型/GPU;流程按 protocol commit → 执行 → raw commit → verdict commit。
- 审计结果决定:C6' 是否重启为主候选(query-relative 前提成立)、
  C3 的定向 verifier 问题是否获得研究对象、或研究线转测量论文后归档。

**明确不授权**:任何模型调用、GPU、新 agent 框架搭建、C3/C4 的正式实验。

## 给负责人的状态汇报

```
DECISION_EVENT = 6(修订后维持:无候选满足主候选条件)
CURRENT_PHASE = CP4 v2 完成
VERDICT = PRIMARY=PENDING_GATE_REAUDIT;EXPERIMENT_AUTHORIZATION=NONE
EVIDENCE:
- C3 v2:Δ/S 符号地图(reuse):naive +7.3%(v=0.01)/−1.7%(v=0.1);conditional +12.7%/+3.7%
- C6 v2:FAIL_MEASUREMENT;TEXT_USAGE_PROXY=INVALID;NATURAL_SELECTIVE_CONSUMPTION=UNRESOLVED
- C4:维持 HIGH_COLLISION(C4-P6 SAME 轴 13/15,评审 ACCEPT)
- P1 整改:provenance addendum、protocol→raw→verdict commit 顺序、fixtures+manifest+merge 脚本
REQUESTED_AUTHORIZATION:仅"修订后的选择性消费审计"(CPU-only);
其余一切实验维持 BLOCK。
HANDOFF: docs/RESEARCHSTUDIO_HANDOFF.md
```
