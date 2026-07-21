# C3 全文级文献核实报告

- 研究方向（C3 一句话定义）：在 agent/多阶段 workflow 中，**默认投机复用已完成的中间计算**（而不是事前判定其有效性），并行运行低成本 verifier（outcome 级），失败时回退到 checkpoint 重算。
- 核心问题：「复用历史中间计算并事后验证」与「预测未来 agent action 并提前执行（speculative execution）」之间是否存在足以形成独立贡献的机制差异。
- 核实时间：2026-07-21。核实方式：arXiv abs/API 页、arXiv HTML、ar5iv、DBLP、期刊页、作者主页、GitHub README。未 clone 任何仓库，未下载 PDF。
- 性质说明：本报告只收集证据、给出证据级 overlap 分类建议（DIRECT/PARTIAL/ADJACENT/NONE/UNCERTAIN），不作 novelty 裁决。
- 清单调整说明：原清单第 6 项（主动检索撞车候选）落实为 C3-P6～C3-P10 五篇，均来自引用链与定向检索（检索词覆盖 speculative execution/rollback/checkpoint/stale reuse/optimistic execution 等组合）。原清单 1–5 全部保留并逐篇核实。

---

## C3-P1 ToolSandbox（Apple）

1. **存在性**：真实存在。arXiv:2408.04682 可解析（v1 2024-08-08, v2 2025-04-16）；DBLP 有 CoRR 与 NAACL 两条记录。
2. **发表状态**：正式发表 — Findings of NAACL 2025, pp. 1160–1183（DBLP 确认；aclant​hology.org 页面抓取时网络失败，确切 anthology ID 未二次确认）。
3. **标题/作者/年份/venue**：*ToolSandbox: A Stateful, Conversational, Interactive Evaluation Benchmark for LLM Tool Use Capabilities*；Jiarui Lu, Thomas Holleis, Yizhe Zhang, …, Ruoming Pang（Apple）；2024（CoRR）/2025（NAACL Findings）。注意：任务清单所给标题（"…Benchmark for LLM Tool Use"）与实际标题（"…Evaluation Benchmark for LLM Tool Use Capabilities"）略有出入；arXiv v1 作者列为 Felix Bai，NAACL 版为 Haoping Bai（疑似同一人改名，未证实）。
4. **真正提出的机制**（full_text_obtained=true，ar5iv 全文）：Python 原生测试环境。Execution Context 持有 World State（settings/contact/messaging/reminder 数据库快照）+ Message Bus；工具是有状态 Python 函数，可修改世界状态、在未满足前置条件时抛异常（如蜂窝关闭时 send_message 抛 ConnectionError）；工具间存在**隐式状态依赖**（可嵌套：发消息→需开蜂窝→需关低电量模式）；GPT-4o 用户模拟器（Knowledge Boundary + Demonstration 降低幻觉，Table 2）；评估用 **Milestone/Minefield DAG**：每个 milestone 带多种 snapshot 相似度度量，在保持拓扑序下对任意轨迹做最优匹配，minefield 命中则整条轨迹记 0 分（Eq. 1）。
5. **关键数字位置**：Table 1（与 BFCL/ToolEval/API-Bank 特性对比）；Table 2（用户模拟器 ablation，1032 条人工标注轨迹）；Table 3（benchmark 统计：1032 用例、34 工具、平均 13.9 turn）；Table 4（13 个模型 × 场景类别 × 工具增强的主结果矩阵：GPT-4o 均分 73.0，最佳开源 Hermes-2-Pro 31.4）；§4 分类讨论（State Dependency/Canonicalization/Insufficient Information）。
6. **公开代码**：https://github.com/apple/ToolSandbox （存在）。
7. **代码是否实现论文机制**：是。README 展示 scenario 定义（`Milestone`/`SnapshotConstraint`/`edge_list`）、工具注册装饰器、Execution Context 快照、评估匹配流程与论文 §2 完全对应。
8. **是否覆盖「状态变化后复用旧计算+事后验证+回退」**：不覆盖。它是**环境/评测侧**工作：提供世界状态建模、状态依赖与 outcome 级（milestone）评价语义——即 C3 问题成立所需的「状态变化」与「outcome 验证」的形式化背景，但本身不含任何复用/验证/回退机制。
9. **明确没解决什么**：不含中间计算复用、缓存失效、投机执行或回退；论文 Limitations 还指出 milestone 人工编写成本高、不含强制确认/授权、不含 daemon 类工具。
10. **overlap 建议：ADJACENT**。它是 C3 问题的「状态变化语义+评测床」供给方，非机制竞争者。

