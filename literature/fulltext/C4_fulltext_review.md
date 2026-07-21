# C4 (Repairable reuse / selective recomputation) 全文级文献核实

- 核实人：文献检索/核实子代理（无 novelty 裁决权；以下 overlap 分类均为证据级建议）
- 核实日期：2026-07-21
- 方法：arXiv abs 页 + arXiv HTML 全文 + 会议/DOI 页 + 官方 GitHub 仓库页，逐篇核对。只读公共网页，未 clone 仓库，未下载 PDF 进项目目录。
- 候选定义（C4）：外部状态 mutation 后，识别受影响 region（token/span/layer/subgraph）并选择性重算修复，保留未受影响计算；正确性 = repair 后 ≡ from-scratch。核心问题：相对 KV refresh / selective recomputation / CacheBlend，是否仍存在 receiver-conditioned、task-conditioned 或 agent-stage-specific 空位。

清单说明：任务给定 5 篇指定文献（P1–P5）全部核实；第 6 项主动检索命中两篇比清单内文献更直接的撞车候选（P6、P7），按要求补入；未发现需要替换掉 P1–P5 中任何一篇的理由。

---

## C4-P1 CacheBlend（指定清单 #1）

1. **真实存在**：是。arXiv abs 页（2405.16444，v1 2024-05-26，v3 2025-04-03）+ arXiv HTML 全文可解析。
2. **发表状态**：正式发表，EuroSys 2025（Twentieth European Conference on Computer Systems, Rotterdam, 2025-03-30–04-03），pp. 94–109，DOI 10.1145/3689031.3696098（HTML 版 ACM 版权头确认；微软研究院亦挂出 eurosys25-final999.pdf）。
3. **标题/作者/年份/venue**：*CacheBlend: Fast Large Language Model Serving for RAG with Cached Knowledge Fusion*；Jiayi Yao, Hanchen Li, Yuhan Liu（+ Siddhant Ray, Yihua Cheng, Qizheng Zhang, Kuntai Du, Shan Lu, Junchen Jiang；UChicago/Stanford/MSR）；2025；EuroSys '25。
4. **真正机制**（HTML 全文 §4–§6 核实）：RAG 输入含多个独立预计算 KV 的 text chunk；非前缀 chunk 直接复用会丢失与前文的 cross-attention。CacheBlend 逐层只对 **HKVD（High-KV-Deviation）token** 重算 KV（§4.2 掩码式 partial prefill），靠 Insight 1（高 KV 偏差 token 重算对 attention 偏差下降贡献最大，Figure 6）与 Insight 2（相邻层 HKVD 高度相关，Figure 8）做逐层渐进筛选（gradual filtering，Figure 9）；重算与下一层 KV 加载流水线重叠（§5），loading controller 选重算比例与存储介质。
5. **关键数字位置**：Figure 6（重算比例 vs attention 偏差，Musique 上 3 个模型）；Figure 7（KV 偏差分布，约 10–15% token 显著偏高）；§5.1 明确 "r\*% = 15% from Figure 16"（Figure 16 为质量 vs 重算比例，决定最小重算比）；端到端数字在摘要/引言：TTFT 降 2.2–3.3×、吞吐升 2.8–5×（vs prefix caching）；vs full KV reuse 绝对 F1 +0.1–0.2、Rouge-L +0.03–0.25。注：HTML 全文读到 §6 末，§7 实验节未逐表展开，上述 §7 数字引自论文自身摘要/引言。
6. **代码**：https://github.com/LMCache/LMCache （论文 §1 注明）。
7. **代码是否实现机制**：是。LMCache 仓库特性列表明确 "Non-prefix KV reuse … leverages CacheBlend to selectively recompute tokens for quality recovery"；CacheBlend 已并入生产级 LMCache（5000+ stars，vLLM 生态）。
8. **C4 格覆盖**：覆盖"影响区域识别"（HKVD token 选择，但是针对**重组合**而非 mutation）与"选择性重算恢复精度"。**不覆盖**外部状态 mutation 后的修复、receiver-conditioned 修复、agent stage。
9. **明确未解决**：(a) chunk **内容**被编辑的情形——KV store 按文本 hash，任何字段改动 = 新 chunk = 该 chunk 全部重算，无 stale-state 修复概念；(b) 单模型设定，无 receiver 变化；(c) 无 agent 多阶段/多轮状态失效；(d) 其选择器按"与 full prefill 的 KV 偏差"挑 token，P6 论文实证该选择器在 mutation 修复场景追错了对象（见 P6）。
10. **overlap 建议：PARTIAL**。机制家族（选择性 token 重算 + 以 ≡ full prefill 为质量基准）与 C4 相同，但触发条件是"chunk 重组合缺失 cross-attention"，不是"外部状态 mutation 后识别受影响区域"；无 receiver/task/stage 条件化。

