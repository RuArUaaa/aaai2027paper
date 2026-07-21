# ResearchStudio Collision Decision Memo(CP2 裁决 + CP3 联动)

日期:2026-07-21 · 主协调代理/科学主席

## CP2 裁决汇总

| 候选 | NOVELTY_STATUS | 最近邻 | 一句话裁决 |
|---|---|---|---|
| C3 投机复用+验证+回退 | **NARROW_GAP(可防守)** | Sherlock(MLSys 在审,机制骨架 DIRECT) | 问题实例(状态变化后复用历史计算)无占用者,但运行时骨架与 Sherlock 逐件对应;新意=问题+测量方法,不是机制 |
| C6 provenance+query-relative IVM | **CLEAR_GAP(附条件)** | Rosen & Rosen Execution Lineage(identity replay 基线本身) | [D]+[Q] 组合在 agent artifact 上无占用者;条件:文本 artifact 的 delta 语义须落地、P6/P7 同团队扩展的时间窗口 |
| C4 Repairable reuse | **HIGH_COLLISION** | Models Take Notes at Prefill(arXiv:2606.17107,SAME 轴 13/15) | 原始形式被直接覆盖;残余交叉格(receiver×mutation)留作备选研究点 |

详件:`scoop_checks/C3_scoop_check.md`、`C6_scoop_check.md`、`C4_scoop_check.md`、`collision_matrix.json`。

## CP3 gate 结果与 CP2 的冲突表

| 候选 | novelty | gate | 冲突 |
|---|---|---|---|
| C3 | NARROW_GAP | **FAIL(经济性)** | naive 形式被 ρ_outcome≈0.40 ≫ ρ*≤0.14 判死;outcome verifier 的混淆问题(baseline 错误 vs 复用引入错误)是判死机制 |
| C6 | CLEAR_GAP | **FAIL(testbed/机制)** | 结构前提(天然选择性消费)在 E0 testbed 不存在;query-relative 失效判定被证明不安全(未引用 doc 仍致 5% flip) |
| C4 | HIGH_COLLISION | REQUIRES_AUTHORIZATION | 未执行;即使授权也不应以原始形式进入实验 |

## 三个 gate 失败的模式级读法(主席)

1. **C3 的判死是因果账**:验证成本花在每个 baseline 错误上;投机要赢,需要定向 verifier(成本 ≤10% 重算)或大得多的 S。定向 verifier 正是 NEG-11 已失败的对象。
2. **C6 的判死是结构账**:两个独立 testbed 家族(TraceBuild 全上下文 prompt、E0 全 doc 路由)都以"consumer 接收全部上下文"消灭选择性消费。这是 NEG-25 的模式化,不再是单点失败。
3. **文本级 usage/等价代理第三次失效**(difflib、verbatim、引用通道),与 NEG-11/NEG-16 形成稳定负知识:任何依赖文本代理的 validity/usage 判定都应默认不可信。

## 抢救条件(精确、可检验)

- **C3'**:仅当 (i) regime 的 S ≫ 14%(长上游链/贵重算)且 (ii) 存在成本 ≤10% 重算、能区分"复用引入损坏"与"baseline 错误"的定向 verifier。无 (ii) 不得重启。
- **C6'**:仅当找到 consumer 原生选择性接触 artifact 子集的真实 workflow(选择性路由是设计属性)。usage 信号由路由提供,禁用文本代理。
- **C4'**:仅作为相对 C4-P6 的增量(receiver×mutation 交叉格),且须先复查 C4-P6 发表状态。

## 下一步未知量(唯一、精确)

> **自然发生的 agent workflow 中,是否存在 consumer 原生选择性消费 artifact 的实例?**
> 这是 C3'(定向 verifier 的意义)与 C6'(query-relative 的前提)共同的先决未知量。
> 可执行的低成本下一步:对 2–3 个公开真实 agent 框架 trace(如 ToolSandbox 场景、SWE-bench 公开轨迹、代码分析型 agent)做选择性消费审计——纯 CPU,零模型调用。