## C3-P2 Leviathan et al. — Speculative Decoding

1. **存在性**：真实存在。arXiv:2211.17192 可解析（v1 2022-11-30, v2 2023-05-18）。
2. **发表状态**：正式发表 — ICML 2023（arXiv comment 标注 Oral；PMLR 引用记录 pp. 19274–19286）。
3. **标题/作者/年份/venue**：*Fast Inference from Transformers via Speculative Decoding*；Yaniv Leviathan, Matan Kalman, Yossi Matias（Google）；2022/2023；ICML 2023。
4. **真正提出的机制**（full_text_obtained=部分：ar5iv Sec. 1–3.5 完整读取，Sec. 4 实验表未在抓取片段内）：将处理器投机执行推广到随机设定：小近似模型 Mq 自回归采样 γ 个草稿 token，大目标模型 Mp **并行**验证，用 speculative sampling（拒绝采样 + 修正分布 p′=norm(max(0,p−q))）保证输出分布与 Mp 完全一致（Alg. 1）；理论给出接受率 α=1−E(D_LK)（Thm 3.5）、墙钟改进因子 (1−α^{γ+1})/((1−α)(γc+1))（Thm 3.8）。任务覆盖 lm1b（97M GPT-like）、英德翻译+CNN/DM 摘要（T5-XXL 11B）、LaMDA 137B 对话；摘要与引言均报告 T5-XXL 对 T5X 实现 2X–3X 加速且输出逐 token 相同。
5. **关键数字位置**：经验数字在 Section 4（墙钟对比，2X–3X）；理论在 §3（Fig. 2 期望生成 token 数曲线）。具体表格编号未核实（抓取止于 §3.4）。
6. **公开代码**：无作者官方实现（Google 未随论文发布）；存在大量第三方复现（未逐一核实，不列入）。
7. **代码是否实现论文机制**：n/a（无官方 artifact）。
8. **是否覆盖 C3 问题**：不覆盖，但它是 C3 核心问题中「speculative execution」一极的**范式源头**：先猜、并行验证、拒绝则丢弃重算。其验证是分布级精确等价（token 分布），环境无外部状态、无副作用、无 checkpoint 概念。
9. **明确没解决什么**：不处理多步 agent workflow、外部世界状态变化、副作用可逆性、近似（lossy）验证；推理时接受率 α 是静态模型属性而非运行时估计量。
10. **overlap 建议：ADJACENT**。机制类比源头（verify-then-commit + reject-recompute），但层次（token 级、无状态、精确验证）与 C3 问题（中间计算、状态变化、outcome 级低成本验证）不同，主要作用是界定范式边界。

## C3-P3 A Plan Reuse Mechanism for LLM-Driven Agent（AgentReuse）

