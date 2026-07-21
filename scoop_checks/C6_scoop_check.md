# C6 Scoop-Check — provenance artifact 复用 + query-relative 增量维护

裁决人：主协调代理/科学主席(独立裁决；证据表由 CP1 子代理准备,见 `literature/fulltext/C6_fulltext_review.md`)
日期：2026-07-21

**C6_NOVELTY = CLEAR_GAP(附条件)**

三格记号:[P] artifact 级 provenance 复用;[D] 增量/delta 维护(失效后只重算受影响部分,非整节点重跑);[Q] 多 consumer 的 query-relative validity。

## 逐轴比较(最近邻三篇)

### C6 vs Execution Lineage(Rosen & Rosen,arXiv:2605.06365,arXiv-only)——identity replay 基线本身

| 轴 | 判定 | 依据 |
|---|---|---|
| 1. Scientific problem | ORTHOGONAL | 可复现性(从 loop 到确定性 DAG)vs 复用效率+多 consumer 有效性 |
| 2. Reuse object | SAME | DAG 节点 artifact,带依赖边 |
| 3. Producer/consumer | SAME | 节点/下游节点;C6 额外要求 ≥2 独立 consumer 共享同一 artifact |
| 4. State mutation model | STRICT_SUPERSET | k_v 变化→失效,但无 mutation 内容结构(哪个字段/区段变);C6 建模区域级 mutation |
| 5. Validity condition | **ORTHOGONAL(核心差)** | execution-identity 哈希相等(单一全局判定)vs 相对各 consumer 查询的逐方判定 [Q] |
| 6. Verification timing | ORTHOGONAL | 重放时 vs 维护时+重放时 |
| 7. Rollback/repair semantics | STRICT_SUPERSET | 失效后整节点重跑 [无 D] vs 受影响子图 delta 维护 [D] |
| 8. Correctness guarantee | STRICT_SUPERSET | 未采用 from-scratch 等价 oracle(对照是 loop 基线,n=3)vs ≡ 全量重算双跑 |
| 9. Execution mechanism | STRICT_SUPERSET | identity replay(它本身就是 C6 命题中的基线) |
| 10. Testbed | STRICT_SUPERSET | 人工 memo 场景 n=3 vs 真实 agent trace + 自然 workflow |
| 11. Primary estimand | ORTHOGONAL | 保全率/污染率 vs exact-vs-query-relative 失效减少、cost-weighted coverage |
| 12. Outcome oracle | STRICT_SUBSET(它无) | 无双跑 oracle |
| 13. Engineering assumptions | SAME | typed local boundary/canonical output |
| 14. Positive-result claim | ORTHOGONAL | "DAG 比 loop 可复现" vs "identity replay 之上存在可测的 delta+query-relative 增量" |
| 15. Null-result value | ORTHOGONAL | — vs "依赖全稠密/query-relative 无增量"的领域判定 |

### C6 vs Durable Intermediate Artifacts(Rosen & Rosen,arXiv:2605.12087,arXiv-only)

| 轴 | 判定 | 依据 |
|---|---|---|
| 2, 3, 13 | SAME | artifact 数据模型(typed/dependency-aware/lineage)重叠最深——C6 可直接采用其 artifact record |
| 5, 7, 8, 11 | STRICT_SUPERSET | scope(role,scope) 是授权边界,**不是**按下游查询的可用性判定;无 delta、无 oracle;评估准则(F1/precision/recall)不同 |
| 1, 10, 14 | ORTHOGONAL | 数据模型/立场文 vs 机制+实验 |
| 其余 | STRICT_SUBSET(它无) | 无实验、无执行机制(委托 P6) |

### C6 vs ToolCacheAgent(OpenReview tX3YcbNa5w,ICLR 2026 在审)

| 轴 | 判定 | 依据 |
|---|---|---|
| 1, 10 | ORTHOGONAL | 工具结果缓存加速 vs artifact 复用的有效性理论;但同域最近邻 |
| 2, 3 | SAME | 工具产物、agent consumer |
| 4, 5 | STRICT_SUPERSET | cache key=参数 hash(identity)+ LLM 推断成对失效规则;**其 Limitations 自述 6 个错误来自 hidden dependencies——参数级 provenance 表达力不足的直接证据**,正是 C6 [P] 的动机 |
| 7, 8, 11 | STRICT_SUPERSET | 无 delta、无 query-relative、正确性靠 τ-bench 任务结果对比 |
| 14 | ORTHOGONAL | 1.69× 加速 vs 有效性判定的表达能力增量 |

### 理论来源(非撞车,为 C6 的迁移对象)
DBSP([D] 理论上限,abelian group 假设与文本 artifact 不匹配)、Differential Dataflow(偏序版本)、Noria(delta+部分物化,无 [Q])、Build Systems à la Carte(from-scratch 判据)、Levy et al. PODS'95([Q] 理论源头)。**全文核实范围内未发现任何工作把 answering-queries-using-views 式可用性判定或 delta 维护移植到 agent 中间产物。**

## 裁决六问

1. **去掉新术语后还剩什么独立机制?** 三件事:P6/P8 的 identity 失效语义之上,(i) 区域级 mutation → 受影响子图的 delta 维护(对**无群结构的文本 artifact** 重新定义"delta"——这是 DBSP 无法直接回答的);(ii) validity 从全局哈希相等改为相对各 consumer 实际使用区域的逐方判定;(iii) from-scratch 双跑 oracle 的实验范式。三者在所核文献中均无占用者。
2. **是否只是已有系统在 agent 场景的直接应用?** [P] 一格是(P6/P8 已在 agent 域);[D]+[Q] 的组合不是——DB 域有 [D] 无 [Q]、有群结构;PODS'95 有 [Q] 无执行;二者在 agent artifact 上的合流未见。
3. **新意属于哪类?** 机制(delta 语义 + query-relative 判定)+ 测量方法(双跑 oracle + exact/增量分报)+ 问题(agent artifact 的多 consumer 有效性)。
4. **最强 reviewer objection?** "这就是 build cache / IVM 在 agent DAG 上的直接应用。" 防守点:(a) 文本 artifact 无 Z-set 群运算,delta 语义必须重建;(b) query-relative 维度在 build/IVM 中不存在对应物;(c) consumer 是 LLM,"使用区域"的判定本身是新的技术问题。
5. **哪项实验证明它不是改名?** 在真实多 consumer trace 上,query-relative 判定相对 identity replay 产生非零且 cost-weighted 显著的失效减少(预登记门槛:≥20%),且 from-scratch 双跑确认正确性不损失;同一 mutation 对两个真实 consumer 给出不同 verdict 的案例存在。
6. **哪项结果直接判定 novelty 不成立?** 全部候选 workflow 依赖稠密(used-region 中位数=100%);或 query-relative 增量 coverage 拆分后恒为 0;或"同 mutation 不同 verdict"在真实 trace 中一次都不出现。

## 附条件(CLEAR_GAP 的保留条件)
- P6/P7 为 2026-05 arXiv-only,同一团队可能扩展;**时间窗口风险真实存在**,若其下一篇加入 delta/query-relative,C6 降级为 NARROW。
- P8 在审;若其扩展为 DAG 传递失效,覆盖 [P] 深化部分,但 [Q] 仍空。
- "delta 语义无群结构"必须在一周实验中给出具体定义(如区域级 replace-invalidate + 受影响 consumer 子集重算),不能只停留在类比。
