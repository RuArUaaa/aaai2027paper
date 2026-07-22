# FABLE5 Current Paper Review — 独立首席研究审查

> **Disposition (2026-07-22): REVIEW_INPUT.** Owner decision A accepts the
> measurement/methodology paper identity but does not authorize Route C as
> written. `docs/FABLE5_OWNER_DECISION_A.md` is authoritative.

日期:2026-07-22(AAAI-27 摘要截止日)
审查者:Claude Fable 5,独立首席研究审查者
审查基线:repo `/Users/zijian_nong/research/aaai2027-new`,branch `main`,
HEAD `3f7406e03a6caea81c046056a6b62bd9234b642a`
工作区:仅任务前已存在的 `.agents/` `.claude/` `.codex/` 未跟踪,与预期一致。

本轮独立复核动作(全部 CPU-only,零模型调用):

- 通读 §三 列出的全部核心文档(含 798 行 negative-evidence dossier 全文);
- 重跑全部 5 套 focused tests:selective-consumption 6/6、C3 v2.1 6/6、
  C3 v2 5/5、C6 5/5、C3 v1 5/5,共 27/27 PASS;
- 用 `data/SOURCE_MANIFEST.json` 对 5 个冻结源数据文件逐一复核 SHA-256,
  全部匹配(数据位于仓库外 `/Users/zijian_nong/research/aaai2027`);
- 抽查 `gates/C3/v2/results_v2.json` 关键数字与 verdict 文本一致;
- 经官方页面核实 AAAI-27 时间线:摘要 2026-07-21 AoE(北京时间今天
  19:59 前有效),全文 2026-07-28 AoE;摘要与终稿间实质性改动可被 desk reject。

**总体判断:仓库内的科学结论与底层证据高度一致,自我审计质量罕见地高。
但仓库中不存在任何 manuscript、abstract、submission 文件——当前"论文"
只以研究过程档案的形式存在。今天必须从零起草摘要。**

---

## 1. CURRENT_PAPER_IDENTITY

### One-sentence paper identity

> 一篇 identifiability-first 的测量/方法论论文:先证明"LLM agent workflow
> 中的计算复用主张目前普遍缺乏可辨识的测量基础"(文本代理三次失效、三大
> 公开框架无一提供可确证的 selective-consumption trace),再给出一个预注册
> 的 testbed 资格框架与投机复用的 verifier 成本模型,并(若本周实验获授权)
> 用一个有界的 actual-skip exact-reuse 受控实验作为证据阶梯的最后一级。

### Primary scientific question

**"在 LLM agent workflow 中,什么样的测量装置和 testbed 才能支撑一条计算
复用主张——而当你用合格的装置去实际跳过计算时,复用到底买到了什么?"**

这不再是原始火花的问题("receiver-conditioned validity 是否存在"),而是它
经过 25 个负面案例、三代 testbed、三次文本代理失效之后的合法收敛形态。

### Primary contribution(当前证据实际能支撑的)

**测量方法论 + 资格判定框架**:

1. 文本级 usage/等价代理(difflib、verbatim、citation channel)作为复用测量
   工具的三次独立失效(RAW_REPRODUCIBLE,跨两个项目);
2. delivery / typed projection / actual-read 三层证据区分 + Q0–Q3/QX 资格
   rubric + 预注册审计协议(protocol→raw→verdict 分 commit);
3. 对 AutoGen、LangGraph、SWE-agent 三个主流框架的 pinned-commit 审计:
   均为 Q0/Q1 + CODE_ONLY,machine-readable mechanism trace count = 0——
   即**公开生态目前不存在能确证 selective computation reuse 的 runtime 证据**。

### Secondary contributions

- C3 投机复用经济学的符号地图:naive outcome-verifier 投机仅在 v≲8% C_full
  时为正;假设定向 verifier 存在则窗口扩至 v≤13.7%;ρ_blame≈4.3%
  (CONDITIONAL,post-hoc 标签);
- trace-conditioned replay + identifiability gate 方法论(D2,97.37% 复现);
- (若授权)actual-skip exact reuse 2×2 受控实验:实测跳过量、验证开销、
  outcome 一致性——无论正/零/负,都是该证据阶梯的首个 live 数据点。

### Evidence already available