1. **存在性**：真实存在。arXiv:2512.21309 可解析（v1 2025-12-24, v2 2025-12-25）；arXiv comment 与正文脚注均注明：本文为 2024 年发表于《计算机研究与发展》(Journal of Computer Research and Development) 同名中文论文的英文版，DOI 10.7544/issn1000-1239.202440380（该期刊 DOI 页可解析，内容为该文参考文献列表页，与论文引用结构一致）。
2. **发表状态**：正式发表（中文期刊，2024）+ arXiv 英文版（2025）。
3. **标题/作者/年份/venue**：*A Plan Reuse Mechanism for LLM-Driven Agent*；Guopeng Li, Ruiqi Wu, Haisheng Tan（USTC）；2024/2025；J. Computer Research and Development。
4. **真正提出的机制**（full_text_obtained=true，arXiv HTML v2 Sec. 1–6.3）：动机为规划延迟（GPT-4+AutoGen 实测平均 31.8s）与真实数据集约 30% 请求相同/相似。AgentReuse（Alg. 1）：bert-base-chinese 做意图分类+槽位填充，抽取关键参数后将请求"去参数化"（"Book a ticket from to"），在意图类别内用 m3e-small 嵌入 + FAISS 余弦相似度（阈值 γ=0.75）检索可复用 plan；plan 经 prompt 工程结构化为（Step, 描述, 容器镜像, 输入, 依赖, 输出）DAG；命中则以新参数执行旧 plan。明确声明：因请求涉实时信息（航班等），**复用 plan 而非 response**。
5. **关键数字位置**：Table 1（相似度判定：F1 0.9718、Accuracy 0.9459，比 GPTCache 高 6.8/13.06 个百分点）；Fig. 4（γ∈[0.75,0.95] 扫描）；§6.3（有效复用率 93%）；摘要称延迟降低 93.12%，§6 正文又称「latency reduced by 60.61 percentage points」——两处数字口径不同（前者对无复用基线、后者疑对现有复用方法），属内部不一致点；额外开销：VRAM ~100MB、每请求内存 <1MB、延迟 <10ms。数据集 SMP2019（2,664 请求，23 意图类）。
6. **公开代码**：未发现（正文与摘要无仓库链接）。
7. **代码是否实现论文机制**：n/a。
8. **是否覆盖 C3 问题**：部分覆盖「复用历史产物」一侧，但范式相反——有效性在**复用之前**判定（意图匹配+相似度阈值，本质是事前分类器），误判代价直接转嫁用户；无事后验证、无 checkpoint、无回退机制；复用对象是 plan 模板而非中间计算结果。
9. **明确没解决什么**：复用错误的检测与恢复；状态变化（世界已变但 plan 仍命中）下的 staleness 问题；论文只优化「判得准」，不设「判错怎么办」。
10. **overlap 建议：PARTIAL**。占据「复用历史 agent 产物降延迟」的问题域，但机制是事前有效性判定——恰是 C3 定义中明确对比的另一半（"而不是事前判定其有效性"）。

## C3-P4 ChainCaps

1. **存在性**：真实存在。arXiv:2605.26542 可解析（v1 2026-05-26 → v4 2026-07-01）。
2. **发表状态**：arXiv comment 标注 "Published at the Second Workshop on Agents in the Wild: Safety, Security, and Beyond (AIWILD) at ICML 2026" —— workshop 论文。
3. **标题/作者/年份/venue**：*ChainCaps: Composition-Safe Tool-Using Agents via Monotonic Capability Attenuation*；Xiaochong Jiang, Shiqi Yang, Ziwei Li, …（共 6 人）；2026；AIWILD @ ICML 2026。
4. **真正提出的机制**（full_text_obtained=true，HTML v3 全文）：定义「permission laundering」失效模式（每个工具调用各自合法、组合后端到端越权）。每个值携带 sink 特定的权限预算（downward-closed privilege 集合）；组合规则 B(y)=Pass(t)∩∩B(x_i)（Eq. 2，只交不并→单调衰减）；sink 调用前检查 Req(t,a)∈∩B(x)（Eq. 3）；上下文预算 B_ctx 做保守污点；HMAC 一次性降权令牌；非放大定理（Thm 3.1）；标量 IFC 表达力不足的表示论论证（Prop 3.2: 2^m vs m-bit）。实现为 ~1,200 行 Python 的透明 MCP 代理。
5. **关键数字位置**：Table 1（82 任务 × 5 模型 × 3 次 live 评测：ASR 25.2–67.8%→0–4.8%，benign 96–100%）；Fig. 3（ASR 柱状图）；Table 2（对 Fides/PFI 抽象的回放对比，GPT-5.1 轨迹上 59.5% vs 16.1%/10.1%）；Table 3（ablation：去 meet 规则 −17pp；manifest 质量：专家 100% / 清单引导 90.9% / 朴素 27.3%）；0.13ms 中位延迟；红队 14/14。
6. **公开代码**：**未发现**。正文末尾有 "Code and artifact availability." 标题但内容为空（HTML v3 与 API 摘要均如此）。
7. **代码是否实现论文机制**：无法判断（无公开 artifact）。
8. **是否覆盖 C3 问题**：不覆盖。它是运行时安全不变量（权限单调衰减）工作，关注的是**派生值的授权**而非**陈旧值的有效性**；无复用、无事后验证、无回退。
9. **明确没解决什么**：隐蔽信道、隐式流、manifest 本身错误、代理不可见的 OS 级副作用（shell 管道残余失败 8%）；明确声明范围限于 explicit-flow composition safety。
10. **overlap 建议：ADJACENT**。与 C3 共享「多步工具链上运行时不变量」的系统层次，但不变量内容（authority vs. staleness/validity）与机制（预防式拦截 vs. 事后验证+回退）正交。

