# FABLE5 Seven-Day Plan — 从摘要提交到全文截止

> **Disposition (2026-07-22): NOT_AUTHORIZED_AS_EXECUTION_PLAN.** Only the
> CPU-only design/static-audit subset is active. Model-call milestones require
> a later owner decision; see `docs/FABLE5_OWNER_DECISION_A.md`.

日期基准:TODAY = 2026-07-22(北京);全文截止 = 2026-07-28 AoE
= 北京时间 2026-07-29 19:59。计划共 TODAY + Day 1–7,Day 7 即提交日上午。

总原则:

- 路线 = C(hybrid):measurement 骨架(不依赖实验结果的 §1–3 章)与
  有界 actual-skip 实验并行;Day 3 GO/NO-GO gate 决定实验去留;
  **写作永远不等实验**。
- 全程遵守 protocol → raw → verdict 分 commit 纪律(provenance addendum §2)。
- 冻结资产(gates/、audits/、旧 Route A+ 证据)只读。
- 每天预算按 6–8 有效小时计,不按满负荷理想日;Day 6 下午起冻结实验,
  Day 7 只做审读与格式。

---

## TODAY(7-22,剩余约半天)

- **Objective**:摘要提交 + 路线授权,不做任何其他工作。
- **Inputs**:`docs/FABLE5_ABSTRACT_SUBMISSION_RECOMMENDATION.md`
- **Tasks**:
  1. 负责人审定标题/摘要文本;
  2. 北京时间 19:59 前提交:标题、摘要、作者列表、topics/keywords
     (以提交系统实际必填字段为准;PCS/OpenReview 的 conflicts 域一并填);
  3. 提交后第一项检查:重开提交记录,与推荐文本逐字核对;
  4. 负责人裁决:授权 Route C 有界实验(模型 API 调用,预算上限建议
     ≤2,000 次调用)或明确选择纯 B。
- **今天禁止开始的工作**:harness 编码、任何模型调用、任何对现有
  gate/audit 文件的改动、扩大框架审计。
- **Deliverables**:提交确认(编号+邮件存档);授权决定记录。
- **Gate**:摘要按时提交 = PASS;未提交 = 全计划终止。
- **Hard stop**:19:59 北京时间。
- **Estimated hours**:1–2h。模型/GPU:无。可并行:否。

## DAY 1(7-23):协议冻结 + 论文骨架

- **Objective**:实验协议在见到任何结果前冻结;论文骨架落地。
- **Inputs**:授权决定;C3 v2 协议(公式沿用);dossier §10 设计规则。
- **Tasks**:
  1. `experiments/exact_skip/protocol.md`(protocol commit,零结果):
     - workflow:两阶段单 agent(HumanEvalFix 修复:阶段1 分析/阶段2 修复),
       工具 allowlist = read_file / run_tests / apply_patch(+排序 list_dir);
     - arms:C00/C10/C01/C11;mutation 档:{identity, light, heavy}
       (light=注释/空白级,heavy=函数体改写级;定义精确到 diff 规则);
     - 计量:skip 计数、token/调用节省、验证开销 v̂、测试通过一致性
       (vs C00 同题)、cache 命中定义(完整 invocation 级,NEG-08 纪律);
     - 统计:task 级聚类 bootstrap;164 题 discovery/confirmatory 二分;
     - 预登记预测:identity 档命中率高且无损;heavy 档 C10 命中→0
       (与 B3.5-I=0 旧观察一致方向);
     - stop rules(写死):同型 infra 失败 2 次即永久停实验;
       Day 5 18:00 数据冻结,无论完成度。
  2. `manuscript/spine.md`:七页分节骨架 + claims matrix v0(引用
     FABLE5_CURRENT_PAPER_REVIEW §2 的 CL 表);
  3. 相关工作清单冻结(以 literature/fulltext 为基,标注需复查发表状态的
     三篇:Sherlock、ToolCacheAgent、Models Take Notes at Prefill)。
