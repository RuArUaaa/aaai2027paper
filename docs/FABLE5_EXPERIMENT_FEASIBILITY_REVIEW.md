# FABLE5 Experiment Feasibility Review — 三条战略路线独立评估

> **Disposition (2026-07-22): PARTIALLY_ACCEPTED.** Route C remains
> design-only and is not a Q2/Q3 positive example, a C3 directed verifier, or
> an authorized model experiment. See `docs/FABLE5_OWNER_DECISION_A.md`.

日期:2026-07-22 · 审查者:Claude Fable 5(独立首席研究审查者)
前置:`docs/FABLE5_CURRENT_PAPER_REVIEW.md`
边界:本文件只做评估,不启动任何实验;EXPERIMENT_AUTHORIZATION 仍为 NONE,
授权决定权在负责人。

---

## 路线 A:Actual-skip exact reuse 2×2(作为主贡献)

设计回顾:C00 无复用 / C10 exact full-invocation recorded-response reuse /
C01 validated exact tool-result reuse / C11 combined;controlled repository
mutation;actual model/tool skip;验证开销与 patch/test/outcome agreement。

### 十五问逐项回答

1. **与原始 idea 的联系?** 弱。exact reuse 是原始火花中被 dossier 明确标注
   为"trivially solved 子集"的部分(C1 判死理由相同)。联系仅在于它是
   证据阶梯的底层("字节相同时能省多少"是"字节不同时"问题的 baseline)。
2. **是否只是 response cache + tool cache?** 作为机制,**是**。C10 就是
   record-replay cache,C01 就是带校验的 tool cache。任何机制新颖性主张
   都不诚实。作为**测量对象**(第一次带 outcome 验证的受控 actual-skip
   测量)则有窄的合法性。