## C3-P5 Information Fidelity / Martingale MCP

1. **存在性**：真实存在。arXiv:2602.13320 可解析（v1 2026-02-10，2,544 KB）。
2. **发表状态**：arXiv comment 标注 "Full working version of an extended abstract accepted at AAMAS 2026" —— AAMAS 2026 扩展摘要录用（全文在 arXiv）。
3. **标题/作者/年份/venue**：*Information Fidelity in Tool-Using LLM Agents: A Martingale Analysis of the Model Context Protocol*；Flint Xiaofeng Fan, Cheston Tan, Roger Wattenhofer, Yew-Soon Ong；2026；AAMAS 2026 (extended abstract)。
4. **真正提出的机制**（full_text_obtained=true，HTML v1 主体全文）：混合语义失真度量 Δ_t = (1−λ)·加权事实集匹配 + λ·嵌入余弦距离（Eq. 1）；MCP 交互建模为适应随机过程，影响函数 ϕ(i,j)=β^{j−i} 指数衰减（Assumption 3，βB<1）；构造 Doob 鞅 Z_t=E[D(T)|F_t]，证有界增量 |Z_{t+1}−Z_t|≤1+α/(1−βB)（Lemma 1），用 Azuma 得高概率界 Pr[D(T)−E D(T)≥√(2T(1+γ*)ln(1/η))]≤η（Thm 1）；推论：偏差 O(√T) 次线性（Cor. 1）、有效信息视界 β=0.7 时约 9 步→周期性 re-grounding（Cor. 2）。
5. **关键数字位置**：§5 Baseline Validation（Fig. 3：Qwen2-7B D(10)=5.26±0.34 vs 包络 9.15；Llama-3-8B 4.92±0.46 vs 8.90；安全边际 >1.7×；经验 β̂∈[0.68,0.71]；语义加权降失真 80%）；注意实验用**确定性缓存工具**（knowledge retrieval + financial data），β 是查询生成时人为设定的参数。
6. **公开代码**：https://github.com/flint-xf-fan/MCP （论文声明；仓库存在，描述为 "experiments for MCP paper"）。
7. **代码是否实现论文机制**：存疑。仓库存在且描述匹配，但页面渲染仅返回 GitHub 导航框架，目录结构未能检查 → 降级置信度。
8. **是否覆盖 C3 问题**：不覆盖。它给出错误沿工具链累积的理论上界与「约每 9 步 re-grounding」的部署建议——re-grounding 概念上是周期性**刷新/重取**，与「复用陈旧计算」方向相反；无复用、无验证器运行时、无回退。
9. **明确没解决什么**：树状/分支交互（实验只跑 B=1 链）、随机工具、失真度量本身的校准（λ、事实抽取器质量）；只给偏差界不给修复机制。
10. **overlap 建议：ADJACENT**。为 C3 的「复用随步数失效」直觉提供可引用的误差累积理论，但本身不含 C3 机制的任何部件。

## C3-P6 Sherlock（撞车候选 1，最接近）

