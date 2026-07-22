# FABLE5 Final Decision — 唯一推荐路线与改进建议分级

> **Disposition (2026-07-22): SUPERSEDED_AS_AUTHORIZATION.** Retained as an
> independent review recommendation. The binding decision is owner option A in
> `docs/FABLE5_OWNER_DECISION_A.md`.

日期:2026-07-22 · 审查者:Claude Fable 5(独立首席研究审查者)
配套:FABLE5_CURRENT_PAPER_REVIEW / FABLE5_EXPERIMENT_FEASIBILITY_REVIEW /
FABLE5_ABSTRACT_SUBMISSION_RECOMMENDATION / FABLE5_SEVEN_DAY_PLAN

---

## 1. 裁决

```text
RECOMMENDED_PAPER_PATH = C(hybrid)

论文身份 = measurement + methodology(measure-before-reuse 主线)
骨架     = 路线 B 四件套:代理失效 → 资格 rubric → 三框架审计 → verifier 成本模型
最后一级 = 有界 actual-skip exact-reuse 实验(HumanEvalFix 两阶段,测试 oracle,
           2×2 arms × {identity, light, heavy} mutation),不主张任何机制新颖性
保底     = Day 3 NO-GO 时回退纯 B(仍可按时成稿提交)
```

### 为什么选 C

1. 三位模拟审稿人(agent / systems / methodology)的**共同**抱怨只有一条:
   "你说现有测量都不合格,却没有展示一次合格的测量。" C 是唯一在一周内
   能消解这条抱怨的路线。
2. C 的实验对三种结局(正/零/failure)都有预登记出口,且零结果本身验证
   预登记预测(B3.5-I=0 方向),不存在"必须出正数"的压力——这与本项目
   的诚实纪律兼容。
3. C 完整保留了项目最强资产(方法论+审计),同时明确放弃了最弱主张
   (机制新颖性),novelty 防线收缩到可守的一条:identifiability-first
   资格框架及其首次正面示范。

### 为什么不选其他

- **不选 A(2×2 作主贡献)**:机制=response cache + tool cache,
  ToolCacheAgent/Prompt Cache/Sherlock 三面占位;正结果也只是
  "缓存有效"的工程复述。NO_GO。
- **不选纯 B**:预计 4/4/5 borderline-reject;"无一次合格测量示范"的
  结构性弱点无法靠写作弥补。仅作保底。
- **不选 D/WITHDRAW_AFTER_ABSTRACT(现在决定)**:摘要是免费期权,
  纯 B 保底稿保证截止日必有可交之物;撤回决定应留给 Day 7 gate 的
  质量标准,不应今天预判。
- **无第四路线**:instrumented-run 审计违反本轮冻结纪律且强化错误的
  短板;已在可行性评审中否决。

### 今天摘要怎么写