| 证据 | 等级 | 位置 |
|---|---|---|
| 文本代理三次失效 | RAW_REPRODUCIBLE | C6 verdict_v2 + 旧 repo NEG-11/16 |
| 三框架审计(Q0/Q1/CODE_ONLY,trace=0) | CODE_CONFIRMED(静态) | audits/selective_consumption/ |
| C3 经济学符号地图 | RAW_REPRODUCIBLE(冻结 trace 重分析) | gates/C3/v2, v2_1 |
| 六次自然工况 null(单 receiver) | RAW_REPRODUCIBLE(旧 repo) | NEG-01 |
| 依赖结构天然稀疏(2 repo) | RAW_REPRODUCIBLE | reports/c6_gate_24h |
| D2 identifiability gate 97.37% | RAW_REPRODUCIBLE(旧 repo) | dossier §9 |
| 近邻文献全文核实(Sherlock/ToolCacheAgent/Prefill Notes 等) | LITERATURE(一手) | literature/fulltext/ |

### Evidence still missing

1. **任何一次真实的 live 计算跳过**(dossier §8-6:所有测量都是事后判定);
2. **任何 outcome-level 验证**(NEG-24 债务;仅 Task B HumanEvalFix 的
   stage-1 测试信号例外);
3. **任何 TRACE_CONFIRMED 实例**(审计三候选全部 CODE_ONLY);
4. fresh confirmatory data(全部现有数字来自冻结 trace 重分析);
5. 可公开发布的 artifact 包(冻结源数据在仓库外,SHA 已核但未打包)。

### Claims currently defensible

- "文本级 usage 代理不能用于判定 agent workflow 中的复用效应"(三次独立失效);
- "三个主流公开框架在 pinned commit 下均不提供可将 artifact identity 绑定到
  consumer delivery 的公开 runtime trace"(限定于冻结 universe 与已发现的公开 artifact);
- "在冻结 trace 的成本模型下,naive 投机复用的正收益窗极薄(v≲8%),定向
  verifier 是决定性的未决变量"(CONDITIONAL 标注不可省略);
- "单 receiver 自然工况下,复用引入的额外翻转率与噪声地板不可区分"(窄表述)。

### Claims currently forbidden

- 任何"复用安全/不安全"的机制级结论(NATURAL_SELECTIVE_CONSUMPTION=UNRESOLVED);
- 任何 receiver-conditioned validity 的正/负结论(从未测量);
- "selective consumption 在真实 agent workflow 中不存在"(只审了 3 框架,CODE_ONLY);
- 任何具体加速/节省数字的 live 主张(actual skip 从未执行);
- "query-relative invalidation 不安全"(v1 已撤回);
- 用静态拓扑计数冒充运行时 coverage(raw invariants 明确 null)。

### 漂移诊断(§四第 7-8 问)

| 漂移 | 发生了吗 | 定性 |
|---|---|---|
| receiver-conditioned validity → exact caching | 部分。exact reuse 是当前唯一可操作的复用形态 | **合理收敛**,但论文若把 exact caching 当主贡献则是致命漂移(NEG-22 教训);它只能是证据阶梯的一级 |
| computation reuse → testbed audit | 是 | **合理收敛**——审计回答的是"复用主张的前提是否成立",与原问题因果相连;但必须以"为了测量复用"为叙事锚,否则退化为框架考古 |
| scientific question → project postmortem | 有风险 | 若论文按时间线写"我们试了什么失败了什么"即成 postmortem——**必须按科学问题组织**("怎样才能合法测量复用"),负结果作为证据而非情节 |
| mechanism study → measurement methodology | 是 | **合理且是唯一诚实选项**;机制层证据不存在 |

原始火花剩余量:约 25%。"复用有效性相对下游而定义"以两种弱化形式幸存:
(a) 审计协议中 delivery/projection/read 的 consumer 侧区分;(b) C3 中
ρ_blame vs ρ_outcome 的归因区分(定向 verifier 问题正是"损害是否由复用引入"
的 receiver 侧判定)。这足以在 related-work/discussion 中诚实叙述谱系,
不足以作为贡献主张。

### 当前材料是否已构成自洽论文?

