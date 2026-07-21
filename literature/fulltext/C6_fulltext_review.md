# C6 全文级文献核实报告

方向：provenance-aware intermediate artifact reuse + query-relative incremental maintenance(C6)
核实日期：2026-07-21。方法：WebSearch + FetchURL(arXiv abs/HTML、DOI/出版社页面、OpenReview PDF、项目 GitHub 页)。本报告只收集证据并给出证据级 overlap 分类建议，不做 novelty 裁决。

三格记号(用于第 8 项):
- **[P]** = artifact 级 provenance 复用(依赖未变→复用)
- **[D]** = 增量/delta 维护(依赖变更→只重算受影响部分,delta 语义而非整节点重跑)
- **[Q]** = 多 consumer 的 query-relative validity(同一 artifact 对不同下游查询有效性不同)

---

## C6-P1 Noria (OSDI 2018)

1. **真实存在**:USENIX 会议页(含 BibTeX 块)与会议 PDF 均已抓取解析。https://www.usenix.org/conference/osdi18/presentation/gjengset
2. **发表状态**:正式发表,13th USENIX Symposium on Operating Systems Design and Implementation (OSDI 18),Carlsbad,2018-10,pp. 213–231,ISBN 978-1-939133-08-3。无 DOI(USENIX 开放获取)。
3. **精确条目**:Noria: dynamic, partially-stateful data-flow for high-performance web applications。Jon Gjengset, Malte Schwarzkopf, Jonathan Behrens(后:Lara Timbó Araújo, Martin Ek, Eddie Kohler, M. Frans Kaashoek, Robert Morris)。2018, OSDI。
4. **机制(全文已读,前 ~5 节直读)**:*partially-stateful data-flow*——应用给出关系 schema + 参数化查询,Noria 编译成联合 dataflow,预计算读结果、以正/负 delta update 增量传播写;operator 状态为部分物化,可驱逐,读缺失时发递归 **upquery** 从上游状态回填;跨相关查询 merge-and-reuse 共享子图与计算;支持在线改 query/schema 且不停机。一致性:最终一致,写入静止后 view 结果 ≡ 直接对 base table 执行查询(§3.4 原文)。
5. **关键实验位置**:§8.1 Lobsters 真实应用端到端 5× vs 手工优化 MySQL;§8.2 代表性查询 2–10× vs MySQL/memcached 与某商业 DB 物化视图;§8.3 集群扩展到数百万 writes/s、数千万 reads/s,对比 differential dataflow。**注意:PDF 抓取文本在 §4(Figure 5)处截断,§8 各 Figure 编号未逐一核实,小节号来自 §1 贡献声明交叉引用。**
6. **代码**:https://github.com/readysettech/readyset (BSL 1.1;其 `history.md` 明示代码库构建自 MIT PDOS 的 Noria 研究原型)。
7. **代码↔机制一致性**:ReadySet 自述为"MySQL/Postgres 线兼容缓存层,对 SELECT 结果做增量更新",与论文机制一致(生产化后代)。已读 README/history.md。
8. **覆盖格**:[P] 部分(视图/record 粒度,非 agent 任务产物);[D] 是(delta update 传播);[Q] 否——状态对所有读统一维护,有效性不随下游查询变化。
9. **明确未解决**:无"按下游查询判定同一物化状态是否可用"的判定(不需要——它对所有查询都维护);无"复用 ≡ from-scratch 重算"的 oracle 实验范式;纯关系数据流域,不涉及 LLM/agent/文本 artifact。
10. **overlap 建议:PARTIAL**。[D] 与共享物化覆盖充分,但 [Q] 完全缺位,领域为关系数据流。

## C6-P2 DBSP (VLDB 2023)