---

## C4-P2 KVPR（指定清单 #2）

1. **真实存在**：是。arXiv abs 页（2411.17089，v1 2024-11-26，v2 2025-06-04）+ HTML 全文可解析。
2. **发表状态**：正式发表，ACL 2025 Findings（abs 页 Comments 栏确认 "ACL Findings 2025"；官方仓库亦称 ACL 2025）。ACL Anthology 精确条目号未核对。
3. **标题/作者/年份/venue**：*KVPR: Efficient LLM Inference with I/O-Aware KV Cache Partial Recomputation*；Chaoyi Jiang*, Lei Gao*（共同一作）, Hossein Entezari Zarch, Murali Annavaram（USC）；2025；ACL Findings。
4. **真正机制**（HTML §1–§3 核实）：KV cache offload 到 CPU DRAM 后 PCIe 传输成瓶颈（Table 1：PCIe 延迟比重算高一个数量级）。KVPR 让 CPU 先传**部分激活**，GPU 从这些激活**重算部分 KV**，同时并行传剩余 KV——用 GPU 重算掩盖 PCIe 传输。profiler + 线性整数规划 scheduler 决定计算/通信切分点。**注意力计算是精确的，无近似、无质量损失问题**。
5. **关键数字位置**：Table 1（PCIe vs 计算延迟）；§4 实验：相对 SOTA 延迟最高降 35.8%、吞吐最高升 46.2%（摘要/引言；§4 逐表未展开）。
6. **代码**：https://github.com/chaoyij/KVPR 。
7. **代码是否实现机制**：是。基于 FlexGen/HF Transformers，提供 `--kv-partial` 开关及 latency/throughput 两组复现命令。
8. **C4 格覆盖**：仅沾边"部分重算"这一手段；重算目的是 **I/O 重叠**而非修复 stale 状态；无影响区域识别、无 mutation、无 receiver 条件。
9. **明确未解决**：一切与"状态变更后哪些 KV 失效"相关的语义问题；其重算集合由带宽/算力比决定，与数据内容无关。
10. **overlap 建议：ADJACENT**。共用"partial recomputation"一词与手段，但问题域（offload 传输隐藏）与 C4（mutation 修复正确性）正交。

---

## C4-P3 dKV-Cache（指定清单 #3）

1. **真实存在**：是。arXiv abs 页（2505.15781，v1 2025-05-21）+ 官方仓库可解析。
2. **发表状态**：正式发表，NeurIPS 2025（一作主页 "2025.09: Three papers (dKV-Cache, …) accepted by NeurIPS'25"；官方仓库标题 "[NeurIPS'25]"；多篇 2026 论文参考文献写作 "In Advances in Neural Information Processing Systems"）。OpenReview 条目号未核到。
3. **标题/作者/年份/venue**：*dKV-Cache: The Cache for Diffusion Language Models*；Xinyin Ma, Runpeng Yu, Gongfan Fang（+ Xinchao Wang；NUS xML Lab）；2025；NeurIPS 2025。
4. **真正机制**（abs + 官方仓库 README 核实；**论文全文未取得**）：扩散语言模型双向注意力无法直接用 KV cache；观察到不同 token 在 denoising 过程中表示动态不同，提出 delayed + conditioned 的 K/V 缓存：表示已稳定的 token 缓存复用、其余刷新。两个变体 Decode（近无损，2–10× 加速）与 Greedy（更激进、有质量折损）。training-free，在 LLaDA / Dream 上验证。
5. **关键数字位置**：abs 给出 2–10× speedup；仓库 README 含 pipeline 图与 benchmark 结果表（图片）；论文内部表号未取得（full_text_obtained=false）。
6. **代码**：https://github.com/horseee/dKV-Cache 。
7. **代码是否实现机制**：是。提供 Dream/LLaDA 的 modeling 与 generate 补丁，`use_cache/cache_type/cache_steps` 等参数对应缓存刷新间隔与变体。
8. **C4 格覆盖**：概念上沾边"哪些 token 需要刷新"的判别（按表示稳定性），但触发是**扩散解码内部步间动态**，不是外部状态 mutation；模型类别不同（DLM 非 AR）；无 receiver/task/stage 条件。
9. **明确未解决**：AR LLM 的 mutation 修复；agent 场景；与 from-scratch 等价的正确性刻画（Greedy 变体明确有质量折损）。
10. **overlap 建议：ADJACENT**。"按 token 动态选择刷新/复用"的直觉相似，但问题域与模型范式不同，证据上不构成撞车。