**否。** 当前材料构成一篇论文的 60% 证据基座 + 0% 文本。缺的不是更多档案,
而是:(1) 一条被明确选定的主线;(2) manuscript;(3) 至少一个 live 实证锚点
(否则 reviewer 把三框架审计读成 n=3 的 position paper)。

### PAPER_TYPE

**Measurement + methodology 混合型论文**(含负结果与资格框架),若 Route C
实验成功则附一个 bounded confirmatory 实验;不是 negative-result paper
(负结果只是证据,不是身份),不是 position paper(有原始数据与预注册协议),
不是 benchmark paper(没有可发布 benchmark)。

---

## 2. Claim–Evidence Matrix

Evidence level:RAW_REPRODUCIBLE > CODE_CONFIRMED > DOCUMENTED > LITERATURE_ONLY > UNTESTED

| ID | Claim | 重要性 | 证据源 | 证据级 | 支持度 | 缺口 | 修补时间 | 截止前可完成? | 降级表述 |
|---|---|---|---|---|---|---|---|---|---|
| CL-1 | 文本 usage/等价代理不能判定复用效应(3 次独立失效) | **CORE** | C6 verdict_v2;NEG-11/16;identity 噪声地板配对 | RAW_REPRODUCIBLE | **SUPPORTED** | 需把三次失效整合为一张对照表(现散于两 repo) | 0.5 天(纯写作) | 是 | 无需降级 |
| CL-2 | 三大框架无公开 runtime trace 能确证 selective consumption | **CORE** | audits/selective_consumption(pinned commits + locators) | CODE_CONFIRMED | **SUPPORTED**(限定表述) | 只有 n=3;全部 CODE_ONLY;"外部 telemetry export 可能存在"已在 verdict 声明 | 无法在一周内扩大(冻结纪律) | — | 表述锁定为"在冻结 universe 与已发现公开 artifact 内" |
| CL-3 | Q0–Q3/QX 资格 rubric 是复用 testbed 的可操作判定框架 | **CORE** | protocol.md(冻结于结果前)+ 应用示范 | CODE_CONFIRMED | SUPPORTED | 只被应用一次(本审计);无第二个独立使用者 | — | — | 表述为"我们提出并示范",不称"已被验证" |
| CL-4 | naive 投机复用正收益窗 v≲8%;定向 verifier 扩至 ≤13.7% | SUPPORTING | gates/C3/v2 + v2_1(冻结 trace) | RAW_REPRODUCIBLE(重分析) | **PARTIAL** | s=0.144 来自单一任务族;ρ_blame 为 post-hoc;无 runtime verifier | live 实验可部分修补(Route C) | 部分 | 全部数字带"frozen-trace, conditional"标签 |
| CL-5 | 单 receiver 自然工况下复用额外翻转 ≈ 噪声地板 | SUPPORTING | NEG-01 六次 null | RAW_REPRODUCIBLE(旧 repo) | SUPPORTED(窄) | 数据在旧仓库;需要 artifact 打包 | 1 天(打包+manifest) | 是 | 限定"该扰动强度、单 receiver" |
| CL-6 | identifiability-first replay 是可信测量的必要前置 | SUPPORTING | D2 gate 97.37%;NEG-12/13/14 伪影链 | RAW_REPRODUCIBLE(旧 repo) | SUPPORTED | 方法论叙述散落;需正式算法化表述 | 1 天(写作) | 是 | — |
| CL-7 | exact reuse 在 live 执行中的实际节省/开销/一致性 | SUPPORTING(Route C 时) | 尚无 | **UNTESTED** | UNSUPPORTED | 需要 actual-skip 实验(模型调用) | 3–4 天(含授权、harness、run) | **有条件** | 失败则整节降级为"frozen-trace 上界分析" |
| CL-8 | 真实 agent workflow 存在天然选择性消费 | OPTIONAL | 无(UNRESOLVED) | UNTESTED | UNSUPPORTED | 强 testbed NOT_FOUND | 不可能(一周) | 否 | **禁止作为 claim;只能作 open problem** |
| CL-9 | 依赖结构在代码分析域天然稀疏 | OPTIONAL | c6_gate_24h(2 repos, AST) | RAW_REPRODUCIBLE | SUPPORTED(窄) | 仅结构前提 1;workflow 层未证 | — | — | 只作动机,不作贡献 |
| CL-10 | receiver-conditioned validity 存在/不存在 | (历史 CORE) | 无 | UNTESTED | UNSUPPORTED | 三代 testbed 均未触及 | 不可能 | 否 | **只在 discussion 作为未决问题** |