3. **novelty 足够支撑 AAAI?** 作为主贡献,**否**。
4. **直接 prior art?** ToolCacheAgent(ICLR'26 在审,工具结果缓存,1.69×)
   直接占据 C01 的机制位;Prompt Cache、各类语义缓存占据 C10 邻域;
   Sherlock 占据"验证+回退"骨架。作为机制论文必死。
5. **本地代码/数据一周内能否支持?** 部分。stage-1 Task B(HumanEvalFix,
   164 题,测试即 oracle,依赖轻)的 pipeline 在旧 repo 可复用;SWE-bench
   级 repository mutation + 依赖安装(NEG-24 债务)一周内**不现实**。
6. **需要新建多少 harness?** 一个两阶段单 agent workflow + 双 cache 层 +
   skip 记账 + mutation 注入,约 2 天工程。历史教训:三代 testbed 死于
   harness(NEG-02~06),必须单层、最小化。
7. **需要模型/GPU?** 需要模型调用(API 即可,无 GPU);预算可控
   (164×4 arms×2 mutation 档 ≈ 1.3k 次调用级别)。
8. **deterministic oracle?** 有——HumanEvalFix 测试;这是全项目最便宜的
   outcome oracle,也是偿还 NEG-24 的唯一一周内途径。
9. **read-set/tool dependency 可操作化?** 在 HumanEvalFix 域可以(文件粒度
   即可);在任意 shell 域不可以(dossier §11-2:通用 Bash read-set tracer
   被明令 No-Go)。
10. **arbitrary shell 会否重新过度工程?** 会。必须 allowlist:只允许
    读文件/跑测试/提交 patch 三类工具。
11. **最小 allowlist?** `read_file`、`run_tests`、`apply_patch`(+可选
    `list_dir`,需排序,NEG-13 纪律)。
12. **fresh tasks?** HumanEvalFix 本身对本项目是旧数据集但新 live 运行;
    严格意义的 fresh split 可用 164 题的 discovery/confirmatory 二分。
13. **24 小时内能否完成资格门?** 能:mock-model 干跑 + 5 题真模型 smoke
    (见七天计划 Day 2)。
14. **正/零/失败分别写成什么?** 正:exact reuse 在低扰动下有实测净节省,
    验证开销实测为 v̂,与 C3 符号地图预测对照;零:命中率在非恒等扰动下
    塌缩(与 B3.5-I=0 的旧观察一致),"exact reuse 在状态漂移下买不到
    东西"成为测量论文的实证锚;失败(harness 未跑通):按 Day 2/3 stop
    rule 放弃,论文回退纯 B。三种结局都可发表——这是该实验作为**测量**
    而非**机制**的关键优点。
15. **与今天摘要兼容?** 兼容,前提是摘要按"controlled empirical evaluation
    of exact reuse"措辞,不承诺方向(见摘要建议文档)。

### 评分(作为主贡献的路线 A)

| 维度 | 评级 |
|---|---|
| Scientific importance | MEDIUM(实测数据缺口真实,但问题窄) |
| Novelty defensibility | **LOW**(机制=缓存;ToolCacheAgent 直接压顶) |
| Identifiability | HIGH(exact match + 测试 oracle,无语义代理) |
| Testbed fit | MEDIUM(HumanEvalFix 合适;SWE 级不可行) |
| Existing asset reuse | MEDIUM(stage-1 pipeline 可搬,harness 需新写) |
| Engineering complexity | MEDIUM(有历史性 harness 自伤风险) |
| Model/GPU dependency | 模型 API 需要;GPU 不需要 |
| Runtime risk | HIGH(一周窗口内任何 harness 事故都致命) |
| Statistical power | MEDIUM(164 题,task 级聚类;两档扰动) |
| Outcome oracle | HIGH(真实测试) |
| Positive-result value | LOW-MEDIUM(单独成文不够) |
| Null-result value | MEDIUM(作为测量论文证据有价值) |
| Abstract compatibility | MEDIUM(作主贡献会过度承诺) |
| Full-paper readiness | LOW(其余章节无处安放) |
| Seven-day feasibility | MEDIUM |

- 最乐观完成:3 天;现实:5 天;最坏:harness 死循环,0 产出。
- 最可能失败点:cache 键/skip 记账与 serving 非确定性(NEG-14)纠缠,
  导致"命中"定义在评审面前站不住。
- 24h stop signal:mock 干跑 + 5 题 smoke 未绿。
- **建议:作为主贡献 NO_GO;作为 Route C 的子实验 CONDITIONAL_GO。**

---

## 路线 B:Measurement / testbed qualification paper(纯测量,无新实验)

### 十问逐项回答

1. **已构成足够强的主贡献?** 接近但不足。方法论内容(代理失效 + rubric +
   审计 + 成本模型)是真实贡献,但全部证据为静态/重分析,AAAI 主会
   对"无新实验的测量方法论"容忍度低。
2. **三个 framework 太少吗?** 对"生态结论"太少;对"资格框架示范"够用。
   写法决定生死:必须写成 depth-over-breadth 的示范性审计。
3. **全 CODE_ONLY、无 TRACE_CONFIRMED 削弱论文吗?** 削弱,但同时**就是
   论文的发现本身**("公开生态不存在能确证复用主张的 runtime 证据")。
   要把弱点翻转为结论,措辞必须限定于冻结 universe。
4. **是否只是项目复盘?** 有此风险。防线:全文按科学问题组织,旧项目
   数据只以"证据 E1…En"形式出现,时间线放附录。
5. **足够 quantitative result?** 勉强:三次代理失效的配对统计、C3 符号
   地图、噪声地板、依赖稀疏统计。没有一张"main result"大表——这是
   硬伤。
6. **需要扩大框架审计吗?** 需要(评审会要求),但——
7. **扩大审计违反冻结纪律吗?** 在**本轮已完成的审计内**加第四候选:违反
   (protocol §3 明令)。合法路径是全文截止后另立预注册的第二轮审计
   (DEFER);一周内不做。
8. **能转成 methodology + measurement paper 而非 position paper 吗?**
   能,条件是加入至少一个正面测量示范(即 Route C 的实验)——否则
   methodology 无 demonstration。
9. **最强审稿意见?** "作者告诉我们现有测量都不行,却没有展示一次合格
   的测量。"(Reviewer 3 的 missing experiment,三位审稿人共同点。)
10. **正文七页独立成立吗?** 内容量够(甚至过多,需砍 C6/C4 线);说服力
    不够——预计 borderline reject。

### 评分

| 维度 | 评级 |
|---|---|
| Scientific importance | MEDIUM-HIGH(测量效度问题真实且无人系统处理) |
| Novelty defensibility | MEDIUM(方法论窄空位;无占用者,但易被贬为 checklist) |
| Identifiability | HIGH(它本身就是 identifiability 论文) |
| Testbed fit | N/A(无新实验) |
| Existing asset reuse | HIGH(一切已存在) |
| Engineering complexity | LOW |
| Model/GPU dependency | 无 |
| Runtime risk | LOW |
| Statistical power | LOW(n=3 框架;定性为主) |
| Outcome oracle | N/A |
| Positive-result value | —(无实验) |
| Null-result value | —(无实验) |
| Abstract compatibility | HIGH |
| Full-paper readiness | MEDIUM(全部内容存在,需 4-5 天纯写作) |
| Seven-day feasibility | HIGH |

- 最乐观完成:4 天;现实:5-6 天;最坏:6 天(写作无硬风险)。
- 最可能失败点:不是执行,是**接收概率**——预计 4/4/5 分,reject 概率高。
- 24h stop signal:无(纯写作路线没有实验型止损)。
- **建议:CONDITIONAL_GO——作为 Route C 失败时的保底出口,不作首选。**

---

## 路线 C:Hybrid(B 为骨架 + 有界 actual-skip 实验为最后一级证据)★推荐

结构:论文主体 = 路线 B 的四件套(代理失效 → 资格 rubric → 三框架审计 →
verifier 成本模型);第五节 = 一个**满足自家 rubric 的正面测量示范**:
HumanEvalFix 两阶段 workflow 上的 exact reuse 2×2,actual skip,测试级
outcome 验证,受控扰动 {identity, light, heavy} 梯度。**不主张任何新缓存
机制**;实验的论文角色是"用合格装置完成的第一次 live 复用测量",其数字
(正、零皆可)与 C3 冻结 trace 符号地图形成预测-验证对照。

### 六问逐项回答

1. **比纯 A/纯 B 更自洽?** 是。它精确回应三位模拟审稿人的共同抱怨
   ("展示一次合格的测量"),同时把 A 的机制新颖性死穴排除在主张之外。
2. **贡献过多、叙事分散风险?** 有,必须砍:C6 强形式、C4、依赖稀疏、
   K2 全部降级或删除(见 Paper Review §4 AC 部分)。主线只有一条:
   measure-before-reuse。
3. **一周内可完成?** 压线可行:实验与写作可并行(§1-3 章不依赖实验
   结果);Day 3 GO/NO-GO gate 保证失败时还有 4 天写纯 B。
4. **正文 vs 附录?** 正文:代理失效对照表、rubric、三框架审计结论表、
   成本模型符号地图、live 实验;附录:框架审计 locator 全表、C3 v1→v2.1
   修正史、协议与 commit 顺序、旧项目负结果目录。
5. **需要修改今天的摘要吗?** 不需要修改——今天的摘要就按 hybrid 写
   (见摘要建议文档);它同时覆盖 C 成功与 C 失败(退纯 B)两种终局,
   只在 C 失败时需把实验句从"we evaluate"弱化为对应实际内容,属于
   非实质修改。
6. **什么结果使 hybrid 失败?** (a) Day 2 smoke 未绿且修复超预算;
   (b) Day 3 pilot 中"命中"判定被 serving 非确定性污染且无法用
   identity 对照隔离;(c) Day 5 18:00 前拿不到可报告的完整 arm。
   任一发生→执行预登记回退:论文回退纯 B,实验记为 qualification
   failure(其本身可作一段诚实的 limitation)。

### 评分

| 维度 | 评级 |
|---|---|
| Scientific importance | MEDIUM-HIGH |
| Novelty defensibility | MEDIUM(方法论主张 + 明确放弃机制主张) |
| Identifiability | HIGH |
| Testbed fit | MEDIUM-HIGH(HumanEvalFix + 测试 oracle) |
| Existing asset reuse | HIGH(B 部分全存量;A 部分复用 stage-1 pipeline) |
| Engineering complexity | MEDIUM |
| Model/GPU dependency | 模型 API(Day 3 起);无 GPU |
| Runtime risk | MEDIUM(有预登记回退,不致命) |
| Statistical power | MEDIUM |
| Outcome oracle | HIGH |
| Positive-result value | HIGH(方法论+首个合格 live 测量) |
| Null-result value | MEDIUM-HIGH(零命中本身是干净结论) |
| Abstract compatibility | HIGH(按本审查的摘要草案) |
| Full-paper readiness | MEDIUM |
| Seven-day feasibility | MEDIUM-HIGH(靠 Day 3 gate 兜底) |

- 最乐观:Day 5 实验+初稿齐;现实:Day 6 全稿;最坏:Day 3 NO-GO 退纯 B
  (仍能按时提交)。
- 最可能失败点:harness(历史基线率高);其次是扰动档设计引起的
  "命中率恒 0 或恒 100"两端塌缩(需 identity 档校准)。
- 24h stop signal:Day 2 结束时 mock 干跑 + 5 题 smoke 未绿。
- **建议:GO(负责人授权后)。**

---

## 第四路线检查

审查未发现优于 A/B/C 的第四路线。曾考虑两个变体并否决:

- **D1:框架 instrumented-run 审计**(在 AutoGen/SWE-agent 上跑一次带
  OTEL 的真实 run,把 CODE_ONLY 升级为 TRACE_CONFIRMED):否决——
  违反本轮审计"不得制造证据"的冻结纪律;若做必须另立预注册,时间上
  与写作冲突,且它强化的是 n=3 审计而非论文最弱处(live 复用测量)。
- **D2:WITHDRAW_AFTER_ABSTRACT(占位后放弃)**:否决为**当前**决定——
  摘要是免费期权,且纯 B 保底稿的存在使"截止前必然无稿可交"不成立。
  保留为 Day 7 gate 的合法出口(条件见七天计划)。

---

## 汇总

```text
ROUTE_A_2X2_EXACT_REUSE   = NO_GO(作为主贡献)/ CONDITIONAL_GO(作为 C 的子实验)
ROUTE_B_MEASUREMENT_PAPER = CONDITIONAL_GO(保底出口)
ROUTE_C_HYBRID            = GO(推荐;需负责人授权模型调用,Day 3 gate 兜底)
OTHER_ROUTE               = 无(D1/D2 已考虑并否决,理由如上)
```
