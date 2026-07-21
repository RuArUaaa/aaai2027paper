# C4 Scoop-Check — Repairable reuse / selective recomputation

裁决人：主协调代理/科学主席(独立裁决；证据表由 CP1 子代理准备,见 `literature/fulltext/C4_fulltext_review.md`)
日期：2026-07-21

**C4_NOVELTY = HIGH_COLLISION(残余 NARROW 空位,不足以支撑主候选)**

## 逐轴比较(最近邻三篇)

### C4 vs Models Take Notes at Prefill(arXiv:2606.17107,arXiv-only)——DIRECT 撞车

| 轴 | 判定 | 依据 |
|---|---|---|
| 1. Scientific problem | **SAME** | 外部状态(field)mutation 后 KV 失效,修复而非全重算 |
| 2. Reuse object | SAME | 上下文 KV cache |
| 3. Producer/consumer | SAME | 单模型单 receiver(其 compose 为同模型拼接) |
| 4. State mutation model | STRICT_SUBSET(C4 窄于计划) | 其覆盖 field 值变更;C4 设想的一般 mutation 结构分类它只做一类,但 C4 原始设想的核心情形已被覆盖 |
| 5. Validity condition | SAME | ≡ full recompute(decision-identical) |
| 6. Verification timing | SAME | 修复后对照 |
| 7. Rollback/repair semantics | SAME | 三档:suffix 重算 / selective@K(判为不可靠)/ erratum(O(1) 鲁棒默认);CoT 门控 field-only |
| 8. Correctness guarantee | SAME | decision-identical ≡ from-scratch |
| 9. Execution mechanism | **SAME(核心撞车)** | mutation → 受影响区域识别(因果探针:locality patching/knockout/linear probing)→ 选择性修复;并给出关键负证据:CacheBlend 式 KV-deviation 选择器在此追错对象 |
| 10. Testbed | SAME | agent 场景(τ²-bench 工具 agent,轨迹中途状态变更)+ 用户记忆 + vLLM 在线 |
| 11. Primary estimand | SAME | 恢复率(recovery)、修复成本、延迟 |
| 12. Outcome oracle | SAME | decision-identical + 任务指标 |
| 13. Engineering assumptions | SAME | vLLM/KV 操作 |
| 14. Positive-result claim | SAME | "KV cache editable & composable;修复可达 ≡ recompute,成本 O(1)–O(K)" |
| 15. Null-result value | SAME | K\* 模型依赖、selective@K 不可靠、CoT 门控——边界刻画它已部分给出 |

**SAME 轴 13/15。** 残余差异(全部列出,无一遗漏):(a) receiver 轴(跨模型 × 内容 mutation 联合条件化)未覆盖;(b) task-conditioned 修复未覆盖;(c) 一般 mutation 结构的可修复边界(其只覆盖 field 值变更、单决策点);(d) 其 arXiv-only 且无公开代码。

### C4 vs KEEP(arXiv:2602.23592,arXiv-only)——强 PARTIAL

| 轴 | 判定 | 依据 |
|---|---|---|
| 1, 2, 3, 4, 10 | SAME | 具身 agent 记忆(外部状态)更新 → memory-group 粒度选择性重算,agent-stage mutation 格被占据 |
| 9 | STRICT_SUBSET | 启发式 memory group + 组间 cross-attention 迭代修复,无因果定位、无 ≡ 刻画 |
| 5, 8, 12 | STRICT_SUBSET | "精度损失可忽略/+4.13% 成功率"而非 ≡ from-scratch |
| 11, 14 | SAME(部分) | 显式以 CacheBlend 为基线并胜出——mutation 场景的基线竞赛已开始 |

### C4 vs CacheBlend(EuroSys 2025,正式发表)——PARTIAL(机制同族,触发不同)

| 轴 | 判定 | 依据 |
|---|---|---|
| 4 | ORTHOGONAL | chunk 重组合(内容假定不可变,hash 失效即整体重算)vs 内容 mutation 后的 stale 修复 |
| 9 | SAME(家族) | 选择性 token 重算 + ≈full prefill 质量基准;但 P6 已证其选择器在 mutation 场景失效 |
| 其余 | STRICT_SUBSET | 单模型单轮 RAG,无 receiver/task/stage 条件化 |

## 裁决六问

1. **去掉新术语后还剩什么独立机制?** 对原始 C4 表述:几乎不剩。mutation→受影响区域识别→选择性修复→≡recompute oracle→agent 场景→部分边界刻画(CoT 门控、K\* 模型依赖、CacheBlend 选择器失效),P6 逐点覆盖且SAME 轴 13/15。
2. **是否只是已有工作的直接应用?** 原始 C4 现在反过来像是 P6 的重复实现(P6 无代码,复现仍有证据价值,但不构成独立贡献)。
3. **残余新意属于哪类?** 仅剩:receiver×mutation 联合条件化(DroidSpeak 只有 receiver 轴、P6 只有 mutation 轴,交叉格为空)、task-conditioned 修复、跨 mutation 结构的统一可修复性分类学。属于"问题"的细分,不是新机制。
4. **最强 reviewer objection?** "P6 已做,你只是加 axis。" 且 P6 极可能正式发表并自然扩展到更多 mutation 类——残余空位的时间窗口可能比 P6 本身更短。
5. **哪项实验能证明残余空位成立?** receiver×mutation 交叉格:同一 field mutation,两个不同 receiver(微调变体),修复需求不同且 DroidSpeak 式 layer 选择与 P6 式 note-token 选择给出不同答案——若观测到此现象,残余空位为真。
6. **哪项结果直接判定残余空位也不成立?** 交叉格实验中修复需求不随 receiver 变化(note-token 集合与 receiver 无关),或 P6 新版已覆盖交叉格。

## 裁决

C4 作为**主候选**:HIGH_COLLISION,否决。残余交叉格(receiver×mutation)保留为**备选研究点**,仅当:(a) C6/C3 主线推进中自然需要 KV 层修复组件,或 (b) P6 发表状态变化留下空间时,再以"相对 P6 的增量实验"重新表述。按任务书 §三,这不构成 escape candidate 事件(C3/C6 未全灭)。
