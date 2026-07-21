# 重新开辟研究报告：通信即计算复用(Idea Landscape)

日期：2026-07-21
文献基础：本会话两次 paper-search(KV/状态复用 2021–2026,104 篇;IVM/SAC/PE/effects 1995–2026,131 篇),编号 [K#] 指第一份报告(allinone-kv-state-2021-2026.md),[I#]/[IM#] 指第二份报告(allinone.md)。
**诚实声明：所有 2025–2026 文献仅核实到标题/venue/arXiv-ID 级别，未逐篇下载全文与代码；未执行独立 scoop-check(§17 给出待查轴)。下文所有 novelty 判断均为"检索级",用于论文前必须逐篇核实。两次检索中 Semantic Scholar/OpenAlex/OpenReview 三源全程失败(403/401/鉴权),OpenReview 存在盲区。**

---

## 1. 原始火花的最小表述

> **上游计算方为完成自己的任务，已经对某些信息做过计算；下游计算方随后要面对相同或高度重叠的信息。下游是否必须从头重算，还是可以获得、转换、修复或合并上游已完成的计算——即使两边在字节层面并不相同？**

三个不可约的核心：

- 复用的对象是**计算**(已经花掉的 FLOPs/推理步/工具调用),不只是**信息**;
- 复用的有效性**相对于下游要用它做什么**而定义，不是绝对语义等价；
- "减少重复计算"是唯一判据，"复用是否安全"只是它的约束条件。

## 2. 反例地图(dossier 25 案例 → 7 类)

| 案例 | 分类 | 它真正否定/警告的窄命题 |
|---|---|---|
| NEG-01 六次 KV null | CONDITIONAL_COUNTEREXAMPLE | 仅否定"单一固定 receiver + 自然扰动强度下，KV 复用+当前 repair 引入可测额外错误"。**对"复用有风险、需要事前 validity 判定"是反例；对"复用安全"不是证明**;对投机复用方向(C3)反而是支持证据 |
| NEG-18 K2=0 | DIRECT_COUNTEREXAMPLE(窄) | 仅否定"K2 行多重集合规范化在 v8 D3 的 6-task/该 mutation 设计下有增量收益"。对更严肃 contract 只是 CONDITIONAL |
| NEG-25 static=runtime | DIRECT(窄)+ TESTBED_SPECIFIC | 否定"task_b.py 全上下文 prompt 能暴露稀疏依赖";对"稀疏依赖普遍存在"不置可否 |
| NEG-07 自由文本界面 | CONDITIONAL | 否定"在不改框架、consumer 是 LLM 的前提下实现 consumer 可见 typed contract"。**对 orchestrator 级 typed 元数据(不给 LLM 消费)不适用** |
| NEG-09 无 fan-out | TESTBED_SPECIFIC | mini-swe/SWE-agent 无真实多 consumer |
| NEG-14 cascade identity 破裂 | CONDITIONAL + DESIGN_WARNING | "上游同→下游同"在真实 serving 栈(批处理非结合性)+ 真实 FS 下不能默认成立;任何依赖该假设的测量需先自检 |
| NEG-17 噪声地板>信号 | CONDITIONAL + DESIGN_WARNING | 该 testbed/该扰动强度下信号测不出;不是"信号不存在" |
| NEG-08/11/12/15/16 | MEASUREMENT_FAILURE | 定义错位、difflib Oracle 无验证力、mtime 伪影、command-only 对齐、token 代理——都不能用于判断科学机制 |
| NEG-02/03/04/05/06/21 | ENGINEERING_FAILURE | harness 自伤与治理问题，与科学假设无关 |
| NEG-10/13/19/20/22/23/24 | DESIGN_WARNING | 因果链未闭合、非确定 readdir、exact 与 contract 增量必须分报、post-hoc 候选隔离、概念漂移、cluster 统计、outcome 必须验证 |
| —(针对原始火花本身) | **无任何 DIRECT_COUNTEREXAMPLE** | dossier 自己的结论：原始问题一次都没被真实测量过，更未被证伪 |

**从反例地图提炼的三个战略判断**(整个报告的地基):

- **J1:NEG-01 的正确读法是把"事前 validity 判定"的实用动机杀死了。** 单 receiver、自然工况下，复用几乎从不出错(错误率与噪声不可区分)。为一个测不到的问题设计精密判定机制，是 Route A+ 后期形式化的根本错位。两个出路:(a) 去错误真实存在的困难场景(跨 receiver、跨模型、外部状态变更后);(b) 放弃事前判定，改投机+验证+回退——低错误率恰好让投机策略期望收益最大。
- **J2:现象必须先于机制存在。** NEG-25/07/09 都是"testbed 不具备暴露目标现象的结构前提"。任何新方向的第一道工序(24 小时、零模型调用)是结构自检：候选场景里稀疏依赖、多 consumer、非平凡 mutation 是否真实存在。
- **J3:validity 判定的位置可以移动。** Route A+ 卡在"LLM 消费自由文本 → typed contract 无处安放"(NEG-07)。但 validity 判据可以放在 orchestrator/系统层(消费元数据，不给 LLM),或改为事后验证(C3),或换成路由决策(C2)——NEG-07 只封死其中一格。

## 3. 研究空间的主要设计轴

| 轴 | 取值 |
|---|---|
| A1 复用对象载体 | latent/KV 张量 · 压缩上下文 · 自由文本 artifact · 结构化 artifact(带 schema) · 执行记录(trace/plan) |
| A2 validity 判据位置 | producer-side(内容寻址) · consumer-side(receiver/use-conditioned) · 系统-side(oracle/verifier) · 无判据(结构保证/投机) |
| A3 复用操作 | 直接 · 转换/翻译 · 修复(部分重算) · 合并 · 投机+回退 · 重路由(搬任务不搬状态) |
| A4 consumer 结构 | 单 receiver 串行 · 真实多 consumer fan-out · 共享 substrate · 单 agent 多阶段(MAS 的最小归约) |
| A5 正确性要求 | exact equivalence · from-scratch consistency(≡ 全量重算) · error budget · outcome-only |
| A6 正确性判定时机 | 事前(判定) · 事后(验证+回退) · 构造时(形式保证) |
| A7 实验对象 | 模型内层(KV/激活) · agent 消息层 · orchestrator/工作流层 · 系统/调度层 |

Route A+ 后期形式化 = A1 文本 × A2 consumer-side × A3 直接 × A4 单 receiver × A5 exact × A6 事前 × A7 消息层——恰好是 NEG-01/07/09/25 全部咬住的格子。**换轴就是换方向。**

## 4. Idea cards(12 个，实质互异)

**C1 共享前缀计算基底(M+E 族,baseline 锚)**
①同模型多分支天然共享前缀 KV，复用在分支点之前免费、之后不可能;②前缀 KV;③orchestrator/各分支 agent;④多 agent 重复 prefill 相同上下文;⑤直接复用;⑥结构保证(causal mask),无 validity 问题;⑦否(单模型分支即可);⑧是;⑨否;⑩否;⑪火花的"trivially solved"子集;⑫即 B3.5/exact 档;⑬NEG-19/22;⑭它就是 exact cache 本身，旧反例全部适用;⑮Hydragen [IM5]、TokenDance [K30]、PolyKV [K32]、vLLM [IM1];⑯**高——已被覆盖**;⑰多租户 serving;⑱无新实验可做;⑲无(已知);⑳无;㉑-㉓不适合作为方向，仅作 baseline;㉔无;㉕不是科学问题是工程问题。

**C2 计算路由：把任务搬到状态所在处(F 族)**
①不回答"状态搬给 receiver 是否有效"——把请求路由给已持有相关计算状态的 worker，让"同一 receiver"假设自动成立，消解 receiver-conditioned validity;②驻留的 KV/上下文 + 亲和性元数据;③state-holding worker / 新请求;④多 worker 各自重复 prefill 相同领域上下文;⑤重路由;⑥路由决策的正确性(亲和度估计),错误代价=未命中(退回重算),无正确性风险;⑦否;⑧是;⑨否;⑩否;⑪保留火花但把"传递"换成"会合";⑫完全绕开 Route A+ 的判定框架;⑬NEG-01/07/18 均不适用(无 validity 判定);⑭它绕开而非依赖旧失败假设;⑮CacheGen [IM3]、prefill/decode 分离、TraCT [K25]、locality-aware 调度;⑯中——serving 层 cache-aware routing 已有,**agent 语义级亲和路由(按任务语义而非前缀匹配)较空**;⑰多实例 agent serving;⑱路由命中率×收益 vs 搬运成本,24h 可用 trace 统计上界;⑲"validity 问题可以被架构消解"是个真实贡献;⑳证明语义亲和估计做不准(信息价值中);㉑trace 统计可行;㉒原型可行;㉓中(偏系统);㉔需要一个像样 serving 栈;㉕可能沦为工程优化，科学增量有限。

**C3 投机复用 + 低成本验证 + 回退(I 族)**
①既然 NEG-01 表明复用错误率接近噪声地板，就不该做事前判定，而该**默认复用、并行验证、罕见回退**——validity 从事前谓词变成事后系统机制;②任意已完成计算(消息/KV/artifact);③上游阶段/下游阶段;④事后发现输入已变导致全链重算;⑤投机+回退;⑥回退率 ρ 与 verifier 成本 v、重算成本 c 的决策边界：投机优于判定 ⟺ ρ·c < 判定成本+误判损失;⑦否(单 agent 多阶段即可);⑧否;⑨否;⑩否;⑪火花的"执行语义"版;⑫把 Route A+ 的 Exact/Repairable/Invalid 三档从判定标签变成执行路径(投机命中/修复回退/全回退);⑬NEG-01(转为支持证据)、NEG-24(verifier 必须 outcome 级)、NEG-14(回退判定不能依赖 cascade identity);⑭核心机制(投机)恰被六次 null 间接支持;回退正确性依赖 outcome oracle，不依赖任何文本 heuristic;⑮speculative execution(OS/CPU 老范式)、speculative decoding(推理加速)、ToolSandbox [IM8](outcome milestone);⑯**低-中**——agent 级"投机复用+outcome 回退"未在两次检索中出现直接覆盖(需 scoop-check);⑰有真实测试当 outcome oracle 的代码 agent;⑱在冻结 trace 上重分析：投机复用的理论回退率是否 ≪100%(零模型调用,24-48h);⑲把"agent 复用"从缓存问题重新表述为乐观并发问题，理论+系统双贡献;⑳若回退率≈噪声且 verifier 成本高→证明"无脑复用+从不验证"就是最优，本身就是强零结果;㉑可行;㉒可行;㉓高;㉔outcome oracle 的工程(装依赖跑测试,NEG-24 的旧坑);㉕被审稿人说成"try-catch 改名"——必须给出决策理论边界而非只有系统。

**C4 Repairable reuse 的独立定义与边界(C 族)**
①三档中的 Repairable 档从未被独立测量：外部状态 mutation 后，只重算受影响的 span/subgraph 能恢复多少正确性、在什么 mutation 结构下彻底失效;②KV/上下文中受影响的子段;③同一 agent 的过去自己/现在的自己;④局部变更导致全量 prefill;⑤修复(选择性重算);⑥mutation 的"影响半径"是否局部化——可修复 ⟺ 影响可被限制在子结构内;⑦否;⑧是(KV 层);⑨否;⑩否;⑪火花最贴肉的一档;⑫阶段1 repair 的遗产，但当年只测风险没测修复能力;⑬NEG-01(CONDITIONAL：测的是风险非修复力)、NEG-18(K2 是文本浅层规范化，与 KV 层 repair 无关);⑭CacheBlend 在 RAG 场景有正结果 [IM4],说明机制可行;开放的是 agent 场景的 mutation 结构是否可修复;⑮CacheBlend [IM4]、KVPR [K3]、dKV-Cache [K12];⑯中——差异化必须落在"mutation 来自外部状态变更/不同 receiver 需求",而非 CacheBlend 的"拼接位置变化";⑰代码 agent(文件被外部编辑)、检索 agent(语料更新);⑱合成正对照先行(NEG-18 纪律):构造理论上必须可修复的 case，验证选择性重算恢复 from-scratch 输出;⑲给出 Repairable 档的第一个独立刻画(什么可修复、什么不可);⑳若影响从不局部化→证明 Repairable 档为空集，三档坍缩为两档——同样有价值;㉑可行(合成 microbenchmark);㉒可行;㉓高;㉔需要本地模型+KV 操作能力;㉕与 CacheBlend 的差异化论证是最大科学风险(必须 scoop-check 其后续引用)。

**C5 跨模型 latent/KV 翻译(B 族，高风险)**
①producer 与 receiver 不同模型时，把 KV/hidden state 翻译到 receiver 的表示空间，实现异构 agent 间的计算传递;②KV/激活张量;③异构模型的 agent 之间;④异构级联/多专家系统每个模型各自重读全文;⑤转换/翻译;⑥翻译保真度(跨 tokenizer/架构时最脆);⑦否;⑧**否(这正是卖点)**;⑨可能需要小投影层训练;⑩否;⑪火花的最强形式;⑫Route A+ 完全没碰;⑬无直接旧反例(阶段1 全是同模型);⑭旧反例体系不适用——这是新假设空间，但也意味着没有旧资产兜底;⑮DroidSpeak [K5]、C2C [K-M10,uncertain]、KVShare [K4];⑯**高——DroidSpeak 已做 cross-LLM KV 共享(2024),需逐篇核实其范围**;⑰异构模型级联(小模型检索→大模型生成);⑱翻译后 receiver 下游输出 vs from-scratch 的 from-scratch consistency 双跑;⑲异构计算传递的第一原则结果;⑳证明跨表示空间的计算传递本质有损且不可修复——强负结果;㉑不可行(需训练);㉒勉强(复用 DroidSpeak 代码);㉓中-高;㉔工程最重(双模型栈+训练);㉕novelty 撞车 + 可能需要训练数据，双重风险。

**C6 带 provenance 的结构化 artifact 复用(G+N 族,IVM/build 范式整套迁移)**
①agent 的工具/检索/分析产物是带输入依赖(provenance)的结构化节点，依赖未变→直接复用，依赖变更→IVM 式增量维护;**validity = provenance 检查,放在 orchestrator 层,不给 LLM 消费(绕开 NEG-07)**;②结构化 artifact + 依赖边;③pipeline 上游节点/下游节点与 orchestrator;④重复检索、重复代码分析、重复构建中间结果;⑤直接复用 + 增量维护(delta);⑥from-scratch consistency:复用结果 ≡ 全量重算;**多 consumer 维度 = query-relative:同一 artifact 对不同下游查询有不同 validity**(answering-queries-using-views 的移植);⑦否(DAG workflow 即可，多 agent 是自然扩展);⑧否;⑨否;⑩是(工具调用天然提供 provenance 边);⑪火花的"artifact+依赖"版;⑫TraceBuild 的正统续作，但修复其 prompt 设计;⑬NEG-25(最大威胁：必须先自检依赖稀疏)、NEG-19(exact 与增量分报)、NEG-07(绕开);⑭NEG-25 只证伪了一个 prompt 设计;选天然稀疏依赖的 workflow(monorepo 式代码库、数据 pipeline)即不依赖已失败假设;⑮Build Systems à la Carte [IM8]、Noria [IM4-2nd]、DBSP [I9]、Durable Intermediate Artifacts/Execution Lineage(旧 scoop-check 近邻，需重新核实);⑯中——agent 场景的 provenance memoization 有空隙，但"普通 build cache 改名"风险真实存在，必须用 query-relative/多 consumer 维度守住差异;⑰天然 DAG 型 workflow(代码库分析、数据管道、多 agent 框架 trace);⑱24h 零模型自检：候选 workflow 的 static vs runtime 依赖是否非平凡(NEG-25 纪律的直接应用);⑲把 IVM/build 的完整实验范式(stable names + 双跑 oracle + from-scratch 判据)第一次严格落到 agent 计算上;⑳若真实 agent workflow 依赖全部稠密→证明"稀疏复用"在 agent 层是伪需求，改写问题定义;㉑可行;㉒可行;㉓**最高**(理论+系统+范式迁移三者齐备);㉔找到天然稀疏且真实的 workflow;㉕退化为普通缓存改名的风险。

**C7 Workflow 特化 / 部分求值(H 族)**
①固定 agent 角色+工具序列后，workflow 可对"任务类型"做 partial evaluation：不变部分预算好，只对新输入重算;②特化后的 prompt/计划/KV;③框架/任务实例;④同类任务重复执行相同规划;⑤转换(特化)+直接复用;⑥Futamura 一致性：特化结果 ≡ 原 workflow 跑新输入;⑦否;⑧是;⑨否;⑩否;⑪火花的"编译"版;⑫无交集;⑬无直接反例;⑭新空间;⑮Prompt Cache [K20]、A Plan Reuse Mechanism for LLM-Driven Agent [K13]、partial evaluation 谱系 [I66][I94];⑯**中-高——[K13] 已做 agent 计划复用(2025,需核实范围)**;⑰重复任务型的 agent 服务;⑱特化前后输出一致性双跑;⑲中;⑳中;㉑可行;㉒可行;㉓中;㉔与 prompt cache 的边界要说清;㉕incremental 风险。

**C8 Effect 标注的 agent 消息(K+N 族)**
①每条消息/artifact 自动携带 effect 标注(读了哪些状态、写了哪些状态)——由工具调用记录自动推导，无需 LLM 消费 typed 对象;下游/orchestrator 用 effect 交集判断复用有效性;②effect 标注 + artifact;③producer/orchestrator;④无法判断旧结果是否受状态变更影响→保守全重算;⑤直接复用(条件化);⑥effect 标注的完整性与精确性(over-approx 保守、under-approx 危险);⑦否;⑧否;⑨否;⑩是(effect 从工具接口推导);⑪typed effects [I3][I69][I70] 向 agent 的移植;⑫typed contract 的去 LLM 化变体;⑬NEG-07(绕开：标注给系统不给人)、NEG-18(K2 的教训：effect 推导必须非平凡);⑭关键差异：标注自动推导且 consumer 是 orchestrator;⑮effects as capabilities [I3]、ChainCaps [K45](能力衰减，相邻);⑯中;⑰工具型 agent;⑱effect 标注能否自动推导且非平凡(24h 静态分析);⑲把 effect system 第一次用作 agent 复用的 validity 基础;⑳effect 标注恒为"读写一切"→证明该抽象无区分力;㉑可行;㉒可行;㉓中-高;㉔工具接口异构;㉕可能恒退化(标注无信息量)。

**C9 单 agent 多阶段 = MAS 最小归约(用户提示方向)**
①阶段间 handoff 形式(全文/summary/压缩表示/KV)决定下游重算量;把"多 agent 通信"归约为"单 agent 阶段拼接",在最可控环境里隔离核心现象;②阶段间传递的上下文表示;③阶段 i/阶段 i+1;④每阶段重新 prefill 全部历史;⑤直接/转换(压缩);⑥下游任务表现不降级为约束;⑦**否(这是优点)**;⑧是;⑨否;⑩否;⑪火花的可控归约;⑫阶段1 Task B 的精神续作;⑬NEG-01(同型，但是 CONDITIONAL)、NEG-25(prompt 设计教训);⑭可控归约允许自由设计 handoff 结构，绕开 testbed 不匹配;⑮context compression/handoff 文献(未在本轮检索重点覆盖，需补检);⑯中——context compression 是拥挤领域,"计算复用"视角的差异化需论证;⑰长程单 agent 任务(代码、深度调研);⑱三档 handoff(全文/summary/KV)×下游质量×成本;⑲给出 MAS 通信的受控基线理论;⑳中;㉑可行;㉒可行;㉓中;㉔与"压缩文献"区分;㉕可能只是 compression 改名。

**C10 误差预算内的近似复用(J 族)**
①放弃零错误，把复用安全性表述为端到端误差预算的分配问题;②任意中间结果;③任意上下游;④保守策略导致的重算;⑤直接复用(带预算);⑥误差传播模型(预算如何在 pipeline 上分配);⑦否;⑧否;⑨否;⑩否;⑪火花的统计版;⑫阶段1 D1→D3 代理问题的理论化;⑬NEG-01(D1 不预测 D3,直接威胁误差模型的可估计性);⑭**NEG-01 是近乎 DIRECT 的反例：在本项目测过的设置里，代理误差信号与下游翻转不相关**;⑮MeanCache [K88]、Martingale MCP 分析 [K21];⑯**高——[K21] 已做 MCP 信息保真度的鞅分析(2026)**;⑰—;⑱—;⑲—;⑳—;㉑-㉓不推荐;㉔—;㉕代理信号不预测 outcome(已被 NEG-01 咬过)+novelty 撞车。

**C11 复用正确性理论:from-scratch consistency 的形式化(N 族反向)**
①不提出新机制，提出判定框架：agent 计算复用的正确性 = 复用执行 ≡ from-scratch 执行，并把各领域的 consistency 判据(IVM、DBSP、build correctness、observational equivalence)统一成分类学+可检验判据;②理论对象(执行语义);③—;④—;⑤—;⑥—;⑦—;⑧—;⑨—;⑩—;⑪火花的"理论底座";⑫给 Route A+ 的 Exact/Repairable/Invalid 一个迟到的形式化;⑬无(理论工作天然规避实证反例);⑭—;⑮DBSP [I9]、Build Systems à la Carte [IM8]、Levy et al. [IM6]、determinacy [I42];⑯低(理论综合类);⑰—;⑱—;⑲成为后续所有实证工作的引用点;⑳—;㉑不可行(理论需慢工);㉒框架可成形;㉓高(但发表渠道窄，适合作为 C6/C3 论文的理论节而非独立论文);㉔—;㉕"综述化"风险——必须产出新定理(如：何时 query-relative validity 可判定)而非只有分类。

**C12 执行去重:orchestration 层的语义重复合并(O 族反向)**
①真正的浪费不是"没传状态",而是同一计算被独立发起多次——在 orchestrator 层识别语义重复的子任务，执行一次、广播结果;②子任务执行本身;③orchestrator/多个发起方;④多 agent 独立发起相同检索/分析;⑤合并+广播;⑥重复识别谓词的精度(语义级，非字节级);⑦是(真 fan-out);⑧否;⑨否;⑩否;⑪火花的"需求侧"版;⑫无交集;⑬无直接反例;⑭—;⑮语义缓存 [K88][K89]、TokenDance [K30];⑯**高——与语义缓存边界模糊**;⑰多 agent 并发框架;⑱真实多 agent 负载中语义重复率测量(24h 统计);⑲若重复率高则是强动机论文;⑳重复率低→直接杀死方向(干净利落);㉑可行(纯统计);㉒可行;㉓中;㉔需要真实多 agent 负载;㉕"普通缓存改名"风险最高。

## 5. 跨领域完整实验范式迁移表

| 来源领域 | 计算对象 | 节点稳定身份 | 依赖暴露 | mutation 构造 | correctness oracle | 正/负例产生 | 机制失败 vs 测量失败 | 在 Agent 中不成立的前提 | 能否整套搬 |
|---|---|---|---|---|---|---|---|---|---|
| IVM/物化视图 [IM6][IM7][I9] | 关系视图 | 视图定义(声明式) | SQL 代数 | 基表 insert/delete | 增量维护结果 ≡ 全量重算 | 更新负载规模 × 视图复杂度 | 双跑对照天然分离 | LLM 计算无声明式代数;mutation 不总是离散 | **能——C6 主干**;需把"视图"换成"工具 artifact+provenance" |
| Self-adjusting computation / Adapton [IM1][IM2][I23] | 函数式计算图 | modifiable references(trace 内稳定名) | 读写 trace 自动记录 | edit-sequence 基准 | change propagation ≡ from-scratch | 编辑序列(合成+真实) | oracle 与机制独立实现 | agent 计算含外部副作用与采样 | **能——C6/C3 的实验模板**(edit-trace + 双跑) |
| Build systems(à la Carte [IM8];Shake;red-green/Salsa) | 构建目标 | 稳定键(文件路径→内容 hash/stable names) | 声明式依赖+动态发现 | 文件编辑 | rebuilder ≡ clean build | 真实项目编辑历史 | 双跑 | agent "输入"含非确定性模型输出(NEG-14 警告) | **能——from-scratch consistency 判据直接搬** |
| Partial evaluation [I66][I94] | 程序 | static/dynamic 输入划分 | 绑定时间分析 | 输入变化 | Futamura:residual ≡ 原程序跑剩余输入 | 划分×基准程序 | 一致性可机械检验 | LLM 无绑定时间分析 | 部分能——C7 的 oracle |
| Noria 部分物化+upquery [IM4-2nd] | 数据流算子状态 | 算子图节点 | 数据流图 | 写负载 | 查询结果 ≡ 全物化基线 | 读写混合负载扫描 | 端到端对照 | agent 无显式数据流图 | 结构能——C6 的 consumer-specific 物化灵感 |
| Answering queries using views / determinacy [IM6][I42] | 查询 | 视图集合 | 查询语法 | — | 可重写性判定 | 查询/视图对 | 可判定性结论 | LLM"查询"是自然语言 | 理论能——C11 的 query-relative 内核 |
| Effect systems [I3][I69][I70] | 带效应计算 | 类型/效应标注 | 类型推导 | — | 类型健全性 | — | 形式证明 | agent effect 需从工具调用自动推导，可能恒退化 | 部分能——C8,先过 24h 资格门 |
| Speculative execution(体系结构/OS) | 指令/事务 | 投机窗口 | 运行时检测 | 错误预测 | 提交结果 ≡ 顺序执行 | 预测准确率扫描 | 回退机制保证正确性天然分离 | agent 回退成本非均匀、outcome oracle 贵 | **能——C3 主干**;需重建成本模型 |
| Provenance(数据库) | 查询结果 | why/where provenance | 查询执行 | 基表变更 | lineage 重放 ≡ 原执行 | — | 重放对照 | agent 工具调用即天然 lineage | **能——C6 的依赖边来源** |
| CRDT/分布式共享状态 | 副本状态 | 副本 ID+操作 | 操作日志 | 并发写 | 收敛性 | 并发调度 | 模型检查 | agent 状态非交换律操作 | 弱——仅作对照 |
| Memoization under effects | 函数调用 | 参数+效应闭包 | 效应分析 | 效应发生 | 重算对照 | — | 双跑 | 即 C8 的理论版 | 并入 C8 |
| Program slicing | 程序语句 | PDG 节点 | 数据/控制依赖 | 变更语句 | slice 执行 ≡ 原程序(投影下) | 变更点扫描 | 投影等价 | agent "程序"是 trajectory，非静态代码 | 概念能——C4 的"影响半径"判据来源 |

## 6. 候选 × 旧反例关系矩阵

(D=DIRECT,C=CONDITIONAL,T=TESTBED,M=MEASUREMENT,E=ENGINEERING,W=DESIGN_WARNING,S=转为支持证据,—=无关)

| NEG 组 | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 | C11 | C12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| NEG-01 六次 null | — | — | **S** | C | — | — | — | — | C | **≈D** | — | — |
| NEG-07 文本界面 | — | — | — | — | — | 绕开 | — | 绕开 | — | — | — | — |
| NEG-09 无 fan-out | T | — | — | — | — | T(选 DAG 即避) | — | — | — | — | — | T |
| NEG-14 cascade 破裂 | W | W | W(回退判定处) | W | — | W | W | W | W | — | — | — |
| NEG-18 K2=0 | — | — | — | 纪律(合成正对照) | — | 纪律 | C | C | — | — | — | C |
| NEG-19 exact≠增量 | W | — | W | — | — | **纪律(强制分报)** | W | W | W | — | — | W |
| NEG-24 outcome 未验 | — | — | **纪律(verifier=outcome)** | 纪律 | — | 纪律 | — | — | 纪律 | — | — | — |
| NEG-25 static=runtime | — | — | — | — | — | **C(首要威胁)** | — | C | W | — | — | — |

## 7. 一手文献与 novelty 冲突(检索级，未逐篇全文核实)

| 候选 | 最近邻(本轮检索) | 冲突度 | 需核实内容 |
|---|---|---|---|
| C1 | TokenDance [K30, 2026]、PolyKV [K32, 2026]、Hydragen [IM5, 2024]、vLLM [IM1, 2023] | **致命** | 已覆盖共享前缀 fan-out，无剩余科学问题 |
| C2 | CacheGen [IM3, SIGCOMM'24]、TraCT [K25, 2025]、RTT-vs-Bandwidth [K48, 2025] | 中 | serving 层 KV 路由已有;agent 语义级亲和路由需 scoop-check |
| C3 | speculative decoding(范式);ToolSandbox [IM8, 2024](outcome milestone) | **低-中(最有空间)** | "agent 级投机复用+outcome 回退"未见直接命中;需专项 scoop-check |
| C4 | CacheBlend [IM4, 2024]、KVPR [K3, ACL'25 Findings] | 中 | CacheBlend 的 mutation 类型边界;其后续工作是否已进 agent 场景 |
| C5 | DroidSpeak [K5, 2024]、C2C [K-M10, 2025, uncertain]、KVShare [K4, 2025] | **高** | DroidSpeak 的 cross-LLM 覆盖范围全文核实 |
| C6 | Durable Intermediate Artifacts / Execution Lineage(旧 scoop-check 近邻)、Noria [IM4-2nd, OSDI'18]、DBSP [I9, 2022] | 中 | 前两篇与本方向的四轴比较需重新生成(NEG-25 纪律：旧数字作废) |
| C7 | A Plan Reuse Mechanism [K13, 2025]、Prompt Cache [K20, MLSys'24] | 中-高 | [K13] 全文核实 |
| C8 | Effects as capabilities [I3, ICFP'20]、ChainCaps [K45, 2026] | 中 | ChainCaps 是否已覆盖 effect 式 agent 约束 |
| C9 | context compression 文献(本轮未重点检索) | 未定 | 需补检 |
| C10 | Martingale MCP [K21, 2026]、MeanCache [K88, IPDPS'25] | **高** | [K21] 已做误差传播理论 |
| C12 | MeanCache [K88]、TokenDance [K30] | 高 | 语义去重边界 |

## 8. Top 3 候选

**Landscape matrix(先看全景，再收敛):**

| 卡 | 载体 | validity 位置 | 时机 | consumer 结构 | 新颖空间 | 一周可行 | 论文潜力 |
|---|---|---|---|---|---|---|---|
| C1 | KV | 无(结构保证) | 构造时 | fan-out | 无 | — | 无 |
| C2 | KV+元数据 | 无(路由消解) | 事前(调度) | 多 worker | 中 | 中 | 中 |
| **C3** | 任意 | 系统-side | **事后** | 单/多皆可 | **高** | **高** | 高 |
| **C4** | KV 子段 | producer-side | 事前+修复 | 单 | 中-高 | 高 | 高 |
| C5 | KV 翻译 | producer-side | 事前 | 异构 | 中 | 低 | 中-高 |
| **C6** | 结构化 artifact | 系统-side(query-relative) | 事前(provenance) | DAG/多 consumer | **高** | 高 | **最高** |
| C7 | 特化产物 | 构造时 | 构造时 | 单 | 中 | 高 | 中 |
| C8 | artifact+标注 | 系统-side | 事前 | 单/多 | 中 | 高 | 中-高 |
| C9 | 上下文表示 | outcome | 事后对照 | 单(归约) | 中 | 高 | 中 |
| C10 | 任意 | 统计 | 事前 | 任意 | 低 | — | 低 |
| C11 | 理论 | — | — | — | 中 | 低 | 高(窄) |
| C12 | 执行 | 系统-side | 事前(合并) | 真 fan-out | 低-中 | 高 | 中 |

**Top 3:C3(投机复用)、C6(provenance artifact 复用)、C4(Repairable 边界)。**

**Adversarial comparison:**

| # | 问题 | C3 | C6 | C4 |
|---|---|---|---|---|
| 1 | 保留火花? | 是(计算不重复执行，靠投机而非判定) | 是(artifact 计算跨节点复用) | 是(最贴"部分计算传递") |
| 2 | 普通缓存改名? | 否——核心是回退机制与决策边界 | **有风险**——必须守住 query-relative/多 consumer 维度，否则=build cache | 否——repair≠lookup |
| 3 | 已被覆盖? | 检索级未见;需 scoop-check | Durable Artifacts/Lineage 近邻，差异在 LLM consumer+query-relative | CacheBlend 最近邻，差异在 mutation 来源与影响半径刻画 |
| 4 | 需人为制造正例? | 否(回退率天然存在，只是低) | 风险中——依赖稀疏 workflow 必须天然存在(NEG-25) | **有**——需合成正对照先行，再上真实 mutation |
| 5 | 旧反例重演? | NEG-01 反转支持;NEG-24 是主要纪律 | NEG-25 是首要威胁;NEG-19 强制分报 | NEG-01 不构成威胁(当年没测修复力) |
| 6 | 24-48h 停/走信号? | **有(冻结 trace 重分析，零模型)** | **有(依赖稀疏自检，零模型)** | 有(合成正对照) |
| 7 | 升级路径自然? | trace 统计→半受控→真实 agent+理论 | 自检→DAG 原型→多 consumer→理论 | 合成→梯度→真实 mutation→三档理论 |
| 8 | 正结果成贡献? | 是(新执行语义+边界定理) | 是(范式迁移+系统+形式化) | 是(Repairable 档首次刻画) |
| 9 | 零结果有信息? | 强("无脑复用最优"也是答案) | 中(依赖稠密=问题重定义) | 强(三档坍缩为两档) |
| 10 | 最难审稿意见 | "不就是 try-catch/乐观并发?"→必须给决策理论 | "不就是 build cache?"→必须证明 LLM consumer 与 query-relative 的新意 | "不就是 CacheBlend 换场景?"→必须给出 CacheBlend 没有的 mutation 分类学 |

## 9. 高风险高回报候选

**C5(跨模型 latent/KV 翻译)**。若成，是火花的最强形式(异构 agent 间直接传递计算);风险：DroidSpeak 撞车 + 需要训练 + 工程最重。处理方式：不启动，先做 scoop-check(C5 轴),若 DroidSpeak 留下明显空档(跨 tokenizer/跨架构、agent 场景 validity 分析)再以一个月预算进入。

## 10. 一周最优候选

**C3(投机复用)**。理由：24-48h 停/走信号完全零模型调用(复用旧冻结 trace，符合 NEG-01 的 YES_AS_CONTROL 判定);一周实验只需单 agent 两阶段 workflow + 现成 outcome oracle(测试/精确答案),无新基础设施。

## 11. 完整论文最优候选

**C6(provenance artifact 复用)**。理由：唯一同时具备(a)可整套迁移的成熟实验范式(IVM/build 的 stable names + 双跑 oracle + from-scratch 判据)、(b)明确未占据的科学空位(agent 计算图上的 query-relative validity)、(c)理论(C11 可作为其理论节)、(d)系统原型四个支柱的候选。

## 12. 建议放弃的候选

**C1(共享前缀基底)**:它是火花的"已解决子集"——TokenDance/PolyKV/Hydragen/vLLM 已完整覆盖，且其 validity 由结构自动保证，不存在未回答的科学问题;保留为 baseline，不值得作为研究方向。
**C10(近似复用误差预算)**并列放弃：NEG-01 近乎直接反例(代理误差信号不预测下游 outcome)+ [K21] Martingale 分析已占据理论位置。
(C12 不建议放弃但建议降级：先只做 C12 的 24h 重复率统计——若真实多 agent 负载语义重复率低，它自我处决;若高，它成为 C6 的动机章节。)

## 13. Top 3 的分级实验计划

**C3 投机复用**
- **24h 结构资格(零模型)**:重分析旧冻结 trace(E0/Task B,NEG-01 资产):标注每个"理论复用点",统计投机复用后下游结果与 from-scratch 的分歧率(=理论回退率 ρ)。停/走:ρ 显著 <50% 且存在低成本 verifier(测试/精确答案)→走。
- **一周**:单 agent 两阶段 workflow(代码修复，真实测试作 outcome oracle);producer 输出做受控强度梯度 mutation;arm:全重算 / 投机复用+验证+回退 / 无脑复用。测：成本-错误曲线、回退率。
- **一个月**:决策理论形式化(ρ、verifier 成本 v、重算成本 c 的三方边界，给出"何时投机优于判定"的充分条件);2-3 种任务类型;discovery/held-out 切分;投 workshop。
- **完整论文**:真实多阶段 agent(SWE 类，装好依赖跑真测试——偿还 NEG-24 旧债);regret 界分析;系统实现;与事前判定基线(C8 式 effect 判定)正面比较。

**C6 provenance artifact 复用**
- **24h 结构资格(零模型,NEG-25 纪律的直接应用)**:对 2-3 个候选自然 workflow(monorepo 代码分析、数据 pipeline、某真实多 agent 框架的公开 trace)测 static vs runtime 依赖是否非平凡、依赖是否稀疏。停/走：至少一个 workflow 稀疏且真实→走;全稠密→退回 C3 主线。
- **一周**:半合成 producer/consumer DAG(真实工具调用、合成拓扑):stable-name + provenance memoization + from-scratch 双跑 oracle;**coverage 强制拆分为 exact 命中与 provenance 增量两字段(NEG-19 纪律)**;正确性 = ≡ from-scratch。
- **一个月**:真实 workflow 接入;**query-relative 维度上线**:同一 artifact 配 2+ 种下游查询，验证"同一 mutation 对不同 consumer 不同 verdict"(这是 dossier §8-1 从未被测过的核心结构的首次真实测量);IVM 式 delta 维护 vs 全量重算对照。
- **完整论文**:形式化(C11 作为理论节:agent 计算图上 query-relative validity 的可判定性条件)+ 系统 + 与 Noria/DBSP/Build-à-la-Carte 的对照分析 + 真实多 consumer 实证。

**C4 Repairable 边界**
- **24h 结构资格**:合成正对照(NEG-18 纪律):构造"理论上必须可修复"的 KV 层 case(共享长前缀+中段局部替换),验证选择性重算能恢复 from-scratch 输出。失败→机制基础不成立，直接停。
- **一周**:mutation 类型梯度(位置 × 范围 × 语义角色)× repair 比例，画"可修复边界"曲线;from-scratch oracle 双跑。
- **一个月**:真实外部状态变更场景(代码 agent 文件被外部编辑、检索 agent 语料更新),fresh-task 确证;与全复用/全重算三档对照。
- **完整论文**:Repairable 档的刻画定理(什么 mutation 结构可修复)+ 与 CacheBlend 的边界划清(其后续引用 scoop-check)+ agent 场景实证。

## 14. Top 3 的 falsification criteria

- **C3**:若理论回退率 ρ 在冻结 trace 上 ≈100%(复用几乎总是错),或低成本 outcome verifier 不存在(验证成本 ≈ 重算成本),或决策边界分析显示"投机在所有合理参数区间都劣于无脑复用"——三者任一成立即证伪。
- **C6**:若所有候选自然 workflow 依赖稠密(static≡runtime,NEG-25 型);或 provenance 增量 coverage 在拆分报告后恒为 0(NEG-18 型);或 query-relative 维度下从未出现"同 mutation 不同 verdict"——三者任一成立即证伪。
- **C4**:若合成正对照失败(理论上可修复的 case 也修不好);或 mutation 梯度实验显示影响从不局部化(repair 曲线恒等于全重算)——即证伪。

## 15. 正结果与零结果的发表路径

| | 正结果 | 零结果 |
|---|---|---|
| C3 | 主会系统/ML 系统方向(新执行语义+边界定理+真实 agent 实证) | "事前 validity 判定在 agent 复用中不必要：投机与无脑复用的边界分析"——测量/立场型论文或 workshop;与 NEG-01 形成跨项目证据链 |
| C6 | 系统会议(范式迁移+系统+形式化);理论节可拆短文 | "LLM agent workflow 的依赖结构实测：稀疏复用是伪需求"——数据集/测量论文，直接改写该方向的问题定义 |
| C4 | ML 主会(Repairable 档首次刻画+机制) | "Repairable 档为空：mutation 影响非局部化的证据"——与 CacheBlend 对照的边界论文 |

## 16. 下一轮 Paper-Search 查询

1. `speculative execution verification rollback LLM agents`
2. `optimistic concurrency control workflow retry compensation`
3. `data provenance memoization incremental recomputation pipeline`
4. `agent tool call artifact caching dependency tracking`
5. `context compression agent handoff multi-stage`
6. `selective recomputation KV cache context mutation`(跟踪 CacheBlend 的引用网络)
7. `cache-aware routing LLM serving locality`
8. `semantic deduplication multi-agent workflows`
9. `Noria partial materialization` / `differential dataflow`(引用追踪)
10. `effect systems runtime verification agents tool use`

## 17. 推荐的 Scoop-Check 轴

1. **C3 主轴**:"speculative/optimistic reuse of completed computation with outcome verification and rollback in LLM agent workflows"(查 2024–2026,重点 OpenReview——本轮 OpenReview 源失败，有盲区)。
2. **C6 主轴**:"provenance/lineage-based memoization of intermediate artifacts in LLM agent pipelines"(含 Durable Intermediate Artifacts、Execution Lineage 两篇旧近邻的重新核实)。
3. **C4 轴**:"selective recomputation / repair of cached model state after context mutation"(重点是 CacheBlend 之后 2025–2026 的跟进工作)。
4. **C5 轴**:"cross-model KV/hidden-state translation for LLM communication"(DroidSpeak、C2C 全文核实)。
5. **C12 轴**:"semantic deduplication of subtask execution in multi-agent systems"。

## 18. 最终建议与不确定性

**建议**:C3 与 C6 并行启动——C3 的 24h 资格实验(零模型，重分析冻结 trace)和 C6 的 24h 资格实验(零模型，依赖稀疏自检)都不需要任何新基础设施,48 小时内得到两个独立的停/走信号;C4 用一周合成 microbenchmark 做小额并行投入。三条线共享同一个 from-scratch 双跑 oracle 方法论(§5)。主线论文押 C6，因为它最完整地继承了旧项目的可挽救资产(D2 replay、三态分类、统计范式)且正面命中 dossier §8 列出的最大未测空白(真实多 consumer、query-relative validity);C3 是它的"执行语义"姊妹篇，两者最终可合流(C6 的 provenance 判定 + C3 的投机回退 = 完整的复用执行模型)。

**不确定性，如实列出**:

- 所有 novelty 判断是检索级的：两次 paper-search 中 Semantic Scholar/OpenAlex/OpenReview 三源全程失败(403/401/鉴权),**OpenReview 盲区对 C3/C5 尤其危险**(NeurIPS/ICLR/ICML 在审论文不可见);§17 的 scoop-check 未完成前,Top 3 排序可能变化。
- 2025–2026 文献未逐篇全文核实;[K13][K21][K45] 等标题级冲突可能改变 C7/C10/C8 的判定。
- C6 的首要威胁是 NEG-25 型失败(真实 workflow 依赖全稠密)——这正是把它放在 24h 资格门的原因;若失败,C6 降级、C3 升主线。
- C3 的"回退率低"推断部分来自 NEG-01 的旧数据(单一 receiver、自然工况),对困难场景(外部状态变更、异构 receiver)外推无证据。
- 旧 dossier 中 DOCUMENTED 级证据(尤其 M0–M3 era)未逐条独立复算;本报告的分类判断依赖其转录可信度。

**结论**:本报告没有得出"原方向不值得继续"的结论，但得出了它的重心必须移动——从"事前 validity 判定"(NEG-01 已证明其对象在自然工况下测量不到)移向三个测得到现象的地方：事后验证与回退(C3)、依赖驱动的 artifact 复用(C6)、修复能力的边界(C4)。receiver-conditioned validity 没有被放弃，而是从"判定谓词"降级为 C6 中的 query-relative 结构属性——它第一次有机会被真实测量，因为它第一次被放进了天然有多 consumer 的 testbed。

---

## 附:24h 资格门执行结果(2026-07-21 当日完成)

- **C3 资格门:GO**(详见 `c3_gate_24h_2026-07-21.md`)。理论回退率 ρ ≈ 5–6%(Task A/B 冻结 trace),距盈亏平衡(≈40–48%)近一个数量级;scope 限定在有内在 verifier 的任务。
- **C6 资格门:GO**(详见 `c6_gate_24h_2026-07-21.md`)。两个真实代码库的 import DAG 天然高度稀疏(median 爆炸半径 0,98–100% 模块影响 ≤10%);结构性前提 1 通过，前提 2(workflow 层保持稀疏)留作一周实验的内置资格门。