1. **存在性**：真实存在。arXiv:2511.00330 可解析（v1 2025-11-01）。
2. **发表状态**：**在审**。正文脚注 "Preliminary work. Under review by the Machine Learning and Systems (MLSys) Conference. Do not distribute."（作者含 Microsoft Azure Research 与 UT Austin 成员；单位未匿名化）。
3. **标题/作者/年份/venue**：*Sherlock: Reliable and Efficient Agentic Workflow Execution*；Yeonju Ro, Haoran Qiu, Íñigo Goiri, …, Esha Choukse；2025；MLSys 在审。
4. **真正提出的机制**（full_text_obtained=true，HTML v1 + ar5iv 全文）：三件套——(i) 故障注入式反事实脆弱性分析识别易错节点（§5：终端>初始>中间，fan-in 正相关；Alg. 1 拓扑放置策略）；(ii) GRPO 偏好学习选成本最优 verifier（§6）；(iii) **投机执行运行时（§7）**：节点 W1 完成后立即后台跑 verifier，同时**不等验证结果**并发执行子节点 W2/W3；验证通过则保留投机结果，失败则**回滚到最近已验证输出**并重算。§7.1 给出投机深度上界（Eq. 4/8：下游累计执行延迟 < 当前节点验证延迟）、预算约束（Eq. 5）、期望投机成本 (1−m_i)·Σ(C_exec+C_vrf)（Eq. 6，m_i 为 verifier 与原输出一致率）。**§7.2 选择性回滚**：验证修订后计算修订输出与原输出的轻量相似度（ROUGE-L，instruction/tool 任务 ρ≈0.55、AUC≈0.85），高于阈值则**保留投机结果**，code/math 任务保守全回滚。动机数据（§3.3）：多数验证不修改原输出（match rate 0.6–0.8）。
5. **关键数字位置**：Table 3 + Fig. 15（延迟：LiveCodeBench 平均 T_exec −62.9%、T_vrf −48.7%；CoTCollection/OMEGA T_exec 降幅 >50%）；Fig. 12（放置策略）；Fig. 13（Pareto 前沿）；Fig. 14（端到端 vs AFlow：准确更高、验证成本 −26.0%）；摘要：平均准确率 +18.3%。
6. **公开代码**：未发现（正文无仓库链接）。
7. **代码是否实现论文机制**：n/a。
8. **是否覆盖 C3 问题**：**机制层面高度重合**——乐观使用未验证中间结果 + 后台 outcome 级验证 + 相似度门控的选择性回滚 + 重算，这正是 C3 的运行时骨架。差异（即 C3 的剩余空间）：Sherlock 投机的对象是**新鲜下游计算**（用当前未验证输出继续往下算），不是**状态变化后复用历史/陈旧中间计算**；其"失效"来自 LLM 输出错误而非外部世界状态漂移；回退粒度为 workflow 节点，副作用/外部状态可逆性未见明确处理。
9. **明确没解决什么**：历史计算的跨请求/跨时间复用；外部状态变化引发的失效模型；验证器本身错误（§7.2 对 code/math 的相似度度量失效、AUC≈0.5，只能全回滚）；论文未讨论副作用安全（irreversible side effects）。
10. **overlap 建议：DIRECT**。「事后验证 + 相似度门控回滚 + 重算」的运行时机制与 C3 三要素逐件对应；唯一实质差异是投机对象（新鲜下游计算 vs. 历史中间计算复用）与失效源（LLM 错误 vs. 状态漂移）。该差异是否足以支撑独立贡献，留主席裁决——但机制邻近性必须按 DIRECT 上报。

## C3-P7 Speculative Actions（撞车候选 2）

1. **存在性**：真实存在。arXiv:2510.04371 可解析（v1 2025-10-05, v2 2026-04-23）；OpenReview PDF 可抓取（Columbia 署名版）。
2. **发表状态**：**ICLR 2026 Oral**（依据：作者 Tianyi Peng 与 Naimeng Ye 主页均标注；OpenReview 存在对应 PDF。未经 ICLR 官方论文集页面二次确认）。
3. **标题/作者/年份/venue**：*Speculative Actions: A Lossless Framework for Faster Agentic Systems*；Naimeng Ye, Arnav Ahuja, Georgios Liargkovas, Yunan Lu, Kostis Kaffes, Tianyi Peng（Columbia）；2025/2026；ICLR 2026 Oral。
4. **真正提出的机制**（full_text_obtained=部分：abs v2 + HTML v2 §1 + GitHub README；正文未逐节读）：Actor/Speculator 双角色——权威但慢的 Actor（SOTA LLM、外部 API、环境、人）产出 ground truth；便宜 Speculator（小 LLM/减 prompt 的同 LLM/启发式）预测下一步 action+参数+预期观测，提前并行发起后续 API 调用；**Actor 结果到达后逐一核对，匹配才 commit，不匹配则回滚/覆盖**（README："Lossless core: verify before commit; rollback/overwrite when needed"）。环境：chess、τ-bench retail 电商、HotpotQA 检索（均 lossless）+ OS 调参（lossy 扩展，last-write-wins）。理论：理想假设下渐近延迟降幅上界 p/(1+p)；成本-延迟权衡与多分支选择性启动。
5. **关键数字位置**：摘要：跨域最高 55% 下一步预测准确率 → 最高 20% 延迟降低；成本-延迟分析章节号未核实（正文未逐节抓取）。
6. **公开代码**：https://github.com/naimengye/speculative-action （存在）。
7. **代码是否实现论文机制**：是。仓库按环境分目录（chess-game/、ecommerce/、hotpotqa/、os-tuning/），README 明确 Actor 验证前提交、失配回滚/覆盖的 lossless 核心，与论文机制一致。
8. **是否覆盖 C3 问题**：不覆盖——它是 C3 核心问题中「**预测未来 action 并提前执行**」一极在 agent 层的代表作：验证方式是**等待权威 Actor 产出真值后逐字匹配**（事前不存在"已完成旧计算"），无效测对象是预测而非陈旧；无 checkpoint/状态回滚语义（失配丢弃投机分支即可，因为投机在并行分支）。
9. **明确没解决什么**：历史计算复用；外部状态变化后的有效性判定；lossy 场景只做了 OS 调参个案（last-write-wins，无通用正确性保证）；预测准确率上限（55%）决定了收益上限。
10. **overlap 建议：PARTIAL**。与 C3 共享「推测+验证+丢弃」的骨架，但方向相反（前向预测 vs. 后向复用），且验证依赖权威真值逐一到达——这正是 C3 核心问题所要区分的机制差。

