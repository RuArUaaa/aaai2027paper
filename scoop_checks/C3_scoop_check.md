# C3 Scoop-Check — 投机复用 + 低成本验证 + 回退

裁决人：主协调代理/科学主席(独立裁决；证据表由 CP1 子代理准备,见 `literature/fulltext/C3_fulltext_review.md`)
日期：2026-07-21

**C3_NOVELTY = NARROW_GAP(可防守)**

## 逐轴比较(最近邻三篇 + 一篇分类学参照)

记号:SAME / STRICT_SUBSET / STRICT_SUPERSET / ORTHOGONAL / UNCLEAR

### C3 vs Sherlock(arXiv:2511.00330,MLSys 在审)——机制最近邻

| 轴 | 判定 | 依据 |
|---|---|---|
| 1. Scientific problem | ORTHOGONAL | Sherlock:新鲜 workflow 执行中容忍未验证 LLM 输出(验证的延迟隐藏);C3:状态变化后避免重算历史计算(重算消除)。失效源不同(LLM 错误 vs 状态漂移) |
| 2. Reuse object | ORTHOGONAL | 新鲜下游续算 vs 历史/陈旧中间计算 |
| 3. Producer/consumer | SAME | workflow 节点 |
| 4. State mutation model | STRICT_SUPERSET | Sherlock 无状态漂移模型;C3 显式建模外部状态变更(ToolSandbox 语义) |
| 5. Validity condition | ORTHOGONAL | verifier 与未验证输出的一致率(m_i)vs 状态变化后的 outcome 正确性 |
| 6. Verification timing | SAME | 后台并行验证 |
| 7. Rollback semantics | SAME(结构上) | 选择性回滚+重算;C3 需额外副作用准入规则(→ SUPERSET 成分) |
| 8. Correctness guarantee | SAME | 不劣于非投机基线 |
| 9. Execution mechanism | **SAME(撞车点)** | "先跑、后台验证、失败回滚重算"运行时骨架逐件对应(§7 全部,含成本模型 Eq.4–6 与相似度门控选择性回滚) |
| 10. Testbed | ORTHOGONAL | LiveCodeBench/CoTCollection/OMEGA vs 代码 agent+真实测试/ToolSandbox 式状态 |
| 11. Primary estimand | ORTHOGONAL | 延迟/准确率/成本 vs ρ(拒绝率)、期望净节省、投机 vs 事前判定的边界 |
| 12. Outcome oracle | SAME | 任务指标 |
| 13. Engineering assumptions | STRICT_SUPERSET | Sherlock 未讨论副作用;C3 采用 C3-P10 的准入三分(side-effect-free/idempotent/commit-barrier) |
| 14. Positive-result claim | ORTHOGONAL | "首个联合优化成本/准确/延迟" vs "低 ρ 区间事前 validity 判定不必要,投机占优" |
| 15. Null-result value | ORTHOGONAL | — vs 投机/无脑复用/事前判定三方边界的否定刻画 |

### C3 vs Speculative Actions(arXiv:2510.04371,ICLR 2026 Oral)

| 轴 | 判定 | 依据 |
|---|---|---|
| 1–2, 4–5, 10–11, 14–15 | ORTHOGONAL | 前向预测未来 action,验证=等权威 Actor 真值到达后逐字匹配;无历史复用概念 |
| 3, 6, 8, 12 | SAME | — |
| 7, 9 | STRICT_SUBSET | 失配丢弃并行分支即可(投机从未生效),无需 checkpoint/状态回滚语义;C3 的回退语义严格更复杂 |
| 13 | STRICT_SUPERSET | 同上,lossy 仅 OS 调参个案(last-write-wins) |

### C3 vs AgentReuse(arXiv:2512.21309,JCRD 2024)

| 轴 | 判定 | 依据 |
|---|---|---|
| 1 | SAME(问题域) | 复用历史 agent 产物降延迟 |
| 2 | STRICT_SUBSET | plan 模板 vs 任意中间计算 |
| 5, 6 | **ORTHOGONAL(对立)** | 事前判定(意图分类+相似度阈值)vs 事后验证——正是 C3 定义中的对比极 |
| 7, 9, 13 | STRICT_SUPERSET | 无验证/回退/副作用处理,误判代价转嫁用户 |
| 11, 14 | ORTHOGONAL | 有效复用率/延迟 vs ρ 与决策边界 |

### 分类学参照:C3-P10(arXiv:2606.07846)
其 §3.1 把领域自我细分为 pre-completion 投机 / post-output-pre-verification(Sherlock 槽位)/ reasoning-time pre-launch(PASTE 槽位)。**"历史中间计算的复用型投机"不在该分类学中**——这是 NARROW_GAP 存在的结构化证据,同时意味着 C3 的差异陈述必须超越这套已有分类。

## 裁决六问

1. **去掉新术语后还剩什么独立机制?** 投机分支的来源从历史计算(缓存/陈旧中间结果)而非新鲜续算取得。由此:P(accept) 的驱动变量从模型错误率变为状态变更分布——ρ 可从 trace 直接测量;真正的对照基线从"非投机执行"变为"事前有效性判定"(AgentReuse 极)。这不是改名,是投机对象的换源 + 对照极的换边。
2. **是否只是已有系统在 agent 场景的直接应用?** 运行时骨架是(Sherlock 的直接应用);问题实例、estimand、状态漂移模型、副作用准入不是。
3. **新意属于哪类?** 问题(stale reuse after state change)+ 测量方法(ρ 的 regime 分解与决策边界)+ 系统成分(副作用准入的回退规则)。机制骨架**不新**——这是 NARROW 而非 CLEAR 的原因。
4. **最强 reviewer objection?** "这就是 Sherlock,只是投机分支从续算换成缓存。" 
5. **哪项实验证明它不是改名?** 在状态变更 regime 下展示:(a) Sherlock 的成本模型(以 verifier 输出一致率 m_i 为驱动)在 staleness 驱动的 ρ 下失准;(b) 复用型投机相对事前判定基线(AgentReuse 式分类器)与 Sherlock 式续算投机的双对照占优。两实验均在 mutation 梯度上做,事前定义预测方向。
6. **哪项结果直接判定 novelty 不成立?** 若在全部 mutation 强度下,复用型投机的期望成本 ≥ 事前判定基线,或 ρ 与 Sherlock 的 m_i 完全同分布(状态漂移不产生新现象)——则 C3 是改名,判死。

## 备注(诚实记录)
- Sherlock 为在审稿,发表状态可能变化;若其正式发表并扩展到缓存分支,C3 降为 HIGH_COLLISION,需重审。
- "stale reuse + 事后验证"未检到占用者为**阴性证据**,检索覆盖有限(尤其 OpenReview 盲区已在 CP1 部分覆盖:ICLR'26 投稿 ToolCacheAgent 被发现,但 NeurIPS'26 在审稿未检)。