- **Deliverables**:protocol commit;spine commit。
- **Gate**:协议自检(判据可满足性、stop rule 完备)PASS。
- **Hard stop**:protocol 未冻结不得写 harness 代码。
- **Estimated hours**:6–7h。模型/GPU:无。可并行:骨架与协议可并行。

## DAY 2(7-24):最小 harness + smoke

- **Objective**:单层 harness 可运行;5 题真模型 smoke 绿。
- **Inputs**:冻结协议;旧 repo `pipelines/task_b.py` 参考(只读)。
- **Tasks**:
  1. 实现最小 harness(单层 driver,NEG-02 红线:无 transport/supervisor
     分层);cache 层与 skip 记账;mutation 注入器;
  2. focused tests(fixtures 上,零模型):命中判定、记账恒等式
     (skip+run=total)、mutation 幂等性、排序确定性;
  3. mock-model 干跑全 164 题路径;
  4. 真模型 smoke:5 题 × 4 arms × identity 档(≤60 次调用)。
- **Deliverables**:harness + tests(commit);smoke 报告(raw)。
- **Gate / stop rule**:当日结束 smoke 未绿 → 触发 24h stop signal,
  Day 3 上午限时 3h 修复,仍不绿 → 实验永久放弃,转纯 B。
- **Estimated hours**:7–8h。模型:少量(smoke)。GPU:无。
  可并行:另一人/另一时段可写 §1(intro)草稿。

## DAY 3(7-25):校准 pilot + 主线冻结(关键 gate 日)

- **Objective**:确认测量装置可信,决定实验 GO/NO-GO。
- **Inputs**:smoke 结果。
- **Tasks**:
  1. pilot:20 题(discovery 半区)× 4 arms × 3 mutation 档;
  2. identifiability 检查:identity 档的命中率与 outcome 一致性
     (serving 非确定性污染检测,NEG-14 纪律);同题双跑分歧率
     = 噪声地板记录;
  3. 若 identity 档命中定义被非确定性污染且无法归因 → NO-GO;
  4. **GO/NO-GO 裁决 + 负责人授权全量预算**(GO:≈164×4×3 − pilot,
     上限 2,000 次调用;NO-GO:转纯 B,Day 4–5 全部写作);
  5. 主线冻结:无论 GO/NO-GO,论文主张清单冻结(此后只允许降级)。
- **Deliverables**:pilot raw commit;GO/NO-GO 决定记录。
- **Gate**:identity 档校准 PASS 且 pilot 完整 = GO。
- **Hard stop**:18:00 未达 GO 条件即 NO-GO,不许延期。
- **Estimated hours**:6h。模型:pilot(~250 调用)。GPU:无。
  可并行:§2(代理失效)章节写作。

## DAY 4(7-26):confirmatory run + 主写作日 1

- **Objective**:全量实验滚动;不依赖实验的章节完稿。
- **Tasks**:
  1. confirmatory run(confirmatory 半区 + discovery 补全),append-only
     写 raw 结果;运行期间**不看聚合统计**(只看健康度);
  2. 写作:§1 Intro、§2 代理失效(含三次失效对照表)、§3 资格 rubric
     + 三框架审计(直接改写自 audits/ 与 framework_matrix);
  3. **不允许改变的内容**:协议、arms、mutation 定义、命中定义、
     主张清单(Day 3 已冻结)。
- **Deliverables**:§1–3 初稿;run 进度记录。
- **Gate**:run 完成率 ≥60% 或预计 Day 5 中午前完成。
- **Estimated hours**:写作 5h + 值守 2h。模型:全量 run。可并行:是。

## DAY 5(7-27):run 收尾 + 分析 + 主写作日 2

- **Objective**:实验数据冻结、raw commit、verdict 分析;§4–5 成稿。
- **Tasks**:
  1. **18:00 硬冻结**:无论完成度,数据截断,raw result commit;
  2. 分析(预登记口径):命中率×mutation 档、净节省 Δ/C_full 实测、
     v̂ 实测、outcome 一致性;verdict commit;
  3. 写作:§4 成本模型(C3 符号地图 + 实测对照)、§5 live 实验;
  4. 若 Day 3 为 NO-GO:今日全部写作,§4 以 frozen-trace 分析收尾,
     §5 改为 qualification-failure 诚实记录或并入 limitation。