## C3-P8 Dynamic Speculative Agent Planning（DSP，撞车候选 3）

1. **存在性**：真实存在。arXiv:2509.01920 可解析（当前 v3, 2025-09-21）。
2. **发表状态**：arXiv-only（API 无 venue comment；被引 ~7）。
3. **标题/作者/年份/venue**：*Dynamic Speculative Agent Planning*；Yilin Guan, Qingfeng Lan, Sun Fei, …, Wenyue Hua（UCSB/Rutgers 等）；2025；arXiv。
4. **真正提出的机制**（full_text_obtained=部分：abs v3 + GitHub README + C3-P10 §11 的逐格转述；正文未逐节读，标注为二手）：异步在线 RL 的投机规划框架：近似 agent 提前推测后续 k 步 plan，目标 agent 验证；用 DistilBERT 回归器（expectile/asymmetric loss，τ 超参）动态预测最优 k 而非固定步长，联合优化端到端延迟与美元成本（注：C3-P10 §11 指出其训练损失用 token 数而非费率，美元仅出现在事后评测）；无需离线预热、lossless。
5. **关键数字位置**：摘要：与最快 lossless 方法效率相当，总成本 −30%、不必要成本 −60%；实验环境 OpenAGI + TravelPlanner（README 给出 4 种 approximation/target 组合与 fix/dynamic 两种模式）。具体表格编号未核实。
6. **公开代码**：https://github.com/guanyilin428/Dynamic-Speculative-Planning （摘要声明，存在）。
7. **代码是否实现论文机制**：是（外观层面）。README 提供 OpenAGI/TravelPlanner 两套实验、--pred/--no-pred、k 值、τ、offset 参数，与论文描述的动态/固定投机规划对应。
8. **是否覆盖 C3 问题**：不覆盖，同 P7 一极（前向投机 plan 链）；差异在 k 的动态化与成本感知。
9. **明确没解决什么**：历史/陈旧计算复用；事后 outcome 验证与回退（其"取消"发生在上游目标失配时）；副作用处理。
10. **overlap 建议：PARTIAL**。投机执行家族成员，用于界定 C3 对比面的边界。

## C3-P9 PASTE（撞车候选 4）

1. **存在性**：真实存在。arXiv:2603.18897 可解析（v1 2026-03-19 → v3 2026-06-16）。**注意**：v1 标题为 *Act While Thinking: Accelerating LLM Agents via Pattern-Aware Speculative Tool Execution*，v3 已改题 *Parallelizing Tool Execution and LLM Generation for Low-Latency Agent Serving*（同一 arXiv ID，系统名 PASTE 不变）。
2. **发表状态**：arXiv-only（API 无 venue comment）。
3. **标题/作者/年份/venue**：现题 *Parallelizing Tool Execution and LLM Generation for Low-Latency Agent Serving*；Yifan Sui, Han Zhao, Rui Ma, …（共 9 人）；2026；arXiv。
4. **真正提出的机制**（full_text_obtained=部分：abs v1/v3 + §1 片段 + 第三方 GitHub issue 转述；正文未逐节读）：挖掘 agent 工具调用序列中的应用层控制流规律（如"search 后必跟 summarize"），在 **LLM 仍在生成推理**时投机预执行预测的工具调用；投机结果被隔离、直到 LLM 确认才生效；联合调度工具执行与返程 LLM session 避免瓶颈移到 GPU；仅策略合规的投机动作被准入（opportunistic execution）。
5. **关键数字位置**：v3 摘要：deep research/coding/科学 agent 负载上平均任务完成时间 −43.5%、观测工具延迟降 1.8×；v1 摘要/第三方转述为 −48.5% 完成时间、1.8× 吞吐（版本间数字口径变化，引用时需注明版本）。
6. **公开代码**：未发现。
7. **代码是否实现论文机制**：n/a。
8. **是否覆盖 C3 问题**：不覆盖。投机对象仍是**未来**工具调用（前向），确认机制是等 LLM 生成完毕；无历史复用、无状态变化失效模型、无 checkpoint 回退（隔离-确认即可，因为投机结果从未生效）。
9. **明确没解决什么**：复用；结果确认失败的恢复成本建模（正文未读，摘要无）；副作用准入规则细节（第三方转述提到 policy-compliant 准入，未核实原文）。
10. **overlap 建议：PARTIAL**。投机执行家族（reasoning-time 预取），边界界定用。