---

## C4-P4 Prompt Cache（指定清单 #4）

1. **真实存在**：是。arXiv abs 页（2311.04934，v1 2023-11-07，v2 2024-04-25）+ 官方仓库可解析。
2. **发表状态**：正式发表，MLSys 2024（abs 页 "To appear at MLSys 2024"；一作主页确认 accepted；引用格式 Proceedings of Machine Learning and Systems 2024）。
3. **标题/作者/年份/venue**：*Prompt Cache: Modular Attention Reuse for Low-Latency Inference*；In Gim, Guojun Chen, Seung-seob Lee（+ Nikhil Sarda, Anurag Khandelwal, Lin Zhong；Yale）；2024；MLSys。
4. **真正机制**（abs + 官方仓库 README 核实；**论文全文未取得**）：用 Prompt Markup Language schema 显式声明可复用 prompt module，预计算其 attention states 并按位置占位符保证位置正确性，跨请求拼接复用。**不做任何重算**（full KV reuse 路线）。
5. **关键数字位置**：abs：TTFT 改善 GPU 8× / CPU 60×，精度不降；仓库 demo 给出 RTX 4090 上 286.9ms→78.2ms 实例；论文内部表号未取得（full_text_obtained=false）。
6. **代码**：https://github.com/MachineLearningSystem/24MLSYS-prompt-cache （另有镜像 yale-sys/prompt-cache）。
7. **代码是否实现机制**：是。PML schema 编译器、module/union/parameter 机制、LongBench 精度与时延评测脚本齐全。
8. **C4 格覆盖**：只覆盖"模块化复用"；**显式放弃修复**（CacheBlend 论文 §3.3 指出其忽略 cross-attention，多 chunk 场景质量显著下降）。
9. **明确未解决**：非前缀复用的 cross-attention 损失；任何 mutation/失效/修复语义。
10. **overlap 建议：ADJACENT**。C4 的"全复用不修复"对照基线；本身不含 repair 机制。

---

## C4-P5 DroidSpeak（指定清单 #5）

1. **真实存在**：是。arXiv abs 页（2411.02820，v1 2024-11-05，v4 2025-07-14）+ USENIX 会议 PDF 可解析。
2. **发表状态**：正式发表，NSDI 2026（USENIX system files 挂出 nsdi26-liu-yuhan.pdf；MSR 作者主页列 "DroidSpeak: KV Cache Sharing Across Fine-tuned Model Variants, NSDI'26, May 2026"；会议版标题与 arXiv 版不同，已更名）。
3. **标题/作者/年份/venue**：arXiv 版 *DroidSpeak: KV Cache Sharing for Cross-LLM Communication and Multi-LLM Serving*；Yuhan Liu, Yuyang Huang, Jiayi Yao（+ Shaoting Feng, Zhuohan Gu, Kuntai Du, Hanchen Li, Yihua Cheng, Junchen Jiang, Shan Lu, Madan Musuvathi, Esha Choukse；UChicago/MSR）；2026（会议版）；NSDI '26。
4. **真正机制**（abs 核实；**全文未取得**）：同架构、不同微调的 LLM 之间共享前缀 KV cache；首个跨模型 KV 共享质量研究；发现只需**选择性重算少数层**、复用其余层即可近乎无损；逐层重算与 KV 加载流水线重叠。最高 4× 吞吐、约 3.1× 更快 prefill，F1/Rouge-L/code-similarity 损失可忽略。
5. **关键数字位置**：abs 给出 4×/3.1×；arXiv v4 含 benchmark 构建（模型对）描述；论文内部表号未取得（full_text_obtained=false）。
6. **代码**：未找到专用公开仓库（MSR 页面有 "Project" 链接，未确认内容；arXiv 摘要未给代码 URL）。
7. **代码是否实现机制**：无法确认（未见仓库）。
8. **C4 格覆盖**：覆盖 **receiver-conditioned 选择性重算**——接收方模型不同（fine-tuned variant）时重算层子集；粒度是 **layer** 而非 token/span。不覆盖外部状态 mutation（其"变化"是模型身份而非上下文内容）、无 agent stage、无"哪些 token 受影响"的识别。
9. **明确未解决**：同一 receiver 内上下文内容变更后的修复；mutation 结构刻画；重算集合按层选而非按受影响区域选。
10. **overlap 建议：PARTIAL**。是目前唯一覆盖 receiver-conditioned 重算的证据，但维度单一（仅 receiver 轴、仅 layer 粒度），与"外部状态 mutation 修复"不重合。