1. **真实存在**:arXiv abs 页与 VLDB 官方 PDF 均已解析。https://arxiv.org/abs/2203.16684 , https://www.vldb.org/pvldb/vol16/p1601-budiu.pdf
2. **发表状态**:正式发表,PVLDB 16(7): 1601–1614 (2023),VLDB 2023,DOI 10.14778/3587136.3587137。另获 VLDB 2023 Best Research Paper(feldera.com 博客佐证)。
3. **精确条目**:DBSP: Automatic Incremental View Maintenance for Rich Query Languages。Mihai Budiu, Tej Chajed, Frank McSherry(后:Leonid Ryzhyk, Val Tannen)。2023(arXiv 2022-03),PVLDB/VLDB。
4. **机制(全文前 ~2.5 节直读)**:把 IVM 重述为流计算:stream = 取值于 abelian group 的无限序列;4 个算子(lift、z⁻¹ delay、积分 I、微分 D);查询 Q 的增量版本定义为 **Q^Δ = D ∘ ↑Q ∘ I**;由 chain rule 得模块化增量化算法(Algorithm 4.6),可增量化任意 DBSP 程序(关系代数全集、嵌套关系、聚合、flatmap、单调/非单调递归、流式聚合);Z-set 建模关系数据;全部定理经 Lean 机检。
5. **关键实验位置**:**理论文,两次独立 PDF 抓取(vldb.org 与 docs.feldera.com/vldb23.pdf)均截断于 §2.3,未发现实验评估章节;§1 roadmap 提到"as we briefly discuss in §7"(实现)。tables/figures:电路图(Figures)在 §2–§4;性能实验数字:无(未见)。**
6. **代码**:论文 PVLDB artifact:https://github.com/vmware/database-stream-processor (现 vmware-archive);活跃后继 https://github.com/feldera/feldera 。
7. **代码↔机制一致性**:Feldera 文档明示其增量引擎即 DBSP(SQL→DBSP→Rust),README 引用该 VLDB 论文为理论基础。一致。
8. **覆盖格**:[D] 是(理论核心);[P] 概念上(视图即复用对象);[Q] 否——IVM 维护视图"当前值",有效性不相对具体查询。
9. **明确未解决**:不研究同一中间结果对不同下游查询的可用性;delta 模型依赖群结构(Z-set 的 +/−),agent 文本 artifact 无天然群运算;零 agent 场景。
10. **overlap 建议:PARTIAL**。delta 维护的理论上限,但 [Q] 缺位、模型假设(abelian group)与文本 artifact 不匹配。

## C6-P3 Differential Dataflow (CIDR 2013)