- **Deliverables**:raw + verdict commits;§4–5 初稿。
- **Gate**:全文各节初稿齐(允许粗糙)。
- **Hard stop**:实验相关一切工作 18:00 终止。
- **Estimated hours**:8h(本周最重的一天)。模型:run 收尾。

## DAY 6(7-28):整稿 + 图表 + claims matrix + artifact

- **Objective**:完整初稿;每条 claim 对应证据锁定。
- **Tasks**:
  1. 全稿组装,砍到 7 页(优先砍:C6/C4 叙事、依赖稀疏、项目史);
  2. 图表:代理失效对照表、Q-rubric×三框架矩阵、Δ/C_full 符号地图、
     live 实验主图;
  3. claims matrix 终版:每句主张 → 证据文件 → 限定语;
  4. related work 终稿(复查 Sherlock/ToolCacheAgent/Prefill Notes
     发表状态,一手来源);
  5. artifact 打包:把 SOURCE_MANIFEST 引用的仓库外数据导出为可发布
     bundle(或匿名下载链接方案),27 项 focused tests 说明;
  6. 内部对抗审读一轮(按 FABLE5_CURRENT_PAPER_REVIEW §4 三位审稿人
     的抱怨逐条自检)。
- **Deliverables**:完整 draft v1;artifact bundle 清单。
- **Gate**:draft v1 无 UNSUPPORTED 主张残留。
- **Estimated hours**:8h。模型/GPU:无。可并行:图表与文字。

## DAY 7(7-29,截止日):终审 + 匿名化 + 提交

- **Objective**:最终 GO/WITHDRAW 与按时提交。
- **Tasks**(上午开始,预留 4h 缓冲):
  1. 完整论文终审:claims matrix 逐条复核;摘要与终稿一致性检查
     (是否触发 substantial-change 风险——对照
     FABLE5_ABSTRACT_SUBMISSION_RECOMMENDATION §5);
  2. 匿名化检查(路径、repo 名、致谢、self-citation 口吻);
  3. AAAI 格式:9 页限制(7+2)、模板、参考文献完整性;
  4. **最终 GO / WITHDRAW 裁决**(标准见下);
  5. 提交(目标:北京时间 15:00 前,留 5h 应急缓冲)。
- **WITHDRAW 条件**(任一成立即撤回):
  - claims matrix 中仍有 CORE 主张证据不足且无法降级;
  - 摘要-终稿偏差构成实质换题;
  - 终稿被内部审读判定低于"诚实的 borderline"(与其投出一篇会伤害
    后续同主题投稿信誉的稿件,不如撤回转投 workshop/下一会议)。
- **即使没有正加速也值得提交的条件**:§1–4 自洽 + live 实验零结果被
  干净测得(零命中/零净益本身是预登记预测的验证)——measurement 论文
  不需要正加速。
- **Estimated hours**:5–6h + 缓冲。模型/GPU:无。可并行:否(单线终审)。

---

## 预算与缓冲总览

| 日 | 主轴 | 模型调用 | 缓冲 |
|---|---|---|---|
| TODAY | 摘要 | 0 | — |
| 1 | 协议+骨架 | 0 | 晚间 1h |
| 2 | harness+smoke | ~60 | Day 3 上午 3h 修复窗 |
| 3 | pilot+gate | ~250 | NO-GO 出口本身即缓冲 |
| 4 | run+写作 | ~1,200 | 写作不依赖 run |
| 5 | 分析+写作 | 收尾 | 18:00 硬冻结 |
| 6 | 整稿 | 0 | 全天写作日(计划要求的"至少一天写作整合") |
| 7 | 终审+提交 | 0 | ≥4h 提交缓冲(计划要求的"至少半天终审") |

总模型调用上限:2,000 次(负责人 Day 3 二次确认);GPU:全程 0;
新 Agent 框架:0;冻结证据修改:0。