## C3-P10 Cost-Aware Speculative Execution for LLM-Agent Workflows（撞车候选 5）

1. **存在性**：真实存在。arXiv:2606.07846 可解析（v1 2026-06-05）。
2. **发表状态**：arXiv-only。
3. **标题/作者/年份/venue**：*Cost-Aware Speculative Execution for LLM-Agent Workflows: An Integrated Five-Dimension Method*；Faisal Fareed（独作）；2026；arXiv。
4. **真正提出的机制**（full_text_obtained=true（主体），HTML v1 Sec. 1–12.2 已读，附录未全读）：五维设计——D1 上游未完成即以预测输入 î 启动下游（任意 DAG）；D2 决策内使用输入/输出双费率美元成本；D3 用户侧 α∈[0,1] 延迟-成本旋钮（运行时可变）与部署侧 λ($/s) 分离；D4 期望价值决策 EV=P·L_value−(1−P)·C_spec ≥ (1−α)·C_spec（失败加权成本）；D5 Beta-Binomial 后验估计 P、结构先验挂依赖类型分类法（router_k_way 先验 1/k 等）。**§3.3 准入前提**：仅 side-effect-free / 幂等 / commit-barrier 后可暂存的下游可投机，因为"错误投机靠重执行回滚，重执行能退 token 但撤不回已发出的副作用"——这是所审文献中对投机-副作用关系最明确的表述。§7.6 闭式自限性（均匀分布 k>k_crit(α) 自动 WAIT）。§11 给出与 DSP/Speculative Actions v2/Sherlock/B-PASTE 的逐维对比表（作者自述，未经第三方核实），其中 §3.1 明确把 Sherlock 归类为"post-output, pre-verification speculation（用真实上游输出 i，赌验证通过）"、把 PASTE 类归为"reasoning-time tool pre-launch"，与本文 D1"上游未产出即猜 î"区分——这套分类学对 C3 定位有直接参考价值。
5. **关键数字位置**：§7.6 k_crit 数值表（AutoReply 参数：k_crit(α=1)≈5.7 / 0.5≈3.8 / 0≈2.9）；§10 三个 worked examples；附录 D synthetic 验证套件（决策边界、P 阈值、后验收敛、流式取消、implied-λ 回收，固定种子）——**全部为合成数值验证，无真实系统实验**。
6. **公开代码**：未发现（仅决策规则伪代码 §6.5）。
7. **代码是否实现论文机制**：n/a。
8. **是否覆盖 C3 问题**：不覆盖（前向投机决策层），但两点直接相关：(a) 副作用可投机性的三分准入（side-effect-free/idempotent/commit-barrier）正是 C3 回退安全的约束面；(b) 其对 Sherlock 的归类表明"用真实输出赌验证通过+失败回滚"这一模式在 2026-06 时点已被明确命名并与前向投机区分。
9. **明确没解决什么**：历史/陈旧计算复用；真实负载评测；预测器自身成本（§14.2 自承可抵消收益）；动态拓扑 workflow（明确出范围）。
10. **overlap 建议：PARTIAL**。机制是投机执行家族的决策理论化，但其文献分类学与副作用准入规则是 C3 定位陈述中必须引用/区分的证据。

---