重点检查逐项回答(§五):

1. **identifiability-first 方法论够独立吗?** 够——它有可复述的操作序列
   (冻结 trace → identity 对照 → 伪影归因 → 才允许解释信号)和三次
   "没做会怎样"的反面案例(v7 Oracle 1.86pp 伪影)。是论文最强的方法贡献。
2. **trace-conditioned replay 是否形成清晰方法贡献?** 形成,但材料在旧 repo,
   需 1 天整理成正式一节 + artifact 引用。
3. **exact reuse 正结果只是窄观察吗?** 是。B3.5-I 跨轨迹=0、v8 coverage
   11.37% 全部来自 replay 内 exact match——exact reuse 只能作 baseline/阶梯,
   永远不能作贡献主张(NEG-19/22 红线)。
4. **K2/C6/C3 负结果有一般化价值吗?** K2=0 没有(单 canonicalizer 单协议);
   文本代理三次失效**有**(跨项目、跨代理类型的一致模式);C3 经济学符号地图
   有条件地有(公式一般,参数窄)。
5. **framework audit 是否系统?** 协议系统(预冻结、Q rubric、锁定计数规则),
   样本不系统(n=3)。诚实写法:深度换广度,每框架给出 exact locator 级证据。
6. **真实 outcome-level evidence?** 无(除 stage-1 Task B 测试信号)。
   Route C 的首要目标就是补这一项。
7. **actual computation skip?** 无。同上。
8. **net savings?** 无 live 数字;只有 frozen-trace 模型推算。
9. **可复现 artifact?** 半成品:fixtures+manifest+tests 在 repo,但完整统计
   依赖仓库外数据。发布前必须打包(P2)。
10. **fresh confirmatory evidence?** 无。Route C 是唯一一周内可获得的来源。
11. **novelty defense 够强吗?** 方法论轴上 NARROW 但可守(资格 rubric +
    三层证据区分未见占用者);机制轴上无防守可言(不得主张)。
12. **贯穿主线存在吗?** 存在但尚未被写出:"measure before you reuse"——
    从代理失效 → 资格框架 → 框架审计 → 成本模型 → (live 实证)。

---

## 3. PAPER_COMPLETENESS_SCORE

**总分 = 38 / 100**

| 维度 | 分 | 扣分原因 |
|---|---|---|
| Problem clarity | 68 | 测量问题本身清晰;但仓库从未把它写成一句论文级问题陈述,存在 postmortem 化风险 |
| Novelty | 45 | 方法论空位真实但窄;Sherlock/ToolCacheAgent/Prefill Notes 三面合围,任何机制表述都会撞车;audit n=3 易被贬为案例研究 |
| Method completeness | 62 | 资格 rubric、replay gate、协议纪律齐备;缺正式化表述与第二次独立应用 |
| Evidence completeness | 42 | 负结果与静态审计充分;live/outcome/TRACE_CONFIRMED 三类关键证据为零 |
| Experimental completeness | 18 | 本 repo 无任何新实验;全部为重分析与静态取证;无 confirmatory |
| Reproducibility | 50 | fixtures+SHA manifest+27 项测试通过(本轮复核);但全量统计依赖仓库外数据,artifact 未打包 |
| Writing readiness | 5 | 不存在 manuscript、abstract、图表;一切文本从零开始 |
| Reviewer defensibility | 40 | 每条 claim 的限定语已备好(罕见优点);但"n=3 code-only + 无新实验"是 AC 一句话就能拒的组合 |
| One-week finishability | 55 | 纯 B 路线一周可成文;含 Route C 实验则压线,取决于 Day 2/3 gate |

---

## 4. Reviewer-Style Adversarial Review

### Reviewer 1(Agent / multi-agent 方向)

- **Summary**:论文声称 agent 计算复用缺乏测量基础,审计三框架、给出资格
  框架与成本模型。
- **Strengths**:预注册纪律少见;三框架 locator 级证据扎实;文本代理失效
  结论对社区有直接警示价值。