---

## C4-P6 Models Take Notes at Prefill: KV Cache Can Be Editable and Composable（主动检索命中，撞车候选 A）

1. **真实存在**：是。arXiv abs 页（2606.17107，v1 2026-06-14）+ HTML 全文可解析。
2. **发表状态**：arXiv-only（2026-06，v1；未见会议录用信息）。
3. **标题/作者/年份/venue**：*Models Take Notes at Prefill: KV Cache Can Be Editable and Composable*；第一作者/提交者 Bojie Li（ResearchGate 条目亦列 Bojie Li；**完整作者列表未从页面提取**）；2026；arXiv preprint。
4. **真正机制**（HTML §1–§5 核实）：直接研究 C4 的核心情形——前缀缓存中**一个字段（field）变更**使下游全部失效。因果实验证明：prefill 时模型已把 field-conditioned 结论写进下游 aggregator/delimiter token 的 KV（"notes"），field 自身 KV 对决策影响 <1%；据此给出三种修复：(i) 重算受影响下游 suffix（recovery 1.0，贵）；(ii) field+selective@K 只重算 field + 因果效应最高的 K 个下游 note token（便宜但**不可靠**，K\* 强模型依赖：8B 时 ≈4，4B 时 >64）；(iii) append-only **erratum**（O(1)，鲁棒默认，P(correct)=1.00）；另外 field-only 原位刷新（~1% 计算）**由 CoT 门控**：有 CoT recovery 1.00、无 CoT 0.00。compose 能力：预编译 skill 的 KV 可 RoPE 重定位拼接（logit cosine 0.90–0.999，12 个模型），edit+compose 统一 agent 与 full recompute 决策一致、延迟最高低 14.9×。
5. **关键数字位置**：Figure 2（editing landscape：stale/field-only/CacheBlend 失败 vs erratum 成功；CoT 分裂）；Figure 3（四个因果探针：locality patching、suffix concentration、linear probing、knockout）；Figure 5（K\* 模型依赖）；Table 1（KV editing vs ROME/LoRA 权重编辑：交叉请求污染 1.0、30–50× 慢）；§7 用户记忆应用（LoCoMo，transplant ≡ full recompute）；§9 vLLM 在线评测（98.5% vs 1% 前缀命中率，p90 TTFT 降 53–398×）。
6. **代码**：摘要/正文未见代码 URL（未找到）。
7. **代码是否实现机制**：无法确认。
8. **C4 格覆盖**：**三格全覆盖**——外部状态 mutation 后的 repair（field 变更→erratum/选择性重算）、影响区域识别（下游 note token，且给出"受影响区域≠内容变化区域"的因果证据）、并实证 **CacheBlend 式 KV 偏差选择器在此场景失效**（"chases changed keys rather than the tokens that memoized the conclusion"）。评测直接在 agent 场景（τ²-bench 工具 agent，轨迹中途状态变更使 cache staleness 成为一等正确性问题；用户记忆；在线 vLLM serving）。
9. **明确未解决/边界**：(a) 只覆盖"字段值变更"一类 mutation，未给一般 mutation 结构分类；(b) receiver 变化（跨模型）不在编辑场景内（compose 是同模型拼接）；(c) field+selective@K 被作者自己判为" genuine but unreliable "，未给出可靠选择性修复的通用条件；(d) task-conditioned 修复未讨论（决策任务单一范式：门控决策 + QA）。
10. **overlap 建议：DIRECT**。mutation→影响区域识别→选择性修复→以 ≡ full recompute（decision-identical）为正确性标准，且含 agent 场景与部分边界刻画（CoT 门控、K\* 模型依赖），与 C4 核心命题逐点对齐。残余差异仅在 receiver 轴与 mutation 结构的一般性。

---

## C4-P7 KEEP（主动检索命中，撞车候选 B）

