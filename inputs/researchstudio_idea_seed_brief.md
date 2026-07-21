This document records one previous formalization of the original idea.
Its “must preserve”, “design requirements”, and “no-go constraints”
are not binding on the new exploration.

# ResearchStudio-Idea Seed Brief

> 输入给 https://github.com/microsoft/ResearchStudio/tree/main/ResearchStudio-Idea 的种子文档。
> 本文档不推荐最终实验路线,只定义问题、证据和约束。完整历史见
> [route_a_plus_negative_evidence_dossier.md](route_a_plus_negative_evidence_dossier.md)。

## 1. Original Scientific Spark

多智能体通信不仅传递信息,也可能传递已经完成的计算状态(computation state)。同一份计算
状态对不同的接收方(receiver)agent,其有效性(validity)可能是不同的——某个 receiver
可以安全复用它,另一个 receiver 可能必须部分修复甚至完全重算。这个"有效性相对于消费者
而定义"的想法,是整个研究线的起点。

## 2. Core Research Question

> After a producer computation changes, can a preregistered receiver-specific contract
> preserve downstream computation even when the full artifact or invocation is no longer
> byte-identical?

三个必须保留的要素:
- **超越 byte identity**:问题的意义在于"字节不同时"是否还能安全复用,不是"字节相同时
  能省多少"(后者是普通 exact cache,不是这个问题)。
- **Receiver-specific**:有效性判定必须相对特定消费者的接口/契约定义,不是全局字节相等
  或全局语义相似。
- **三档复用状态**:Exact(字节相同)/ Repairable(可修复后安全)/ Invalid(必须重算)——
  不是二元的"能不能复用"。
- **Computation state,不只是文本 artifact**:原始构想包含 latent/KV 状态直接传递的
  可能性,不应被窄化为纯文本层面的 agent 消息缓存。

## 3. Existing Negative Evidence(8-12 条最重要约束)

1. 六次独立自然工况复用测量(KV cache + repair),在固定单一 receiver 视角下,额外任务
   翻转率与噪声地板不可区分——不支持"需要风险控制"的直接证据,但也没有证明复用安全,
   因为从未测过 receiver-conditioned validity 本身。
2. 三代 testbed(AutoCodeRover / mini-swe-agent / SWE-agent)都只有单一固定 receiver,
   没有一次真正比较过"同一 producer 产物、两个真实 consumer、不同 verdict"。
3. 自由文本是三代 testbed 里 LLM 实际消费的唯一形式——内部 typed 对象(SearchResult 等)
   从来不是 consumer-visible interface,这从工程根子上排除了直接实现 typed contract
   的路径。
4. 测出的"正 headroom"信号(v7 Oracle 1.86pp)被独立复核证明 100% 来自与内容无关的
   文件系统 mtime 伪影,不是真实等价性信号。
5. 完整 invocation 级比较是唯一可信的比较单位——命令前缀对齐、diff 相似度阈值等代理
   比较方式全部被证明会漏判或误判等价性。
6. 唯一被真正测量过的 typed-contract 候选(K2,行多重集合规范化),在可测数据上贡献
   恒为零,但它只是一个浅层结构规范化,远不是"typed/executable contract"的严肃实现。
7. 即使在 greedy/temperature=0 设置下,真实 serving 栈(批处理浮点非结合性)与真实文件
   系统操作(未排序目录遍历、checkout 路径 mtime)仍然引入测量敏感的非确定性——
   "上游相同则下游确定性相同"这一假设不能默认成立。
8. Outcome-level(真实 patch/test 判定)验证在全部实验中都缺失——所有"安全"结论目前
   最多只到 trajectory/exit_status 层面。
9. 早期 TraceBuild 尝试测"运行时依赖集合是否比静态依赖集合更稀疏",在具体 workflow
   (全上下文 prompt 设计)下测出 static=runtime(0/120 clusters 有差异)——testbed 的
   prompt/上下文路由设计必须先自检是否具备暴露目标现象的结构性前提。
10. 用于支撑 novelty 差异化的实测数字,如果脱离产出实验的判定结论单独引用,存在把
    "不具区分力 workflow 上的理论上界"误当作"真实可达收益"的风险。

## 4. What Is Falsified(窄结论)

- 若干具体测量装置/具体 testbed 组合已被证明不可信或不可行(AutoCodeRover 四层
  harness、v7 的 difflib Oracle、`task_b.py` 全上下文 prompt 设计下的 static=runtime)。
- 一个具体 contract 候选(K2,行多重集合规范化)在具体数据集上贡献为零。
- 在固定单一 receiver、自然工况扰动强度下,KV 复用引入的额外错误率与噪声不可区分。

**没有一条构成对原始核心问题(receiver-conditioned typed contract 复用)的证伪。**

## 5. What Is Not Falsified(原始 idea 仍未被真实实验触及的部分)

- Real multi-consumer receiver-conditioned validity(核心中的核心,三代 testbed 都
  没有真正测过)。
- Bytes-different / contract-equal / outcome-same 的非人为构造案例。
- Repairable(部分修复后可用)这一中间复用档位的独立定义与测量。
- Latent/KV computation state 的直接传递(现有工作已完全转向文本/tool-call 层面)。
- Heterogeneous receiver(不同能力/不同类型消费者)。
- 真实 live 执行中的下游计算跳过(而非事后判定)。
- Fresh-task outcome-level 验证。

## 6. Design Requirements Inherited from Failures

- Stable logical node identity(而非依赖 mtime/路径等易变元数据)。
- Explicit, machine-checkable dependencies(而非"几乎所有节点读全部上下文"式的隐式
  全依赖设计)。