按 `FABLE5_ABSTRACT_SUBMISSION_RECOMMENDATION.md` §3 提交
(标题 "Measure Before You Reuse: An Identifiability-First Study of
Computation Reuse in LLM Agent Workflows");北京时间 19:59 前完成。

### 明天(Day 1)首先做什么

冻结 `experiments/exact_skip/protocol.md`(protocol commit,零结果)+
`manuscript/spine.md`。协议未冻结前不写一行 harness 代码。

### 24 小时后用什么 gate 决定继续或转向

Day 2 结束:mock 干跑 + 5 题真模型 smoke 是否全绿。
不绿 → Day 3 上午限时 3h 修复;仍不绿 → 实验永久放弃,转纯 B。
Day 3 18:00:identity 档 identifiability 校准 + 20 题 pilot 完整性
= 全量 run 的 GO/NO-GO(负责人二次授权预算)。

### 什么情况下必须撤回全文(Day 7 gate)

- claims matrix 中任何 CORE 主张证据不足且无法降级;
- 摘要-终稿偏差构成实质换题(desk-reject 风险);
- 内部终审判定稿件低于"诚实的 borderline"——此时转 workshop /
  下一会议,保护同主题后续投稿的信誉。

### 什么情况下即使没有正加速也值得提交

§1–4(代理失效、rubric、审计、成本模型)自洽成文,且 live 实验的
零结果是被干净测得的(identity 档校准通过、聚类统计、预登记口径)。
measurement 论文的可发表性取决于测量质量,不取决于符号方向。

---

## 2. 关键差距登记

```text
MOST_SERIOUS_SCIENTIFIC_GAP    = 全项目从未执行过一次 live 计算跳过与 outcome 级验证;
                                 所有"节省"均为纸面推算(dossier §8-6/8-7,NEG-24)
MOST_SERIOUS_EXPERIMENTAL_GAP  = 无 fresh confirmatory 数据;审计全部 CODE_ONLY,
                                 machine-readable trace = 0
MOST_SERIOUS_NOVELTY_RISK      = Sherlock(投机+验证骨架)/ ToolCacheAgent(工具缓存)/
                                 Models Take Notes at Prefill(KV repair)三面合围;
                                 任何机制式措辞都会撞车;三篇发表状态需在 Day 6 复查
MOST_SERIOUS_WRITING_RISK      = manuscript 为零 + postmortem 化倾向:若按项目史
                                 而非科学问题组织,论文自动降级为复盘报告
```

---

## 3. 改进建议分级

### P0(今天,否则摘要不能提交)

| 项 | 文件/模块 | 目标 | 收益 | 风险 | 时间 | 依赖 | 验收 |
|---|---|---|---|---|---|---|---|
| P0-1 | 提交系统 | 按推荐文本提交标题+摘要+topics | 保住投稿资格 | 无(免费期权) | 1h | 负责人审定 | 提交编号存档,文本逐字核对 |
| P0-2 | 决策记录 | 负责人裁决 Route C 授权(或纯 B) | 解锁 Day 1–3 | 不裁决则实验线死 | 0.5h | P0-1 | 书面授权+预算上限(≤2,000 调用) |

### P1(24 小时内,决定实验是否启动)

| 项 | 文件/模块 | 目标 | 收益 | 风险 | 时间 | 依赖 | 验收 |
|---|---|---|---|---|---|---|---|
| P1-1 | experiments/exact_skip/protocol.md | 零结果协议冻结(arms/mutation/命中定义/统计/stop rules) | 实验合法性 | 定义不严→重蹈 NEG-08 | 3h | P0-2 | protocol commit,自检 PASS |
| P1-2 | manuscript/spine.md | 七页骨架+claims matrix v0 | 写作不等实验 | 无 | 2h | — | spine commit |
| P1-3 | harness 设计说明(协议附录) | 单层架构+allowlist+记账恒等式 | 防 harness 自伤 | 层数膨胀(NEG-02) | 1h | P1-1 | 设计说明 ≤2 页 |

### P2(全文截止前必须完成)

| 项 | 文件/模块 | 目标 | 收益 | 风险 | 时间 | 依赖 | 验收 |
|---|---|---|---|---|---|---|---|
| P2-1 | harness + focused tests + smoke | Day 2 全绿 | 实验入场券 | 历史 harness 死亡率 | 1 天 | P1-1/3 | smoke 5 题×4 arms 绿 |
| P2-2 | pilot + identifiability 校准 | Day 3 GO/NO-GO | 装置可信性 | serving 非确定性(NEG-14) | 0.5 天 | P2-1 | identity 档校准 PASS |
| P2-3 | confirmatory run + raw/verdict commits | live 数据点 | 论文第五节 | 时间 | 1.5 天 | P2-2 GO | Day 5 18:00 硬冻结 |
| P2-4 | manuscript §1–5 全稿 | 完整论文 | — | postmortem 化 | 3 天(并行) | P1-2 | claims matrix 无 UNSUPPORTED |
| P2-5 | 三近邻发表状态复查(一手) | novelty 防线更新 | 防撞车 | Sherlock 若已正式发表并扩展→ related work 重写 | 2h | — | 引用+状态注记 |
| P2-6 | artifact bundle(仓库外数据导出) | 可复现性 | 审稿加分 | 许可/体积 | 0.5 天 | — | bundle+SHA 清单 |
| P2-7 | 匿名化+格式+终审 | 提交合格 | — | — | 0.5 天 | P2-4 | Day 7 checklist 全过 |

### P3(时间允许时)

- Q-rubric 的 inter-rater 说明(第二人对 1 个框架独立赋 Q 级,附录);
- 三次代理失效的统一形式化记号;
- 摘要句式的 camera-ready 备选表。

### DEFER(补充材料或下一篇)

- 第二轮扩大框架审计(≥8 框架,另立预注册)——回应 "n=3" 批评的正道;
- C3 定向 verifier 作为独立研究问题(当前唯一的机制级未决问题,
  值得一篇独立论文);
- C6' 强 testbed 搜索 / instrumented-run 升级 TRACE_CONFIRMED;
- latent/KV 层计算传递(原始火花的最强形式,C5 轴)。

### DROP(不再投入)

- C4 Repairable reuse(HIGH_COLLISION,Models Take Notes 13/15 SAME);
- 一切文本级 usage/等价代理(三次失效,负知识已定案);
- SWE-bench 级依赖安装 + repository mutation 的完整 2×2(本周期);
- 在已完成审计内添加第四框架(违反冻结);
- exact caching 作为贡献主张的任何表述(NEG-19/22 红线)。

---

## 4. 合规声明(本审查轮)

```text
MODEL_CALLS = 0(仅 CFP 页面与检索的网络访问,无模型实验调用)
GPU_RUNS = 0
NEW_AGENT_TRAJECTORIES = 0
EXPERIMENTAL_FILES_MODIFIED = 0(gates/、audits/、inputs/、reports/ 全部只读)
新建文件 = 本轮 5 份 FABLE5_*.md(未提交,等待负责人审查)
git 历史 = 未 reset/rebase/stash/clean;三个任务前未跟踪目录原样保留
```