1. **真实存在**:CIDR 2013 官方 PDF 全文已解析(cidrdb.org, CIDR13_Paper111.pdf);Microsoft Research 出版页佐证。https://www.microsoft.com/en-us/research/publication/differential-dataflow/
2. **发表状态**:正式会议论文,6th Biennial Conference on Innovative Data Systems Research (CIDR '13),2013-01,Asilomar。CIDR 无 DOI。
3. **精确条目**:Differential dataflow。Frank McSherry, Derek G. Murray, Rebecca Isaacs, Michael Isard。2013, CIDR。
4. **机制(全文直读)**:differential computation——集合状态按**偏序版本**变化(而非全序);每次 update 的 difference 被索引化保留而非合并丢弃,可按不同 predecessor 组合重建任意版本状态,从而支持任意嵌套迭代的增量维护;在数据并行 dataflow(Naiad 原型)上实现。
5. **关键实验位置**:§2 Figure 1(24 小时 Twitter mention 图连通分量:逐 iteration 的 label 差异数;滑窗滑动 1 秒仅处理 67 个差异,约为全量 prioritized 工作的 0.003%);§5 性能(亚秒级 SCC 维护;§5 具体表号未截入抓取范围)。
6. **代码**:原始 Naiad 原型为 MSR 内部系统(硅谷实验室已关闭);Rust 重实现 https://github.com/TimelyDataflow/differential-dataflow (README 已核实:"An implementation of differential dataflow over timely dataflow on Rust")。
7. **代码↔机制一致性**:一致,原作者(McSherry)主导的同模型重实现。
8. **覆盖格**:[P] 是(跨版本复用 difference trace);[D] 是;[Q] 否——"有效性"沿版本/时间偏序组织,不是按下游查询的相对有效性。
9. **明确未解决**:consumer-relative 维度完全未出现;数据模型为 multiset,非文本 artifact;无 from-scratch 等价判据(有正确性但非"双跑对照"范式)。
10. **overlap 建议:PARTIAL**。[P]/[D] 强覆盖,[Q] 缺位。

## C6-P4 Build Systems à la Carte (ICFP 2018)

1. **真实存在**:ACM DL 页面(DOI 10.1145/3236774)与 MSR 官方 PDF(前 ~6 页)均已解析。
2. **发表状态**:正式发表,Proc. ACM Program. Lang. 2, ICFP, Article 79(2018-09),29 页,DOI 10.1145/3236774。扩展版:Build Systems à la Carte: Theory and Practice, JFP 2020。
3. **精确条目**:Build Systems à la Carte。Andrey Mokhov, Neil Mitchell, Simon Peyton Jones。2018, ICFP (PACMPL)。
4. **机制(直读部分:§1–§2.5、Table 1)**:把 build system 分解为两个正交设计选择——scheduler(topological / restarting / suspending)与 rebuilder(dirty bit / verifying traces / constructive traces / dynamic dependency traces);给出 Definition 2.1(Minimality:task 每次 build 至多执行一次,且仅当其传递依赖的输入发生变化);用 Make/Excel/Shake/Bazel 四系统实例化分类;模型以可执行 Haskell 给出。C6 关心的"from-scratch consistency"即本文正确性判据(build 结果必须与从零全量重算一致)——**注意:correctness 定义位于 §3 抽象模型,抓取文本未覆盖到 §3 的确切定义小节号;JFP 2020 扩展版含完整形式化。**
5. **关键实验位置**:理论/模型文,无 benchmark;Table 1(四 build system 的 scheduler×rebuilder×persistent info 分类矩阵)已直读核实。
6. **代码**:论文脚注声明所有模型可执行并发布于 Hackage(build-1.0);仓库 https://github.com/snowleopard/build (GitHub 页抓取返回导航壳,README 未直读;Hackage 链接在 PDF 正文已核实)。
7. **代码↔机制一致性**:Haskell 可执行模型即论文抽象本身,一致(基于论文声明)。
8. **覆盖格**:[P] 是(task 依赖图 + traces);[D] 是(rebuilder 语义=最小重算);from-scratch 一致性判据 = 是(C6 判据的直接来源);[Q] 否。
9. **明确未解决**:单一 target 视角,无"同一 artifact 对不同 consumer 查询有效性不同"的概念;非 LLM/agent 场景;无 delta(群)语义——重算单位是整 task。
10. **overlap 建议:PARTIAL**。正确性判据与最小重算语义重叠深,但 [Q] 与 delta 语义缺位。

## C6-P5 Answering Queries Using Views (PODS 1995)

1. **真实存在**:DBLP 记录(conf/pods/LevyMSS95)确认;另有 ≥4 个独立论文引文交叉确认(含页码)。ACM DL 页面抓取被 403 拦截。
2. **发表状态**:正式发表,14th ACM SIGACT-SIGMOD-SIGART Symposium on Principles of Database Systems (PODS '95),1995-05,pp. 95–104。DOI 候选 10.1145/212784.220272 **未直接验证**(ACM 403;OpenAlex 按此 DOI 查询返回 404,存疑)。
3. **精确条目**:Answering Queries Using Views。Alon Y. Levy, Alberto O. Mendelzon, Yehoshua Sagiv, Divesh Srivastava。1995, PODS。
4. **机制**:**full_text_obtained=false**(全文未获取;以下基于摘要与多份二手引文)。研究"给定一组物化视图,判定查询 Q 能否用这些视图回答/重写"的问题:提出 bucket algorithm;给出 datalog 查询用视图重写的 containment 判据与复杂度界(NP-complete 类结果);证明重写所需视图数不超过查询子目标数等定理。这是"同一组视图对不同查询可用性不同"(query-relative usability)的理论源头。
5. **关键实验位置**:纯理论,无实验;unknown(全文未取)。
6. **代码**:无(1995 年理论文)。
7. 不适用。
8. **覆盖格**:[Q] 是(理论源头);[P] 概念上(视图即复用对象);[D] 否。
9. **明确未解决**:不含任何维护/增量/运行时;静态数据库理论,与 agent 执行无关。
10. **overlap 建议:PARTIAL**。[Q] 一格的源头文献;[D] 与执行语义完全不覆盖。

## C6-P6 Execution Lineage(Rosen & Rosen,2026)—— 旧记录"Execution Lineage"的真实身份

1. **真实存在**:arXiv abs + HTML 全文(v1)均已解析。https://arxiv.org/abs/2605.06365 。ThruWire 研究页(thruwire.ai/research)列为 "Paper 01"。
2. **发表状态**:arXiv-only 预印本(2026-05-07 提交),未检索到正式 venue。
3. **精确条目**:From Agent Loops to Deterministic Graphs: Execution Lineage for Reproducible AI-Native Work。Josh Rosen, Seth Rosen。2026, arXiv。
4. **机制(全文直读)**:AI-native 工作 = DAG,节点 v = (ℐ_v, f_v, 𝒪_v);**execution identity k_v = h(σ_v, x_v, {k_u : u∈pred(v)})**(结构、解析后输入、上游 identity 的哈希);k_v 不变→identity-based replay 精确复用;k_v 变化→依赖它的下游节点失效并**整体重跑**(非 delta),无关分支不动;typed local boundary、canonical output、deterministic publication。原文明确对照对象:prompt lineage / transcript state。
5. **关键实验位置**:§8 Table 1(unrelated-branch 任务,n=3,GPT-5.2:DAG replay 3/3 精确保全、0 churn、0 污染;loop 基线 3/3 重写,污染 2/3 与 3/3;输入 token 382 vs ~11.7k,≈30.5×);§8 Table 2(intermediate-artifact edit:三方 final constraint reflection 均 1.00;仅 DAG replay 上游保全/下游传播/cross-artifact consistency 全 1.00,loop 仅 0.50);Table 3(information boundaries);Figure 1。
6. **代码**:论文引用 "repo commit f6cc8679ab1178b22fa01c263aa14e77454081ee",但全文与 ThruWire 页均未给出公开仓库 URL。**code_url = null。**
7. **代码↔机制一致性**:无法判断(无公开仓库)。
8. **覆盖格**:[P] 是(agent 域、identity-based);[D] 否(失效后整节点重跑,无 delta);[Q] 否(validity = execution identity 相等,单一判定,与下游查询无关);from-scratch 等价 oracle 否(对照是 loop 基线,非"复用 ≡ 全量重算"双跑)。
9. **明确未解决**:query-relative/多 consumer 维度完全未出现;无 delta 维护;无 from-scratch 等价验证;任务为人工构造 memo 场景且 n=3。
10. **overlap 建议:PARTIAL**。**它恰好就是 C6 命题中"identity-based lineage replay"基线本身**(C6 最近邻);C6 的三个增量维度(delta、query-relative、多 consumer)它一个都不做。

## C6-P7 Durable Intermediate Artifacts(Rosen & Rosen,2026)—— 旧记录"Durable Intermediate Artifacts"的真实身份

1. **真实存在**:arXiv abs + HTML 全文(v1)均已解析。https://arxiv.org/abs/2605.12087 。ThruWire 研究页列为 "Paper 02"。
2. **发表状态**:arXiv-only 预印本(2026-05-12 提交)。
3. **精确条目**:Intermediate Artifacts as First-Class Citizens: A Data Model for Durable Intermediate Artifacts in Agentic Systems。Josh Rosen, Seth Rosen。2026, arXiv。
4. **机制(全文直读)**:系统级数据模型:一等 artifact 七性质(typed / structured / addressable / versioned / dependency-aware / authoritative / consumable downstream);artifact record = (identity, family, role, scope, status, dependencies, lineage, payload);**additive vs superseding 更新语义**与 active(role, scope) 当前态解析;artifact lineage 四关系(produced-by / consumed-by / supersedes / superseded-by);supersession manager 发失效事件;执行/重放显式委托给 P6 的执行基底。提出评估准则:AuthorityAcc、stale-artifact detection F1、revision-localization precision/recall。
5. **关键实验位置**:**无实验**(数据模型/立场文);Table 1(相邻 state surface 概念对比)、Table 2(artifact 生命周期示例)、Table 3(评估准则)均为概念表,已直读。
6. **代码**:无。
7. 不适用。
8. **覆盖格**:[P] 是(artifact 语义最完整:dependency-aware + lineage);[D] 否(委托执行基底);[Q] 边缘——active(role, scope) 的 scope 是"授权/场景边界",接近但**不是**按下游查询的可用性判定。
9. **明确未解决**:无 delta;scope ≠ query-relative validity;无正确性 oracle;无实验。
10. **overlap 建议:PARTIAL**。artifact 数据模型与 C6 建模层重叠最深,机制三格几乎全缺。

## C6-P8 ToolCacheAgent(ICLR 2026 在审)—— 引用链发现的撞车候选(替换进清单)

1. **真实存在**:OpenReview PDF 已解析(forum id=tX3YcbNa5w;直链 PDF 05f7fe080121ee4044c4899cf9b69ac21b7738ba.pdf)。
2. **发表状态**:ICLR 2026 投稿,双盲在审(匿名),抓取时未录用。
3. **精确条目**:TOOL CACHE AGENT: Accelerating LLM Agent through Intelligent Tool Call Caching。匿名。2026,OpenReview。
4. **机制(全文直读)**:"agent-for-agents"缓存层:LLM Cache Planner 按工具元数据把工具分类 READ/WRITE、cacheability(STATIC/TRANSIENT/NONE)、TTL、primary arguments;**cache key = 工具名 + 参数 hash(identity-based)**;**dependency-aware invalidation**:WRITE 工具的实参映射到 READ 工具 primary arguments,前缀失效;EWMA 平滑 hit/eviction/mem 指标触发自适应 replanning;Redis 后端。
5. **关键实验位置**:§5.1 Table 1(HotpotQA/Movie Recommendation/ParallelQA × ReAct/LLMCompiler × Llama-3.3-70B/Qwen-2.5-72B:最高 **1.69×** 加速且准确率不降);Table 2(hit rate/eviction);§5.2 workload-shift replanning;§5.3 Table 3(τ-bench Retail 依赖失效正确性);**Limitations 自述:6 个错误结果源于 hidden dependencies——WRITE 工具修改了未出现在参数表中的状态,argument-based invalidation 无法捕捉隐式/间接依赖。**
6. **代码**:未发现(匿名投稿)。code_url = null。
7. 无法判断。
8. **覆盖格**:[P] 是(工具结果缓存+失效,agent 域最近邻之一);[D] 否;[Q] 否;from-scratch oracle 否(正确性靠 τ-bench 任务结果对比)。
9. **明确未解决**:隐式依赖(自述);DAG 传递失效(只有 planner 推断的成对规则);多 consumer;query-relative;语义等价判据。
10. **overlap 建议:PARTIAL**。缓存+依赖失效与 C6 同域,但三个增量维度全缺;其 limitation 一节恰好是"参数级/identity 级 provenance 不足"的直接证据。

## C6-P9 Agent Workflow Memory (ICML 2025)

1. **真实存在**:arXiv abs 2409.07429 + OpenReview 页面(NTAhi2JEEE)已解析。
2. **发表状态**:正式发表,ICML 2025(PMLR 267,Vancouver)。
3. **精确条目**:Agent Workflow Memory。Zora Zhiruo Wang, Jiayuan Mao, Daniel Fried, Graham Neubig。2025(arXiv 2024-09),ICML。
4. **机制**:**full_text_obtained=false**(abs + OpenReview 元数据)。从经验中归纳可复用的 workflow(文本化例程/子目标),写入 memory,后续任务选择性注入 prompt 指导行为;offline(训练集归纳)与 online(测试时归纳)两模式。复用对象是**程序性记忆文本**,不是带输入依赖的计算产物。
5. **关键实验位置**:Mind2Web +24.6%、WebArena +51.1% 相对成功率(abstract);具体表号 unknown。
6. **代码**:https://github.com/zorazrw/agent-workflow-memory (OpenReview "Link To Code" 与 GitHub 页均已核实)。
7. **代码↔机制一致性**:官方仓库,README 与论文方法描述一致。
8. **覆盖格**:三格均否(无 provenance 依赖边、无失效/增量、无 query-relative validity;复用靠文本检索/注入)。
9. **明确未解决**:artifact 正确性、失效、增量计算。
10. **overlap 建议:ADJACENT**。同为"agent 工作流复用"叙事,但复用对象与机制完全不同。

## C6-P10 Prompt Cache (MLSys 2024)

1. **真实存在**:arXiv abs 2311.04934 + MLSys 2024 proceedings 条目(papers.cool、MLSys PDF 引文)已核实。
2. **发表状态**:正式发表,MLSys 2024,pp. 325–338。
3. **精确条目**:Prompt Cache: Modular Attention Reuse for Low-Latency Inference。In Gim, Guojun Chen, Seung-seob Lee(后:Nikhil Sarda, Anurag Khandelwal, Lin Zhong)。2024, MLSys。
4. **机制**:**full_text_obtained=false**(abstract + 多份引文)。把高频重叠文本段(system message、prompt 模板、文档)注册为 **prompt module**,在推理服务器上预计算并存储其 attention state(KV),跨 prompt 复用;schema 保证复用时位置正确性。复用粒度 = KV 注意力状态,匹配方式 = 模块 identity/模板。
5. **关键实验位置**:TTFT 加速 8×(GPU)至 60×(CPU),精度不降(abstract);具体表号 unknown。
6. **代码**:https://github.com/MachineLearningSystem/24MLSYS-prompt-cache (声明含实现与评估;疑似社区归档镜像,作者官方性未核实)。
7. **代码↔机制一致性**:仓库名与论文对应,内容未深入核实。
8. **覆盖格**:三格均否(无 artifact 语义、无依赖失效——模块是静态模板、无 query-relative)。
9. **明确未解决**:内容变化后的失效;agent/任务层语义;多 consumer 有效性。
10. **overlap 建议:ADJACENT**。是"复用中间计算"的最邻近系统工作,但粒度在 KV 层,identity/template 匹配。

---

## 对 C6 核心问题的总结证据(只陈述证据)

核心问题:"query-relative、multi-consumer validity 与 delta maintenance,是否形成超越 identity-based lineage replay 的明确增量?"

证据(按主题归并,不作裁决):

1. **identity-based lineage replay 在 agent 域已存在但极新、未正式发表**:Rosen & Rosen 2026(C6-P6,arXiv-only)给出 DAG + execution-identity 哈希 replay + 选择性失效 + n=3 对照实验;同一团队的 C6-P7 给出 artifact 数据模型(typed/dependency-aware/supersession)。两篇均:无 delta(失效→整节点重跑)、无 query-relative validity、无 from-scratch 双跑 oracle。
2. **工具级缓存+依赖失效在 agent 域已有在审工作**:ToolCacheAgent(C6-P8,ICLR'26 投稿)identity key + LLM 推断的成对失效规则;其自述 6 个错误来自 hidden dependencies——参数级 provenance 表达力不足的直接证据。
3. **delta 维护理论/系统成熟但全在 DB 域**:DBSP(群结构 delta,Lean 机检)、Differential Dataflow(偏序版本 difference 复用)、Noria(delta 传播 + 部分物化 upquery)。三者均无 query-relative 维度,数据模型均为关系/multiset。
4. **from-scratch 一致性判据成熟但在 build 域**:Build Systems à la Carte(minimality + correct rebuilders);C6-P6/P8 均未采用该判据做实验。
5. **query-relative validity 的理论源头在 PODS'95(Levy et al.)**,本次检索**未发现任何工作把 answering-queries-using-views 式可用性判定移植到 agent 中间产物**。
6. **多 consumer 共享计算**在 Noria(merge-and-reuse)与 ReadySet 中以"所有读统一维护"的方式存在,与"同一 artifact 对不同下游查询有效性不同"不是同一性质。
7. **2024–2026 扫描到的其余候选(未全文核实,记录在案)**:MemOS(arXiv 2507.03724,memory OS,启发式 cache invalidation);LLMCache(arXiv 2512.16843,层间激活的语义相似复用);Continuum(arXiv 2511.02230,KV cache TTL 调度);LLM Agents for Interactive Workflow Provenance(arXiv 2509.13978,用 agent 查询 provenance 记录,方向相反);ICM workspace(arXiv 2603.16021,文件系统上下文层级);博客 "The Process Is the Memory"(yonk.dev,event sourcing + memoization + 依赖失效,非论文);科学工作流 provenance 缓存(VisTrails / Kepler smart rerun,~2008–2015);ML pipeline 中间结果/lineage(Helix VLDB'18、ModelDB、Mistique,2016–2018,本次未展开核实)。**未发现比 C6-P6 / C6-P8 更直接的撞车工作。**
8. 检索纪律说明:arXiv 1803.02413 经核实**不是** Noria(是一篇数学论文,convolution operators);Noria 无 arXiv 版本,以 USENIX 页面为准。Levy 1995 的 DOI 候选值未能直接验证(ACM 403、OpenAlex 404),DBLP 记录(PODS 1995: 95–104)已确认。