- Typed producer artifact,且该类型必须是 consumer 真实消费的接口,不是内部旁路对象。
- Real consumer-specific projections(每个 receiver 有自己独立的投影/视图)。
- Consumer 无法绕过 typed projection 直接访问 raw artifact(否则 typed contract
  形同虚设)。
- Controlled, mechanism-targeted mutation(而非只能测出"是否触发"而不能测"为什么"
  的黑箱扰动)。
- From-scratch oracle(不能用同一份未校准的文本相似度 heuristic 兼任 Oracle 和
  contract 判据)。
- Fresh confirmatory data(discovery 集合上调出的阈值/发现不能直接当作确证结论)。
- Task/repository-clustered statistics(不能把同一 task 的多个 edge/mutation 当独立
  样本)。
- Outcome validation(真实 patch/test 判定是"安全复用"主张的必要条件)。
- Minimal harness(审计层数不得超过被审计科学问题本身的复杂度)。
- No post-hoc free-text heuristic 充当正式 contract 或 oracle。
- No LLM judge 充当 runtime contract(如果引入 LLM-as-judge,必须明确它是探索性
  信号,不是等价性证明)。

## 7. Questions for ResearchStudio-Idea

1. 哪些 MAS(multi-agent system)工作真实地把 agent 间通信视为 computation-state
   transfer,而不仅仅是消息/文本传递?
2. 是否存在天然暴露"同一 producer 输出被多个真实、独立 consumer 以不同方式消费"这一
   结构的现成 workflow(不需要人为构造 receiver)?
3. 哪些跨领域实验设置可以直接迁移到这个问题:projection query(数据库)、materialized
   view(数据库增量维护)、red-green testing(编译系统)、stable names(增量构建)、
   typed effects(类型系统)、partial evaluation(程序分析)、incremental view
   maintenance(数据库)?
4. 如何构造非人为的 bytes-different / contract-equal 案例(即不是研究者手工设计的
   mutation,而是真实工作流里自然出现的场景)?
5. Repairable 复用应该如何定义和验证——它与 Exact/Invalid 之间的边界应该用什么指标
   划定?
6. 如何把 latent/KV 层面的 validity 判定与离散(文本/结构化)artifact 层面的 validity
   判定统一在同一个理论框架下?
7. 哪些已有工作已经覆盖了 exact cache、tool cache 和 semantic cache 这几类问题,
   新工作与它们的差异化论证应该建立在哪个具体机制/洞见上(注意:不要只依赖单一实测
   数字,见 §3 第10条教训)?
8. 一周、一个月、完整论文三个预算层级下,分别能验证到原始问题的哪一层(是否可能设计
   出"结构资格审查零模型调用"式的低成本第一步,类似本项目 v8 D2 的做法)?
9. 什么样的实验结果会真正构成对原始 idea 的证伪(而不是对某个具体 testbed/具体 contract
   候选的证伪)?
10. 哪些看起来相关的实验设计,实际上只能验证 exact-cache baseline,而无法触及
    receiver-conditioned validity 这一核心?(需要在设计阶段就明确排除这类实验被
    误当作核心验证。)

## 8. Explicit No-Go Constraints

- 不再用 mini-swe-agent 证明 fan-out(已确认是单一顺序 pipeline)。
- 不再用自由文本 difflib/K2 类浅层 heuristic 充当正式 contract。
- 不再以 exact caching(B3.5/B3.5-I)结果替代或冒充 B4(typed contract)结论。
- 不再建立通用 Bash/文件系统 read-set tracer 作为项目主线基础设施(如确需追踪,先评估
  是否有现成工具,不要重新发明)。
- 不再建立多层 transport/supervisor/outer/inner 式 harness 架构。
- 不再"先写系统再寻找 testbed"——testbed 的结构性前提(是否有真实多 consumer、
  prompt 设计是否暴露稀疏依赖)必须先自检,再决定是否投入工程。
- 不使用被旧数据启发、又拿旧数据验证的新 contract 候选(K3/K4 式 post-hoc selection
  bias 的教训)。
- 不把 correlated microcases(同一 task/repository 的多个 mutation)当独立风险样本。

## 9. Assets Available for Reuse

仅列可复用资产,不默认必然被采用,详见 dossier §9:
- D2 trace-conditioned replay + identifiability gate 方法论(结构阶段零模型调用,
  先验证测量装置本身可信)。
- D3 read-set/mutation MEASURED/INFEASIBLE/INVALID_SAMPLE 三态严谨分类框架。
- 六次早期 null 的 cluster-bootstrap + 配对差值 + held-out 确证性统计设计范式。
- `docs/scoop_check_2026-07-13/` 的七步查新方法论框架(但需重新生成引用数字)。
- `EXPERIMENT_AUDIT.json` schema 与 `protocol_deviations` 强制声明纪律。
- focused test 套件(v7/v8,覆盖大量已知伪影的回归防护)。

## 10. ResearchStudio Expected Outputs

要求后续 ResearchStudio 项目产出:

- Primary-source literature map(直接读一手论文,不复用本项目未重新核验的旧 novelty
  数字)。
- Cross-domain transfer matrix(§7 第3条列出的跨领域概念与本问题的映射关系)。
- Candidate natural testbeds(必须先满足"真实多 consumer"结构前提的筛选)。
- Falsifiable hypotheses(明确写出什么结果会构成证伪)。
- Minimal experiment designs(不代替本文档做出选择,但应给出可比较的候选设计)。
- Novelty conflict analysis(独立重新核验,不沿用 §3/dossier 中标记为"需重新生成"的
  旧数字)。
- Explicit stop rules(预先写好的止损条件,吸取本项目"审计不得比科学复杂"的教训)。
- Positive and null-result publication paths(两种结果都要有对应的发表路径规划,
  不预设必须是正结果)。