## 对 C3 核心问题的总结证据（只陈述证据，不下 novelty 结论）

**A. 「预测未来 action 并提前执行」一极（speculative execution for agents）已拥挤且持续增多**：Speculative Actions（2510.04371，ICLR 2026 Oral，Actor 真值匹配后提交）、DSP（2509.01920，动态 k）、PASTE（2603.18897，模式挖掘+隔离确认）、B-PASTE（2604.16469，beam 级分支假设，已核实存在性，未单列）、Cost-Aware（2606.07846，EV 决策+副作用准入）、Skim/Accio（2605.16565，web agent，已核实存在性，未单列）、Interactive Speculative Planning（2410.00079，2024，已核实存在性，未单列）、Conveyor（2406.00059，工具 partial execution，−38.8% 延迟，已核实存在性，未单列）。这些工作的共性：投机对象=**未来**计算；验证=等待权威结果（Actor 输出/LLM 生成完毕/上游完成）后比对；失配成本=丢弃并行分支或重执行；均不引入"复用已完成旧计算"的概念。

**B. 「事后验证 + 失败回退」的运行时机制已有直接先例**：Sherlock（2511.00330，MLSys 在审）把「先跑、后台验证、按相似度选择性回滚、重算」做成完整运行时（§7 全部机制含成本模型与选择性回滚规则），并宣称是首个联合探索成本/准确/延迟的框架。它与 C3 的机制差异已被压缩到一个点上：**投机对象是新鲜下游计算 vs. 历史中间计算**；失效源是 LLM 输出错误 vs. 外部状态漂移。C3-P10 的 §3.1 分类学（pre-completion vs. post-output-pre-verification vs. reasoning-time pre-launch）显示该领域已在主动自我细分——C3 若成立，其差异陈述需要超越这套已有分类。

**C. 「状态变化后复用历史中间计算（stale reuse）+ 事后验证」一侧未发现占用者**：定向检索（"stale computation reuse agents"、"reuse intermediate results LLM agent workflow cache invalidation state change"、"optimistic execution agent workflow verification" 等）返回的复用类工作全部是**事前**判定有效性：AgentReuse（C3-P3，意图+相似度分类器判定后才复用 plan）、层次缓存/工具结果缓存系统（dependency-aware invalidation，写时失效，仍是复用前判定）。未检到任何工作把「默认复用、并行低成本 outcome 验证、失败回退重算」用于历史中间计算。此为阴性证据（absence of evidence），检索覆盖有限，不能等同证据缺席。

**D. 回退/checkpoint 基础设施已存在但视角不同**：ACRFence（2603.20625）指出 agent checkpoint-restore 的语义回滚攻击（恢复后重新合成的请求与原始不逐字相同→重复扣款/凭证复活），并给 replay-or-fork 缓解——说明 C3 的"回退到 checkpoint"在 agent 设定下有已知正确性陷阱；DeltaBox（2605.22781）提供毫秒级沙箱 checkpoint/rollback；Shepherd（2605.10913）提供可逆执行轨迹（fork 134–143ms、字节级重放）。三者均为基础设施/安全视角，不含"复用+验证"的调度语义（均只核实了 abs/HTML 片段，未单列）。

**E. 状态与评测语义供给方**：ToolSandbox（C3-P1）的 world-state/milestone 体系提供了"状态变化"与"outcome 级验证"的可操作定义；Martingale MCP（C3-P5）提供了多步交互误差累积的浓度界（偏差 O(√T)、约 9 步 re-grounding 建议）；ChainCaps（C3-P4）提供了组合不变量的运行时执法样例。三者均为支撑性而非竞争性证据。

**F. 事实性勘误与风险提示（供主席引用时规避）**：
- C3-P3 摘要（93.12% 延迟降低）与 §6 正文（60.61pp）数字口径不一致。
- C3-P4 的 artifact 一节为空，全部实验结论无公开代码支撑。
- C3-P6（Sherlock）为在审稿，引用时状态可能变化；其 §7.2 的选择性回滚在 code/math 上退化为全回滚。
- C3-P7 的 ICLR 2026 Oral 信息来自作者主页与 OpenReview PDF，未经官方论文集页面确认。
- C3-P9 存在改题（v1→v3）与版本间数字差异（48.5%→43.5%）。
- C3-P10 为独作 arXiv 稿，验证全为合成套件，其 §11 对比表是单方陈述。