- **Weaknesses**:没有任何真实 agent 运行;三个框架是 2026 年生态的很小
  切片;结论"trace 不存在"可能只反映作者没找到 telemetry export。
- **Major questions**:为什么不直接跑一个 AutoGen 应用导出 OTEL trace?
  (答案必须诚实:审计协议禁止制造证据——这个防守要写进正文。)
- **Missing experiments**:任一框架上的一次 instrumented run;live reuse 实验。
- **Novelty concern**:资格 rubric 像 checklist,不像贡献。
- **Score if submitted today**:**4/10(reject,borderline 之下)**。
- **升一档最小改动**:加入任何一个 live、outcome-validated 的复用测量点。

### Reviewer 2(Systems / incremental computation 方向)

- **Summary**:把 IVM/build-system 的正确性判据意识引入 agent 复用测量。
- **Strengths**:C3 成本模型干净(Δ/C_full = s − v − ρ(s+RB) 符号地图);
  对 delivery/projection/read 的区分在系统语义上是对的;诚实区分 exact 与
  contract 增量。
- **Weaknesses**:成本模型参数来自单一冻结任务族(s=0.144);没有实现任何
  系统;"actual skip 从未执行"意味着所有节省都是纸面推算。
- **Major questions**:s 和 ρ 在真实长链 workflow 中的分布?验证开销的
  实测值?
- **Missing experiments**:任何 end-to-end 的 skip-vs-recompute 对照。
- **Novelty concern**:成本模型是标准投机执行经济学的直接应用。
- **Score if submitted today**:**4/10**。
- **升一档最小改动**:一个 live 实验给出 (s, v, ρ) 的至少一组实测三元组。

### Reviewer 3(Empirical methodology / evaluation 方向)

- **Summary**:一篇关于测量效度的论文:代理失效、identifiability gate、
  资格框架。
- **Strengths**:这是最欣赏本文的审稿人——三次代理失效 + identity 噪声
  地板配对是教科书级的效度分析;预注册 commit 顺序可验证。
- **Weaknesses**:n=3 框架不足以支撑"生态普遍缺失"的口吻;负结果的
  一般化边界需要更谨慎;缺少"合格测量长什么样"的正面示范。
- **Major questions**:资格框架的 inter-rater 可靠性?第二个团队会得出
  相同 Q 级吗?
- **Missing experiments**:一个满足自家 rubric 的正面 demo(哪怕小)。
- **Score if submitted today**:**5/10(borderline)**。
- **升一档最小改动**:用自家 rubric 通过的装置完成一次正面测量示范——
  这正是 Route C 实验的定位。

### Area Chair 视角

- **最可能拒稿原因**:"三个 code-only 案例 + 冻结 trace 重分析 + 无新
  实验 = 加长版 position paper。"
- **最可能接受原因**:测量效度问题在 agent 效率文献中真实存在且无人
  系统处理;若有一个 live 实证锚点,三位审稿人的核心抱怨同时消解。
- **必须成为唯一主贡献的**:identifiability-first 测量框架(rubric +
  代理失效证据 + 成本模型作为其应用)。
- **必须删除或降级的**:receiver-conditioned validity 的任何残余主张
  (降到 discussion);C6' 强形式叙事;依赖稀疏性结果(降为一句动机);
  K2=0(降为脚注级窄负结果);任何"框架审计=生态结论"的口吻。

---

## 5. 结论摘要

- 当前项目的自我结论(C3=NEED_NEW_VERIFIER、C6=NOT_FOUND、C4=REJECTED、
  PRIMARY=NONE)**与底层证据一致,本审查确认采信**。
- 但"PRIMARY_CANDIDATE=NONE"是实验授权状态,不是论文判决。论文层面
  存在一条已经成立 60% 的主线(measure-before-reuse),它不需要 C6 强
  testbed,也不需要定向 verifier 存在——它只需要被写出来,并用一个
  有界 live 实验补上"正面示范"这最后一块。
- 裁决与路线见 `docs/FABLE5_FINAL_DECISION.md`;实验可行性见
  `docs/FABLE5_EXPERIMENT_FEASIBILITY_REVIEW.md`;摘要建议见
  `docs/FABLE5_ABSTRACT_SUBMISSION_RECOMMENDATION.md`;七天计划见
  `docs/FABLE5_SEVEN_DAY_PLAN.md`。