1. **真实存在**：是。arXiv abs 页（2602.23592，v1 2026-02-27，v2 2026-03-17）。
2. **发表状态**：arXiv-only（未见会议录用信息）。
3. **标题/作者/年份/venue**：*KEEP: A KV-Cache-Centric Memory Management System for Efficient Embodied Planning*；提交者 Zebin Yang（**完整作者列表未从页面提取**）；2026；arXiv preprint。
4. **真正机制**（abs 核实；**全文未取得**）：具身规划 agent 的记忆频繁更新导致 KV 复用收益被抵消。三部分：(1) Static-Dynamic Memory Construction——混合粒度 memory 分组，减少记忆更新引发的 KV 重算；(2) Multi-hop Memory Re-computation——动态识别 memory 组之间重要的 cross-attention 并迭代重建交互（即 mutation 后选择需要重算的组间交互）；(3) Layer-balanced Memory Loading 均衡各层加载与重算。
5. **关键数字位置**：abs：ALFRED 上相对文本记忆 2.68× 加速且精度损失可忽略；**相对 CacheBlend（EuroSys'25）成功率 +4.13%、TTFT 降 1.90×**——作者直接把 CacheBlend 当 mutation 场景基线并超越。论文内部表号未取得（full_text_obtained=false）。
6. **代码**：abs 称 "Our code is available on this https URL"，具体 URL 未从提取文本获得。
7. **代码是否实现机制**：无法确认。
8. **C4 格覆盖**：覆盖 **agent 场景下外部状态（环境/记忆）mutation 后的选择性重算**——更新区域以 memory group 为粒度识别、组间 cross-attention 迭代修复。不覆盖 receiver 变化；正确性标准是"精度损失可忽略/+4.13% 成功率"而非 ≡ from-scratch；无"何种 mutation 可修复"的边界刻画。
9. **明确未解决**：repair 后与 from-scratch 的等价性；receiver/task 条件化；修复可靠性边界。
10. **overlap 建议：PARTIAL（强）**。占据了"agent-stage mutation → 选择性重算"这一格的重要部分，但粒度为启发式 memory group、无正确性等价刻画、无边界理论。

---

## 对 C4 核心问题的总结证据（只陈述证据）

**CacheBlend 的 mutation 边界覆盖到哪**：全文证据显示其"变化"仅为** chunk 重组合**（已有不变 chunk 出现在新位置/新邻居），修复目标是补上与前文的 cross-attention；预计算 chunk 内容本身被假定为不可变——KV store 按文本 hash，任何内容编辑都使该 chunk 整体失效并整体重算，论文与系统均无"stale 状态修复"概念。重算比例为 token 级 10–20%（r\*=15%，Figure 16），质量基准是 ≈ full prefill。单模型、单轮 RAG，无 receiver/task/stage 条件化。

**"外部状态 mutation 后的 repair"是否已有工作**：有，且至少两篇直接命中。P6（2026-06，arXiv）在同一模型内覆盖 field mutation → 受影响区域（下游 note token）识别 → 三种修复路径，并给出部分边界（CoT 门控 field-only 编辑；field+selective@K 不可靠且 K\* 模型依赖；CacheBlend 式选择器在此失效的实证）。P7（2026-02，arXiv）覆盖具身 agent 记忆更新 → memory-group 粒度选择性重算，并以 CacheBlend 为基线胜出。两篇均为 arXiv-only、均未正式发表。

**receiver-conditioned 空位**：证据显示仅 P5（NSDI'26）覆盖 receiver 变化（同架构微调变体间），粒度为 layer、触发为模型身份而非内容 mutation；"receiver 变化 × 内容 mutation" 同时条件化的修复在所核文献中无证据。P6 的 compose 是同模型拼接，明确不算 receiver 变化。

**task-conditioned 空位**：所核 7 篇中无任何一篇按下游任务条件化修复策略（P6 用单一门控决策 + QA 范式；其余无），证据上该格为空。

**边界刻画（何种 mutation 可修复/不可修复）**：仅 P6 给出局部刻画（限 field-value 变更、单决策点、CoT 依赖）；一般性的 mutation 结构分类（什么结构可 O(K) 修复、什么必须 suffix 重算）在所核文献中无证据。

**其他相邻线索（未做全文级核实，仅记录）**：Continuum（arXiv 2511.02230，多轮 agent 的 KV cache TTL 失效管理——只有失效没有修复）；KV Packet（arXiv 2604.13226，recomputation-free 的 context-independent 缓存——免修复路线）；EPIC / CacheSlide / MPIC / KVLink（position-independent/aware 复用 + 边界 token 重算，P6 相关工作节自认其 compose 能力源于 EPIC/CacheSlide）；VeriCache（2026-05，arXiv，lossy KV → lossless）。这些若需纳入裁决应另行全文核实。
