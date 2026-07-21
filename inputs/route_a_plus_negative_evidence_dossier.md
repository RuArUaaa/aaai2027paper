
# Route A+ Negative Evidence Dossier

> 生成者:独立"负面证据整理者"任务,2026-07-21。仅供追溯与新项目奠基,不设计下一版实验。
> 仓库:`/Users/zijian_nong/research/aaai2027-route-a-plus`,分支 `route-a-plus-codex`,
> 起始 HEAD `045eedf`。本文档为只读证据整理产出,未修改/未提交任何既有文件或 frozen evidence。
> 证据等级标注贯穿全文:`RAW_REPRODUCIBLE`(有可独立复核的 JSON/数据文件)、`CODE_CONFIRMED`
> (亲自读过实现代码确认)、`DOCUMENTED`(仅见于叙事文档,未独立复算)、`SUMMARY_ONLY`(仅见于摘要,
> 无原始数据)、`UNRESOLVED`(证据不足或矛盾未消)。所有后续复核结论标注 `POST_HOC_DIAGNOSTIC`,
> 不得与正式判定混为一谈。

---

## 1. Executive Summary

- **负面案例总数:25 个**(NEG-01 至 NEG-25),覆盖任务书第六节要求逐项核查的全部 30 个具体条目
  (部分同根因条目合并入同一案例,详见 §4 前的覆盖映射表)。
- **按主类别计数**(部分案例有次类别,以主类别计入):
  - N1 真实科学负结果:**4** 个(NEG-01、NEG-17、NEG-18、以及 NEG-17 与 NEG-18 共享的
    no_change 噪声地板发现)
  - N2 伪正结果:**1** 个(NEG-12,`..` mtime 伪影)
  - N3 测量不可辨识:**4** 个(NEG-10、NEG-13、NEG-14、NEG-17 次类别)
  - N4 指标/分析语义错误:**4** 个(NEG-08、NEG-11、NEG-15、NEG-16)
  - N5 testbed/接口不匹配:**4** 个(NEG-07、NEG-09、NEG-10 次类别、NEG-25)
  - N6 harness/工程失败:**5** 个(NEG-02 至 NEG-06,AutoCodeRover 时代)
  - N7 治理与过度工程化:**2** 个(NEG-02 次类别、NEG-21)
  - N8 统计/风险主张:**2** 个(NEG-20;NEG-23 为"经核查未确认"的对照条目,不计入失败数)
  - N9 概念漂移:**3** 个(NEG-19、NEG-22、NEG-25 次类别)
  - N10 novelty 冲突:**1** 个(NEG-25 次类别;另有独立的 novelty scoop-check 结论见 §6)
  - 未分类/跨领域文档记录:**1** 个(NEG-24,任务依赖未安装 → outcome 永远 UNKNOWN,贯穿 v7/v8)
- **原始 idea 是否被直接证伪:UNRESOLVED,但有明确方向性证据。** 迄今为止的全部三代 testbed
  (AutoCodeRover M0-M3、mini-swe-agent v7、SWE-agent v8 D2/D3)得到的最接近原始问题的答案是:
  在这三个 testbed 里,**"receiver-specific typed/executable contract 让 bytes-different 的
  重算结果被安全判定为等价"这一核心机制,一次都没有被真实测量过、也没有被真实证伪过**——
  v7 的正信号被证明是测量伪影(NEG-12),v8 唯一被真实测量的"contract"(K2,行多重集合
  canonicalizer)贡献恒为零,但 K2 本身只是一种粗糙的结构规范化,并非原始设想的"typed/executable
  contract"的严肃实现(NEG-18、NEG-22)。**被证伪的是"K2 这个特定 canonicalizer 在这三个
  testbed 上有非零增量收益",不是"receiver-conditioned typed contract 这个更广的假设本身"。**
- **原始 idea 中完全未被真实实验触碰的部分**:receiver-conditioned validity(同一 producer
  产物对不同 consumer 有不同 verdict)、Repairable 复用档位、latent/KV state 直接传递、
  outcome-level 验证(全部三代 testbed 都从未运行 patch/test 判定,见 NEG-24)。见 §8。

---

## 2. Original Idea and Evaluation Target(原始构想,不以后期 pivot 改写)

> **固定问题**(不得用后期 exact-caching 结果重新定义):
> *After a producer computation changes, can a preregistered receiver-specific contract
> preserve downstream computation even when the full artifact or invocation is no longer
> byte-identical?*

原始核心不是普通 response cache、tool cache、repository mutation 或 incremental build。核心是:

1. computation state 随 agent 间消息一起传递,而不只是文本内容;
2. **receiver-conditioned validity**——同一份 producer 产物对不同 consumer 可能有不同的
   有效性判定;
3. 复用状态应分三档:**Exact / Repairable / Invalid**;
4. 在字节不完全相同(bytes-different)时,仍可能通过 typed/executable contract 安全复用;
5. B4(typed contract 截断)应**严格超过** B3.5(exact byte identity)——这是整条 idea 存在
   的理由:如果 B4 最终等于 B3.5,idea 就退化为普通 exact cache。

**判断准则**(贯穿全文档):后续每一个实验,都要标注它是(a)在检验这个问题本身;(b)这个问题的
必要 baseline(如 exact-identity 对照);(c)一种代理实验(如文本 diff heuristic);还是
(d)已经 pivot 成另一个问题(如"字节相同能省多少")。**本文档发现:三代 testbed 中,真正
测量过(c)的次数远多于(a),而(a)本身在任何一代 testbed 里都没有被完整测量过一次**——
这是全文档最核心的结论,详见 §7/§8。

---

## 3. Chronological Timeline

### 阶段 0:最初 KV/LatentMAS 火花(2026-07-03 前,repo 之外)

原始火花早于本仓库 git 历史,未在仓库内找到独立可引用的一手记录(`EVIDENCE_LEVEL=UNRESOLVED`,
仅能从后续文档中推断其存在)。仓库内最早的落地形式是 `docs/paper_idea_and_writing.md`、
`docs/engineering_contract.md`、`docs/experiment_spec_v1.md`(2026-07-03 首次提交),已经是
"KV-reuse across multi-agent RAG pipeline"这一具体化实现,而非最原始的"communication as
computation-state transfer"表述。

### 阶段 1:早期六次 null(2026-07-03~07-11)

- **目标**:在 HotpotQA 多智能体 RAG(Task A)与 HumanEvalFix(Task B)两个真实工作流上,
  验证 KV cache 重用+选择性 repair 是否能在保持下游任务正确性的前提下节省计算。
- **得到的证据**:见 NEG-01。E0 100-trace 批量、identity 配对对照、判别式扰动探针、Task B
  全量 164 题、pos_shift 判决实验、S0 24-模板 held-out 跨模型确证性重跑——六次独立尝试,
  全部未能证明"KV 复用/修复导致的额外翻转率显著大于恒等对照/噪声地板"。
- **为什么停止**:S0(第六次/确证性重跑)是预注册的终局实验,结局按预注册分支判定为"抢救终止,
  不进 S1",且诊断出旧 8-模板 discovery 基准数字是判别集过拟合(discovery-set overfitting)。
- **是否触及原始 hypothesis**:**部分触及,但只测了"Exact vs Repairable"这一个维度下的一个
  代理终点(D3 严格 EM 翻转率),从未测试 receiver-conditioned validity(所有六次实验都只有
  一个固定 receiver,没有比较"同一 producer 产物对不同 receiver 是否有不同 verdict")。**

### 阶段 2:Route A / Route A+ 早期(M0-M3,2026-07-13~07-17)

- **目标**:把"computation reuse validity"问题从 KV 张量层面迁移到"agent tool-call 结果的
  跨 turn/跨 task 复用"层面,用 AutoCodeRover(真实 SWE-bench 修复 agent)作为 testbed,
  尝试在 M2/M3 建立 byte-cutoff 假设的最小 hand-check。
- **得到的证据**:见 NEG-02 至 NEG-07、NEG-21。工程层面的 harness 问题(多层 transport/
  supervisor 架构、conv_round_limit 错配、projection 落盘顺序 bug、evidence 与
  clean-worktree guard 自冲突)反复出现;M3 的 source-backed validator 被发现可以被伪造
  provenance 骗过。
- **为什么停止**:这一era 没有正式的单一停止点,而是持续累积工程债务,最终在 Decision A
  阶段(见阶段 3)触发预先约定的止损规则。
- **是否触及原始 hypothesis**:**几乎没有。** 这一 era 的绝大部分工作量花在让 harness
  本身能可信运行,没有产出任何关于 edge-observable byte cutoff 假设本身的真实测量。

### 阶段 3:AutoCodeRover Decision A(2026-07-18~07-19)

- **目标**:在 M0-M3 基础设施上,正式跑通 G0(最小 preflight)。
- **得到的证据**:见 NEG-03、NEG-04、NEG-05、NEG-06。三次 G0 CPU preflight 依次死于
  `conv_round_limit` 错配、projection 落盘顺序 bug(遗留自 M3)、`sys.setprofile` 与
  CPython frozen module 冲突。
- **为什么停止**:第三次失败触发预先约定的"Option B rule 10"——同一协议第二次失败即永久停止。
  `docs/route_a_plus_v7_testbed_and_minimal_g0_prereg_draft_2026-07-19.md:5-10` 原话:
  "三次失败全部是 harness 自伤(harness/tooling 缺陷),没有一次让 edge-observable byte
  cutoff 假设本身接受过实测检验。假设未被证伪,也未被支持。"
- **是否触及原始 hypothesis**:**零。** 三次尝试全部死于 harness 自身,连一次探针都没有真正
  跑进模型调用。

### 阶段 4:mini-swe-agent v7(2026-07-19~07-20)

- **目标**:换用极简的 mini-swe-agent(单层 driver,无多层审计)作为 testbed,先做 G0
  (静态投影检查)再做 G1(6-task pilot matrix,测 headroom)。
- **得到的证据**:见 NEG-08 至 NEG-17。G0 PASS(有 documented limitations,NEG-10)。
  G1 matrix-v1/v2 字面结果 1.48pp/1.86pp,均 <5pp 阈值;matrix-v2 的 no_change 噪声地板
  (3.73pp)大于信号本身(NEG-17)。
- **为什么停止**:预注册"若 v2 仍未达标即接受 FAIL 止损,不再发起 v3"——按此止损。
- **是否触及原始 hypothesis**:**是官方判定为"否"的,但这个"否"本身站不住**——因为 G1 唯一
  的正信号来源(Oracle arm)后来被独立复核证明 100% 来自 `..` 目录 mtime 伪影(NEG-12),
  而不是内容差异。所以 v7 真正测出来的是:**在这个 testbed 上,零 headroom** 这个数字本身
  是可信的(经 B3.5-I 完整 invocation 级复算确认为 0.0000pp,NEG-08 附表),但"零"是否
  意味着"假设为假"仍不确定,因为整个测量装置(difflib Oracle、command-only 对齐)从未被
  证明有能力探测到真实存在的等价性(NEG-11、NEG-15)。

### 阶段 5:v7 独立复核(2026-07-20)

- **目标**:lead reviewer 对 v7 官方结论做独立复核。
- **得到的证据**:六项质疑全部 CONFIRMED(NEG-08、NEG-11、NEG-12、NEG-15、NEG-16、以及
  G0 因果链质疑 NEG-10)。
- **为什么停止**:复核本身是一次性任务,完成后交还负责人裁决。
- **是否触及原始 hypothesis**:复核**没有产生新的一手数据**,只是重新解读已有数据
  (`POST_HOC_DIAGNOSTIC`),但把"v7 官方数字支持假设为假"降级为"v7 测量装置从未真正测过
  假设",这是一次重要的范围收窄。

### 阶段 6:v8 identifiability-first structural replay(2026-07-20)

- **目标**:吸取 v7 教训,重新设计:结构阶段零模型调用(trace-conditioned replay,复用冻结
  trajectory 作基线),先建立 100% 可复现的 identifiability gate(D2 控制组),再做真正的
  read-set mutation + headroom 测量(D3)。
- **得到的证据**:D2 控制组 identifiability gate 高比例复现(R2R B3.5-I=74/76=97.37%,
  唯一例外可解释为 readdir 顺序非确定,NEG-13);D3 gate 全部四项判据 FAIL(pooled headroom
  0.0pp,positive task/strata=0,K2 贡献=0,NEG-18)。
- **为什么停止**:预注册明确的止损条件("headroom <5pp")触发,负责人接受止损闭合。
- **是否触及原始 hypothesis**:**是目前三代 testbed 中唯一一次真正测量装置本身被验证可信
  (identifiability gate 高比例通过)之后,再去测原始问题的尝试**。得到的答案很窄但可信:
  **在这 6 个 SWE-bench task、这一个 read-set mutation 设计、K2 这一个 canonicalizer 下,
  contract-incremental headroom 精确为 0。** 这不等于"receiver-conditioned contract
  在任何 testbed 下都不可能有非零收益",但目前没有任何证据支持它有。

### 阶段 7:后续 exact-cache pivot 风险(尚未发生,记为风险登记)

- v8 收尾文档已经出现"11.37% coverage 完全来自 exact-invocation 平凡匹配"这类表述
  (NEG-19),如果下一个项目不警惕,很容易把"exact cache 在某些 stratum 下命中率高"重新
  包装成"contract-based reuse 有效",这正是 N9 概念漂移最容易发生的位置,记入 §10
  设计规则第一条。

---

## 4. Negative-Case Master Table

**覆盖映射**(任务书第六节 30 项 → 本表 25 个案例;凡合并的项在"备注"列注明):

| # | 任务书条目(节选) | 案例 | 备注 |
|---|---|---|---|
| 1 | 最早六次共享知识块/KV/prefix reuse null | NEG-01 | |
| 2 | AutoCodeRover 多层 harness 导致科学实验迟迟未开始 | NEG-02 | |
| 3 | conv_round_limit 与真实对话轮数错配 | NEG-03 | |
| 4 | primary projection 在 ancillary assertion 之后落盘 | NEG-04 | |
| 5 | sys.setprofile 与 CPython frozen module 伪路径冲突 | NEG-05 | |
| 6 | evidence 输出与 clean-worktree guard 自冲突 | NEG-06 | |
| 7 | internal typed object 不是 consumer-visible interface | NEG-07 | |
| 8 | invocation metadata 被错误用于推断 result equivalence | NEG-07 | 与#7同根因合并 |
| 9 | edge exact factorization 被误称为 B4 | NEG-22 | |
| 10 | mini-swe-agent 缺少真实 fan-out | NEG-09 | |
| 11 | G0 probe projection 与完整 model invocation 因果链未闭合 | NEG-10 | |
| 12 | v7 B3.5 实现语义与冻结定义错位 | NEG-08 | |
| 13 | v7 difflib Oracle 出现观察到的 false cutoff | NEG-11 | |
| 14 | `..` mtime 造成全部正 headroom | NEG-12 | |
| 15 | 未排序 find 破坏 byte reproducibility | NEG-13 | |
| 16 | 相同输入下模型 serving 输出不同 | NEG-14 | |
| 17 | command-only 对齐忽略 prior history 差异 | NEG-15 | |
| 18 | W_a 只是 single-step token proxy | NEG-16 | |
| 19 | no_change noise 高于 mutation signal | NEG-17 | |
| 20 | K2 contract incremental headroom = 0 | NEG-18 | |
| 21 | D3 中 positive task/stratum = 0 | NEG-18 | 与#20同一 gate 数据集合并 |
| 22 | 11.37% coverage 全部来自 exact invocation | NEG-19 | |
| 23 | K3/K4 post-hoc selection bias | NEG-20 | |
| 24 | source-backed validator 接受伪造 provenance | NEG-21 | |
| 25 | 60 个相关 microcases 误当独立风险样本 | NEG-23 | 经核查未确认违规,见案例正文 |
| 26 | bootstrap 被过度解释 | NEG-23 | 经核查未确认违规,附于同案例 |
| 27 | exact caching 逐渐取代原始 B4 idea | NEG-22 | 与#9同根因合并 |
| 28 | sound deterministic 语义下 cascade identity 理论矛盾 | NEG-14 | 作为 NEG-14 的理论层结论 |
| 29 | generic Bash read-set 完整追踪一周不可行 | UNKNOWN | 未找到独立可引用证据,不编造 |
| 30 | 任务依赖未安装,无法验证 patch correctness | NEG-24 | |

| Case ID | 名称 | 阶段 | 主类别(次类别) | Evidence Level | 是否值得重复 |
|---|---|---|---|---|---|
| NEG-01 | 早期六次自然工况复用 null | 2026-07-03~07-11 | N1 (N8) | RAW_REPRODUCIBLE | YES_AS_CONTROL |
| NEG-02 | AutoCodeRover 四层 harness 过度工程化 | M0-M3 | N7 (N6) | DOCUMENTED | NO |
| NEG-03 | conv_round_limit 错配 | Decision A G0 attempt 1 | N6 | CODE_CONFIRMED | NO |
| NEG-04 | Projection 落盘顺序 bug | M3 / Decision A G0 attempt 2 | N6 | RAW_REPRODUCIBLE | NO |
| NEG-05 | sys.setprofile vs frozen posixpath | Decision A G0 attempt 3(永久止损) | N6 | RAW_REPRODUCIBLE | NO |
| NEG-06 | Evidence 输出与 clean-worktree guard 自冲突 | M0-M3 早期 | N6 | DOCUMENTED | NO |
| NEG-07 | 自由文本 consumer interface,typed object 不可见 | M2/M3,并延续到 v8 D4 | N5 | DOCUMENTED | YES_AFTER_REDESIGN |
| NEG-08 | B3.5 测量定义与冻结定义错位 | v7 | N4 | CODE_CONFIRMED | NO(需先修实现) |
| NEG-09 | mini-swe-agent/SWE-agent 无真实 fan-out | v7 testbed 选择 + v8 D4 | N5 | DOCUMENTED | YES_AFTER_REDESIGN |
| NEG-10 | G0 probe projection 因果链未闭合 | v7 G0 | N3 (N5) | DOCUMENTED | YES_AFTER_REDESIGN |
| NEG-11 | difflib Oracle 无下游验证,false cutoff | v7 G1 | N4 | RAW_REPRODUCIBLE | NO |
| NEG-12 | `..` mtime 伪影 | v7 G1 / v8 D2 | N2 | RAW_REPRODUCIBLE | NO(已修复,见 NEG-13 关联) |
| NEG-13 | 未排序 find 非确定性 | v8.1 control gate | N3 | RAW_REPRODUCIBLE | YES_AS_CONTROL |
| NEG-14 | Serving 非确定性 + cascade-identity 假设破裂 | v7 pilot(PD-6)+ matrix-v2(PD-3) | N3 | RAW_REPRODUCIBLE | YES_AS_CONTROL |
| NEG-15 | Command-only 对齐忽略 prior 分歧 | v7 pair_align | N4 | CODE_CONFIRMED | NO |
| NEG-16 | W_a 单步 token 减法代理量 | v7 pair_align | N4 | CODE_CONFIRMED | NO |
| NEG-17 | no_change 噪声地板高于信号 | v7 matrix-v2 | N1 (N3) | RAW_REPRODUCIBLE | YES_AS_CONTROL |
| NEG-18 | D3 结构性 headroom 决定性零结果(含 K2=0) | v8 D3 | N1 | RAW_REPRODUCIBLE | NO(该 testbed/protocol 下) |
| NEG-19 | 11.37% coverage 全部来自平凡 exact match | v8 D3 | N9 | RAW_REPRODUCIBLE | — |
| NEG-20 | K3/K4 post-hoc 候选,selection bias 风险 | v8 收尾 | N8 | DOCUMENTED | UNRESOLVED |
| NEG-21 | Source-backed validator 接受伪造 provenance | M3 mutation manifest | N7 | DOCUMENTED | NO |
| NEG-22 | B4 承诺退化为 exact-byte match | v7→v8 全程 | N9 | DOCUMENTED | — |
| NEG-23 | N=60/4.87% 界:核查独立性假设 | TraceBuild Phase 0 | N10(对照,未确认违规) | DOCUMENTED | — |
| NEG-24 | 任务依赖未安装,patch correctness 全程 UNKNOWN | v7 + v8 全程 | (跨类别) | RAW_REPRODUCIBLE | — |
| NEG-25 | TraceBuild 全上下文 prompt 设计使 static=runtime | TraceBuild Phase 1 GPU discovery | N5 (N9/N10) | RAW_REPRODUCIBLE | YES_AFTER_REDESIGN |

---

## 5. Deep Dives

### NEG-01:早期六次自然工况复用 null

**当时想证明什么**:KV cache 重用 + 选择性 repair,在真实多智能体工作流(Task A HotpotQA
RAG、Task B HumanEvalFix)下,不会显著增加下游任务翻转率(EM/pass@1)。预计正结果:超额翻转率
(相对恒等对照)的 95% CI 应明确大于 0 且有实际量级,才能支持"需要风险控制模型"这一论文核心
卖点。

**实际发生了什么**(`runs/STATUS.md`,`EVIDENCE_LEVEL=RAW_REPRODUCIBLE`):
1. E0(100-trace,4076 pairs):`d3_flip_repair=4.22%`,但 D1-D3 Spearman rho=0.0283
   (p=0.071,不显著)——D1 完全无法预测 D3。
2. Identity 配对对照(1000-pair):超额翻转 +0.10%,95% CI `[-0.48%, +0.73%]`,含 0。
3. 判别式扰动探针(400 traces,4 种扰动):四种扰动的超额翻转 CI 全部含 0,D1 与超额翻转
   相关系数 rho=0.0227(p=0.65)。
4. Task B 全量(164 题):超额翻转 -1.22%,95% CI `[-3.05%, 0.00%]`,非劣性判 GO。
5. pos_shift(N=90,6 档位移量):D1 均值无单调上升趋势,rho=0.0261(p=0.807)。
6. S0 24-模板 held-out 确证性重跑:旧 8-模板基准(`ΔD1=+0.130`)在新 held-out 模板上
   `完全没有复现`;非-KL 指标(D2)方向相反(repair 让 D2 显著变差)。

**根因**:`scientific null`——六次独立测量,在不同工作流、不同扰动强度、不同模型
(Qwen2.5、部分尝试 Llama-3.1)下反复得到"KV 复用/修复引入的额外翻转不可与噪声区分"的一致
结论,统计设计(cluster bootstrap、配对差值、held-out 确证)本身站得住。

**它证伪了什么**:在本项目实际测过的这几种自然工况扰动强度下,"KV cache 复用+当前选择性
repair 机制会显著提高下游任务错误率"这一具体担忧,没有被观察到——**换句话说,没有证明需要
风险控制,不是证明了风险控制无用**。

**它没有证伪什么**:(a)没有测试极端发散工况(见 CLAUDE.md 阶段2→3 门槛已知的 extreme
repair 反向现象,不在这六次自然工况 null 范围内);(b)没有测试 receiver-conditioned validity
(全部六次都是单一固定 receiver);(c)没有测试字节不同但语义等价这一核心 B4 命题——这六次
测的是"D1(KL 散度代理量)是否预测 D3(下游翻转)",不是"typed contract 是否能安全截断
传播"。

**对下一项目的约束**:不要用"D1/KL 散度是否预测下游翻转"作为唯一 surrogate 假设的验证入口;
如果下一个 testbed 仍然只有一个固定 receiver,不可能触碰 receiver-conditioned validity
这个原始问题的核心。

**是否值得重复**:`YES_AS_CONTROL`——统计设计本身值得作为新项目的 baseline/noise-floor
校准参照,但不应在同一 setup 下重复期待不同结果。

**可挽救资产**:cluster-bootstrap + 配对差值 + held-out 确证性设计范式;E0/Task B/pos_shift
的数据生成 pipeline(`pipelines/task_a.py`、`pipelines/task_b.py`)。

**证据定位**:`runs/STATUS.md:573-667`(E0)、`:826-920`(identity 对照)、`:1320-1389`
(判别探针)、`:1729-1819`(Task B)、`:1821-1925`(pos_shift)、`:2661-2739`(S0)。

---

### NEG-05:sys.setprofile 与 CPython frozen module 伪路径冲突(Decision A 永久止损触发点)

**当时想证明什么**:用 `sys.setprofile` 建立一个"正向执行包络"(positive envelope),
只允许经批准的代码路径触发 native tool call,以此在不修改 AutoCodeRover 本身的前提下,
无侵入式捕获真实的 search/edit 调用序列。

**实际发生了什么**(`runs/route_a_plus_v6_decision_a/g0_v2/formal_fresh_v1/formal_execution_v1_failure/G0_V2_FRESH_FORMAL_EXECUTION_FAILURE_SUMMARY.v1.json`,
`EVIDENCE_LEVEL=RAW_REPRODUCIBLE`):CPython 3.12 把 `posixpath` 作为 frozen module 编译,
其 code object 的 `co_filename` 是伪路径字符串 `<frozen posixpath>`,既不匹配
`approved_code_bindings`(真实文件路径),也不匹配 `runtime_roots`(目录前缀),`Path.resolve
(strict=True)` 在这个伪路径上必然失败,导致 profile hook 在任何 native 调用发生前就
fail-closed。`science_reached` 字段原文:`"none: failure precedes SearchManager
construction; no native call, no boundary, no projection"`。

**根因**:`harness defect`——测量装置(execution envelope)与被测对象运行时环境
(CPython 3.12 的 frozen-module 机制)之间的一个基础设施级不兼容,与被测科学假设完全无关。

**它证伪了什么**:证伪了"`sys.setprofile` 正向白名单包络可以在不修改被测 agent 代码的
前提下无侵入捕获调用"这一具体工程方案在 CPython 3.12 + frozen module 组合下可行。

**它没有证伪什么**:与 edge-observable byte cutoff 假设完全无关——这次失败发生在任何模型
调用、任何 search 调用之前。`docs/route_a_plus_v7_testbed_and_minimal_g0_prereg_draft_2026-07-19.md:5-10`
原话:"三次失败全部是 harness 自伤...假设未被证伪,也未被支持。"

**对下一项目的约束**:不要用运行时 profile hook/monkey-patch 作为捕获层去无侵入观测一个
你不完全控制版本的第三方 agent 框架;如果确实需要拦截,优先选择 subprocess 级 stdout/stderr
捕获或框架自带的 hook 点(这正是 v7 后来采用的方案)。

**是否值得重复**:`NO`——这是一个已定位、已用不同技术路线绕过(v7 改用单层 driver + OS 级
输出捕获)的具体工程死角,同 setup 重复没有新信息。

**可挽救资产**:`G0_V2_FRESH_FORMAL_EXECUTION_FAILURE_SUMMARY.v1.json` 本身是一份写得很
干净的失败根因归因范例,可作为"如何诚实记录 harness 失败而不混淆为科学结论"的模板。

**证据定位**:commit `72f7c410dbe881bbde789c4414de9e481e988f35`;
`runs/route_a_plus_v6_decision_a/g0_v2/formal_fresh_v1/formal_execution_v1_failure/G0_V2_FRESH_FORMAL_EXECUTION_FAILURE_SUMMARY.v1.json`;
`docs/route_a_plus_v7_testbed_and_minimal_g0_prereg_draft_2026-07-19.md:8`。

---

### NEG-08 / NEG-11 / NEG-12:v7 Oracle/B3.5 测量装置的三重缺陷(合并深挖,同一批代码/同一批数据)

这三个案例根因不同(NEG-08 是标签/定义错位,N4;NEG-11 是 Oracle 本身无验证力,N4;
NEG-12 是伪正结果的具体来源,N2),但共享同一段代码(`analysis/route_a_plus_v7/g1_matrix_pair_align.py`)
和同一批数据,合并深挖以避免重复引用。

**当时想证明什么**:G1 pilot 要回答"byte-exact reuse(B3.5)与允许一定发散的 Oracle 截断
之间,是否存在有意义的 headroom gap(S_Oracle - S_B3.5 ≥ 5pp)",作为 v7 testbed 上是否
存在"bytes-different 但仍可安全复用"空间的代理证据。

**实际发生了什么**:
- `EVIDENCE_LEVEL=CODE_CONFIRMED`(本文档撰写时亲自读取并核对了以下代码,与官方文档引用
  的行号一致):`analysis/route_a_plus_v7/g1_matrix_pair_align.py:92`:
  `b35_cutoff = bool(node_differs and edge_same)`;`:93-94`:
  `oracle_cutoff = bool(node_differs and (diff_ratio <= 0.05 or diff_changed_lines <= 2))`。
  两个谓词都以 `node_differs` 为前提——**真正的 node-exact(字节完全相同)事件被结构性排除
  在 B3.5 和 Oracle 两个 arm 之外**,而"B3.5"这个名字原本冻结定义就是"byte-exact reuse"。
- 官方报告 `S_B3.5 恒为 0`(`docs/route_a_plus_v7_closure_report_2026-07-20.md:43-45`),
  独立复核用同一套代码单独重建的"真正 node-exact"事件(`B3.5-N`)则是
  no_change **5.3176pp**、dependent_source_change **0.6560pp**(`EVIDENCE_LEVEL=RAW_REPRODUCIBLE`,
  `analysis/route_a_plus_v7_independent_reaudit/results.json`)——**"S_B3.5 恒为 0"这句话
  本身是真的,但它测的是错误定义下的量,不能推广为"byte-exact 复用在真实场景零触发"。**
- Oracle 的 1.8599pp(matrix-v2)正信号,独立复核逐事件重建后:**8/8 事件**全部是
  `ls -la` 输出中 `..` 父目录行的 mtime 变化,与 mutation 内容零关系
  (`docs/route_a_plus_v7_posthoc_diagnostic_results_2026-07-20.md:46-55`)。同时 Oracle
  谓词本身(`diff_ratio<=0.05` 或 `diff_changed_lines<=2`)从未做过下游行为核验;补做后:
  next-step 行为级 false cutoff **6/8**(勘误自初稿的 5/8)、suffix trajectory 级 **8/8**、
  outcome/exit_status 级 **4/8**。
- 用同一套代码把比较颗粒度从"下一条命令"逐步收紧到"完整下一次 invocation",Oracle 的
  pp 数字单调塌缩:官方 1.8599 → 要求 next command 相同 0.2942 → 要求 next assistant
  相同 0.1488 → **要求完整 invocation 相同 0.0000**。

**根因**:NEG-08=`measurement artifact`(标签与实现语义错位,N4);NEG-11=`measurement
artifact`(代理指标无下游验证力,N4);NEG-12=`measurement artifact`(具体伪影来源,N2)。
三者共同指向同一个更深的问题:**比较单位从来不是"完整 consumer invocation",而是被逐步
放宽的文本片段(命令前缀、diff 相似度阈值)**。

**它证伪了什么**:证伪了"当前 pair_align.py 实现的 B3.5/Oracle 判据能够作为
S_Oracle-S_B3.5 headroom gap 的可信估计"——**这个具体测量管线不可信**,不是"headroom
不存在"。完整 invocation 级 B3.5-I 在 matrix-v2 上精确复算为 0.0000pp,这是一个更窄但更
可信的数字:在这 6 个 task、这次真实 agent 轨迹分岔模式下,**从未观察到一次完整下一次
invocation 逐字节相同的跨轨迹事件**——这本身是一条干净、可信的观察,不依赖任何 Oracle
heuristic。

**它没有证伪什么**:不能推广为"任何 testbed 上 byte-exact 复用都不可能触发"(v8 D2 的
unrelated stratum 就测到 4/4 task B3.5-I=100%,见 NEG-18 附注);不能证明"receiver-
conditioned typed contract"这一更高层假设为假,因为 Oracle 从来不是 typed contract 的
实现,只是一个未校准的文本相似度 heuristic。

**对下一项目的约束**:(1)比较对象必须是完整 invocation,不能是命令前缀或 diff 相似度;
(2)任何"截断/cutoff 是否安全"的判据,必须在预注册时锁定其精确谓词逻辑并让第三方复核该
逻辑与命名是否一致,不能事后靠文档描述断言;(3)不能用未经下游验证的自由文本 heuristic
(difflib 阈值)充当 oracle 或 contract。

**是否值得重复**:`NO`(同一套 pair_align.py 实现不应重复使用);但"完整 invocation 级
比较+多层次 false-cutoff 核验表"这一方法论值得原样搬到下一个 testbed。

**可挽救资产**:`g1_matrix_pair_align.py` 中 `node_differs`/`edge_same`/`diff_ratio` 的
计算逻辑本身(只是命名和阈值组合方式有问题,底层字段提取是对的);独立复核的 8 行逐事件表
方法论;`analysis/route_a_plus_v7_independent_reaudit/reanalyse_v7.py` 重算脚本。

**证据定位**:`analysis/route_a_plus_v7/g1_matrix_pair_align.py:82-121`(node_differs/
edge_same/b35_cutoff/oracle_cutoff 定义,已亲自读取确认);
`docs/route_a_plus_v7_independent_reaudit_2026-07-20.md`(六项质疑);
`docs/route_a_plus_v7_posthoc_diagnostic_results_2026-07-20.md:21-63`(数字表+8行逐事件表);
`analysis/route_a_plus_v7_independent_reaudit/results.json`。

---

### NEG-18:D3 结构性 headroom 决定性零结果(v8,含 K2 贡献恒为 0)

**当时想证明什么**:在完整 invocation 级、control gate 已验证高比例可复现(D2)的前提下,
用一个具体的 contract-incremental canonicalizer(K2:行多重集合规范化)去测:对于
dependent_read_hit stratum(下游命令真实读取了变异过的文件内容),K2 是否能把一部分
B3.5-I=false(完整字节不同)的 turn "拯救"为等价(即字节不同但 K2 规范化后相同,从而安全
截断传播),从而产生真实的、超越"exact match"本身的 headroom。

**实际发生了什么**(`runs/route_a_plus_v8/d3_structural/SUMMARY.json`,`V8_FINAL_VERDICT.json`,
本文档撰写时亲自用 `python3 -c "json.load(...)"` 复核以下字段,`EVIDENCE_LEVEL=RAW_REPRODUCIBLE`):
```
pooled_structural_headroom_pp: 0.0
positive_task_count_headroom_gt_0: 0        (阈值 >=3)
positive_stratum_count_headroom_gt_0: 0     (阈值 >=2,不含 no_change)
pooled_eligible_downstream_coverage: 0.11368158103077777   (阈值 >=10%,PASS)
K2 contract-incremental coverage: 0.0                        (FAIL)
```
`V8_FINAL_VERDICT.json` 对 K2 的原话:"K2 (line-multiset canonicalizer) never rescued
a single B3.5-I=false turn across all 8 measured (task, stratum) pairs;
eligible_downstream_coverage numerically identical to plain B3.5-I coverage in every row."
12 个 (task, stratum) cell 中,8 个 MEASURED,2 个因读取集为空判 INFEASIBLE,2 个因
mutation 目标文件字节数泄漏进目录列表判 INVALID_SAMPLE(具体机制见 NEG-19 附注)。

**根因**:`scientific null`——在已验证可信的测量装置(D2 control gate 74/76、72/76 R2L
分歧全部可归因于已知伪影)基础上,对一个具体的 contract 候选(K2)做了干净的负结果测量。
这是全部 25 个案例中证据链最完整、最不依赖 heuristic 的一个负结果。

**它证伪了什么**:严格窄语言——"在这 6 个 SWE-bench task、这一个 read-set mutation
设计、K2(行多重集合规范化)这一个具体 canonicalizer 下,contract-incremental headroom
精确为 0"。`docs/route_a_plus_v8_claims_matrix_2026-07-20.md` 原话(经研究agent引用):
"这是一个干净的负结果:在本数据集内,只要完整 invocation 前缀发生字面差异,其行多重集合
规范化形式也发生差异。"

**它没有证伪什么**:(1)不能推广为"任何 typed/executable contract 都不可能有非零 K2 类
增量收益"——K2 只是一种非常粗糙的结构规范化(行级多重集合),远不是原始 idea 设想的
"typed/executable contract"(例如真正基于语义等价谓词或程序切片的等价判定);(2)不能推广
到 SWE-agent(B4-C 候选 testbed)——K2 的测量全部发生在 mini-swe-agent/trace-conditioned
replay 上,SWE-agent 路径本身是 `FROZEN_NOT_ACTIVATED`,从未执行;(3)不能推广到
receiver-conditioned validity——D3 全程只有一个固定 receiver 视角(下游命令是否读取变异
内容),没有比较"同一变异对不同 receiver 是否有不同 verdict"。

**对下一项目的约束**:(1)不要把"行多重集合规范化"或类似浅层结构等价当作"typed/executable
contract"的代表性实现去检验整个假设;(2)任何新的 contract 候选,必须先在 read-set 非空、
样本可测的 cell 上验证其机制原理(K2 至少应该有一个"理论上应该生效"的合成样例做正对照,
D3 文档中未见此类合成正对照);(3)coverage 指标必须拆分报告"来自 exact match 的部分"
与"来自 contract 增量的部分",不能合并成一个数字(见 NEG-19)。

**是否值得重复**:`NO`(该 testbed/protocol 下,针对 K2 这一具体候选)。是否值得针对一个
更严肃的 contract 候选、在一个更好的 testbed 上重新测量,`UNRESOLVED`,留给负责人裁决。

**可挽救资产**:D3 read-set/mutation/k2/d3_measure 四个模块的整体测量框架(区分
MEASURED/INFEASIBLE/INVALID_SAMPLE 的严谨性本身值得保留);D2 control-gate replay driver
(identifiability 验证方法论);26 条 focused test。

**证据定位**:`runs/route_a_plus_v8/d3_structural/SUMMARY.json`(`pooled_gate_inputs`字段,
已亲自复核);`runs/route_a_plus_v8/V8_FINAL_VERDICT.json`(`gates.D3_structural_headroom_gate`,
已亲自复核);evidence commit `0369285`;`tests/route_a_plus_v8/test_d3_structural.py`。

---

### NEG-24:任务依赖未安装 → patch correctness 全程 UNKNOWN(跨 v7/v8 的持续限制)

**当时想证明什么**:不直接对应某一个具体假设,而是一个贯穿 v7 G1 pilot 与 v8 D2/D3 全程的
方法论边界条件——reviewer 裁决"任务依赖统一不装"以控制工程范围(`runs/route_a_plus_v7/PROGRESS.md:75`)。

**实际发生了什么**:v7 closure report(`docs/route_a_plus_v7_closure_report_2026-07-20.md:98`)
与 v8 closure(`docs/route_a_plus_v8_closure_2026-07-20.md:44`)都明确记录:由于 SWE-bench
任务依赖从未安装,**outcome verifier(实际跑 patch/test 判定)从未接入**,`patch
correctness` 与真实 `outcome` 在全部实验中永远是 `UNKNOWN`,不是"经检验为相同"。

**根因**:`incomplete dependency`——一个经过明确裁决、如实记录的工程范围限制,不是隐藏的
缺陷。

**它证伪了什么**:什么都没有直接证伪——这是一个测量盲区声明,不是一次实验结果。

**它没有证伪什么**:所有基于"exit_status 相同"或"suffix trajectory 相同"的等价性论证
(见 NEG-11)都不能被解读为"outcome 相同"——`docs/route_a_plus_v7_posthoc_diagnostic_results_2026-07-20.md:62`
原话:"exit_status 相同也不构成'结果等价'证据。"

**对下一项目的约束**:任何"效率收益"或"安全截断"的最终主张,必须有 outcome-level(真实
patch/test 判定)验证支撑,不能停留在 trajectory 或 exit_status 层面;如果预算不允许装
依赖跑测试,必须在论文/报告的每一处相关主张旁显式标注"outcome UNKNOWN,非经验证的相同"。

**是否值得重复**:不适用(这是范围声明,不是实验)。

**可挽救资产**:无直接可挽救的代码/数据资产,但这条方法论纪律(显式声明 outcome 未验证的
边界)本身值得作为新项目的报告规范搬运。

**证据定位**:`runs/route_a_plus_v7/PROGRESS.md:75`;`docs/route_a_plus_v7_closure_report_2026-07-20.md:98`;
`docs/route_a_plus_v8_closure_2026-07-20.md:44`;`docs/route_a_plus_v7_posthoc_diagnostic_results_2026-07-20.md:62`。

---

### NEG-25:TraceBuild 全上下文 prompt 设计使 static=runtime read-set(0/120 clusters),数字被导出进 novelty delta 论证

**当时想证明什么**:TraceBuild Phase 1 GPU discovery 想验证"runtime 观测到的依赖读取集合"
是否比"静态可达性(static transitive)分析出的依赖集合"更精确——如果 runtime read-set
显著更稀疏,就存在"只重算真正被读取的下游节点"这一 incremental-computation 式收益空间。

**实际发生了什么**(`runs/STATUS.md:2822-2864`,`EVIDENCE_LEVEL=RAW_REPRODUCIBLE`,已亲自
读取原文):真实 Qwen2.5-7B-Instruct 跑批,60 task × 2 mutation = 120 cluster:
```
static_transitive:              0.0000 (mean node saving)
runtime_read_set:                0.0000
readset_exact_early_cutoff:      0.0033   (= 0.33pp)
offline_oracle:                  0.1617   (= 16.17pp)
```
`runtime−static=0(120个cluster无一例外)`。手工复核锁定根因:`task_b.py` 既有的
prompt 设计(`shared_prefix_ids`)让每个 agent 节点的 prompt **永远**拼接完整的
system+code+test 内容,不论该 agent 语义上是否需要——这是"为 prompt 质量考虑的设计选择,
不是 bug",但直接导致 runtime 观测到的读取集合与 static 声明的读取集合逐字段完全相同,
没有可利用的依赖判别信号。原文明确:"**这不是否定 TraceBuild 假说本身,是这套具体workflow
测不出来**"。这一结果触发预注册停止条件 1(几乎所有节点读全部 prompt/repository)与
条件 4(runtime 优于 static 的比例为 0%,以最强形式成立),按预注册"任一停止条件成立即
停"判定 NO-GO。

**同一批数字随后出现在 novelty scoop-check 里**:`docs/scoop_check_2026-07-13/step1.md:5`
与 `step7.md:3` 把"0.33% vs 16.17%"作为支撑 novelty delta 论证的"实测"证据("recovering
oracle headroom that byte/identity-level invalidation provably misses(实测 0.33% vs
16.17%)"),用于论证本项目与 Durable Intermediate Artifacts / Execution Lineage 两篇
最接近的竞品之间存在有效差异化。**但这批数字的产出实验自己已经诊断出该 workflow 本身
无法区分 static 与 runtime 依赖**——16.17% 的 offline_oracle 上界,是在一个"static 和
runtime 读取集合逐字段相同"的 workflow 上算出来的理论上界,不代表任何真实可达的算法收益;
0.33% 是这个不具区分力的 workflow 上唯一非零的 cutoff 命中(仅 2/120 cluster,且只可能
出现在 source_change mutation 下)。

**根因**:主类别 `testbed mismatch`(N5,同 TraceBuild Phase 1 GPU discovery 本身的
判定)——`task_b.py` 的 prompt 结构不具备暴露"稀疏、节点特定依赖"这一现象所需的结构性
前提;次类别 `conceptual drift`(N9)/`prior-art conflict`(N10,间接)——一个自身已被
诊断为不具区分力的实验产出的数字,被导出用于一个面向未来、需要经得起同行审视的 novelty
差异化论证,而这层"该数字产出条件已被诊断为不具代表性"的警示没有跟着数字一起传递。

**它证伪了什么**:证伪了"`task_b.py` 现有 4-agent prompt 设计能够暴露 static vs runtime
依赖判别信号"这一具体工程前提。

**它没有证伪什么**:不能推广为"多智能体工作流普遍不存在稀疏、节点特定依赖"——原文明确
这是这一具体 prompt 设计选择的产物,换一个"prompt 本身就有稀疏依赖"的自然 workload 可能
得到完全不同的结果,这个换 workload 的尝试本身"不在本轮授权范围内"。

**对下一项目的约束**:(1)任何用于 novelty 差异化论证的实测数字,必须在引用处同时注明其
产出实验的判定结论(GO/NO-GO/testbed 局限),不能只截取数字本身;(2)在设计新 testbed 前,
先验证"该 agent workflow 的 prompt/上下文路由设计本身是否具备暴露目标现象所需的结构性
前提",不要在已知不具区分力的 workflow 上加大样本量;(3)"static vs runtime read-set
是否有差异"应作为新项目最早期(甚至先于任何 mutation 设计)的一次快速自检,如果两者恒等,
后续所有基于"稀疏依赖"的收益论证都无从谈起。

**是否值得重复**:`YES_AFTER_REDESIGN`——必须先换一个 prompt/上下文路由本身具有节点特定
稀疏依赖的自然 workload,而不是在 task_b.py 现有设计上加更多 task。

**可挽救资产**:`readset_exact_early_cutoff` 四级阶梯基线(static ≤ runtime_read_set ≤
readset_exact_early_cutoff ≤ offline_oracle)与两类语义 gate(pre-execution/
post-execution)分开定义的设计;discovery/confirmatory 数据切分纪律;
`pipelines/tracebuild_harness.py`(Planner→Coder→Test→Reviewer→Fixer,含独立
instrumentation Test 节点);`runs/tracebuild_discovery/EXPERIMENT_AUDIT.json`
(`verdict_status: audited`,含逐cluster手工复核记录)。

**证据定位**:`runs/STATUS.md:2784-2887`;`docs/scoop_check_2026-07-13/step1.md:5`、
`step6.md:8`、`step7.md:3`;`docs/tracebuild_phase1_discovery_prereg_2026-07-12.md`;
commit `9747ba6`(预注册)、`b127aea`(harness)、`8391fc6`(2-task smoke bug 修复)。

---

### v7:官方说法 — 后续独立复核 — 当前应采用的解释(并列表,不得只引用官方结论)

| 主题 | v7 官方说法 | 后续独立复核(`POST_HOC_DIAGNOSTIC`) | 当前应采用的解释 |
|---|---|---|---|
| B3.5 | "byte-exact 复用在真实 agentic 场景零触发,`S_B3.5` 恒为 0"(`route_a_plus_v7_closure_report_2026-07-20.md:43-45`) | 实现谓词 `node_differs and edge_same` 结构性排除了真正的 node-exact(byte-same)事件;重建的真 byte-exact 事件(B3.5-N)非零:no_change 5.32pp、dsc 0.66pp(`independent_reaudit_2026-07-20.md:34-49`) | "S_B3.5 恒为0"这句话在**官方错误定义下**是真的,不能推广为"byte-exact 复用一般性零触发"。完整 invocation 级(B3.5-I)才是正确对齐冻结定义的量,复算后仍为 0.0000pp——这是一条独立于标签问题的、更窄但可信的观察。 |
| Oracle | matrix-v2 字面 headroom 1.8599pp(< 5pp 阈值,判 FAIL) | 8/8 个 oracle-only cutoff 事件全部是 `..` 父目录 mtime 伪影,与 mutation 内容无关;Oracle 谓词本身是未校准 difflib 阈值,无下游验证,行为级 false cutoff 6/8(勘误自5/8)(`posthoc_diagnostic_results_2026-07-20.md:46-63`) | 1.8599pp 不是有效 headroom,是一个应被诊断并剔除的测量伪影。真实 headroom signal(逐层收紧比较颗粒度到完整 invocation 后)为 0.0000pp,与 B3.5-I 一致。 |
| PD-6 | 归类为"连续批处理(continuous batching)导致的非确定性"候选解释之一 | 复核只能确认"相同输入产生不同输出"这一现象本身(matrix-v2 报告与 posthoc 文档均未给出根因的最终排他性证明) | 根因(批处理浮点非结合性 vs 其他可能机制)**未唯一确认**,不应在报告中把 PD-6 的根因当作已证实结论引用,只能引用现象本身。 |
| G0 | "G0 判定 PASS with documented limitations"(`route_a_plus_v7_g0_verdict_2026-07-20.md`),核心证据"node≠/edge="(工具输出变化但投影不变) | probe projection(`_build_probe_projections`)在 agent loop 之外单独构造,sentinel 只捕获第一次调用(仅 system+user);G0 从未验证该投影真正进入一次完整下游 invocation(`independent_reaudit_2026-07-20.md:26-32`) | G0 只证明了"隔离投影可以与真实工具输出解耦地保持不变"(命题 A),**没有证明**"这个投影安全地代表了一次完整下游 invocation 可以被跳过"(命题 B,即 B3.5-I)。引用 G0 结果时必须明确限定为命题 A。 |

---

## 6. Cross-Cutting Failure Patterns

1. **迁移了理论,没有迁移实验假设。** 从 KV 张量层面(阶段1)迁移到 agent tool-call 层面
   (阶段2起)时,"receiver-conditioned validity"这一原始核心命题没有被显式迁移——三代
   testbed 全部只设计了单一固定 receiver 的比较,从未构造"同一 producer 产物、两个不同
   receiver、验证结论不同"的对照实验。这是全部 25 个案例背后最大的共性缺口(见 §8)。
2. **testbed 不暴露原始结构。** AutoCodeRover 的多层 harness(NEG-02)、mini-swe-agent
   的单一 history_processors 管线(NEG-09)、`task_b.py` 的全上下文 prompt 设计
   (NEG-25),三代 testbed 依次因为不同的具体原因,都不具备"同一产物有多个真实、独立
   consumer"这一原始问题所需的最基本结构前提。
3. **自由文本 consumer interface 无法支持 typed validity。** NEG-07(AutoCodeRover
   SearchResult)、v8 的工具返回值被明确记录为"裸 str"(见
   `docs/route_a_plus_v8_swe_agent_static_qualification_2026-07-20.md` 对 claim 降级
   的建议)——三代 testbed 里,LLM consumer 实际消费的对象从来都是渲染后的自由文本,
   不是任何强类型对象,这从工程根子上排除了"typed/executable contract"的直接实现路径,
   只能退而求其次做文本层面的近似(K2 canonicalizer、difflib Oracle),而这些近似本身
   又是 NEG-08/NEG-11/NEG-18 的直接根源。
4. **真实 Agent 轨迹随机性破坏因果比较。** NEG-13(未排序 find)、NEG-14(vLLM 批处理
   非结合性 + checkout 路径 mtime 噪声)共同说明:即使在"理论上应该完全确定"的 greedy/
   temperature=0 设置下,真实 serving 栈与真实文件系统操作仍然引入了肉眼不可见但测量
   敏感的非确定性。**"cascade identity"这一隐含理论前提**(即"一旦某个 node 的投影
   相同,下游经确定性传播也应相同")在 PD-3(环境准备噪声从 turn 1 起就已经污染)和
   PD-6(同一 prompt 在批处理推理下输出本身分叉)两条独立路径下都被打破——这意味着
   任何依赖"上游相同→下游必然相同"这一假设链条的测量装置,都需要先独立验证这个假设
   在目标 serving/文件系统栈上成立,不能默认。
5. **审计复杂度超过科学复杂度。** NEG-02(四层 harness)、v8 收尾文档明确写下的第一条
   红线"审计机制不得比被审计的科学复杂"(`docs/route_a_plus_v7_testbed_and_minimal_g0_prereg_draft_2026-07-19.md:10`),
   以及测试/回归数量的持续膨胀(M1 38+37 测试 → M2 19 hand-check → M3 阶段 225 CPU
   测试 → Decision A 最终候选 201 dedicated + 528 regression,见 NEG-02 引用数据)——
   这条红线是负责人在 Decision A 永久止损后才明确写下的,说明这个模式在被制度化纠正
   之前已经真实发生过。
6. **代理指标替代真实 outcome。** NEG-16(W_a 单步 token 代理)、NEG-24(outcome 全程
   UNKNOWN)——efficiency/savings 的度量始终建立在 token 计数或 trajectory 文本层面,
   从未接入真实的 patch/test 判定,这使得任何"节省了 X% 计算"的主张都缺少"节省的计算
   是否仍然产出正确结果"这一半的证据。
7. **post-hoc candidate search 的选择偏差风险。** NEG-20(K3/K4)——这两个候选是在观察
   到 K2 失败之后,从同一批 D3 数据里"事后"提出的新假设,项目自身已经正确地把它们隔离
   到"future hypothesis registry"、明令"不得在当前论文/报告中作为已验证发现引用"——
   这是一个正确处理的风险,但新项目仍需知道这批候选的出身,不能把它们当作独立于 D3
   数据集之外的新证据。
8. **exact baseline 被误称为核心创新的风险持续存在。** NEG-19(11.37% coverage 全部
   来自 exact match)、NEG-22(B4 承诺退化为 exact-byte match)——目前项目文档已经能够
   正确区分"exact-invocation coverage"与"contract-incremental coverage"两个数字
   (`V8_FINAL_VERDICT.json` 把它们拆成 criteria 2 和 2b 两条),这是一个好的实践,
   但历史上(v7 closure report 的"S_B3.5 恒为0"表述)曾经因为标签错位而模糊过这条
   边界,新项目应该从一开始就把"exact match 贡献"与"contract 增量贡献"设计成两个
   永远分开报告的字段,不给合并的机会。

---

## 7. What Has Actually Been Falsified(窄命题,已被当前证据否定)

1. `readset_exact_early_cutoff` 相对 `runtime_read_set` 在 `task_b.py` 现有全上下文
   prompt 设计下,除 2/120 cluster 外没有可利用的依赖判别信号(NEG-25,`RAW_REPRODUCIBLE`)。
2. AutoCodeRover 场景下,四层 transport/supervisor/outer/inner harness + `sys.setprofile`
   正向白名单包络这一具体工程方案,在 CPython 3.12 环境下不可行(NEG-02/NEG-05,
   `RAW_REPRODUCIBLE`)。
3. `g1_matrix_pair_align.py` 当前实现的 B3.5/Oracle 判据(基于 `node_differs`+
   `edge_same`/`diff_ratio` 阈值的文本层面判据),不能作为 S_Oracle-S_B3.5 headroom
   gap 的可信估计(NEG-08/NEG-11,`CODE_CONFIRMED`)。
4. 在 mini-swe-agent v7 的 6-task pilot matrix 上,从未观察到一次完整 next-invocation
   逐字节相同的跨轨迹(old vs new)事件(B3.5-I 精确复算为 0.0000pp,NEG-08 附表,
   `RAW_REPRODUCIBLE`)。
5. K2(行多重集合规范化)在 v8 D3 的 8 个可测 (task, stratum) cell 上,没有一次把任何
   B3.5-I=false 的 turn 拯救为等价(contract-incremental coverage 精确为 0,NEG-18,
   `RAW_REPRODUCIBLE`)。
6. 在本项目实际测过的自然工况扰动强度、单一固定 receiver 视角下,KV cache 复用+当前
   选择性 repair 机制引入的额外任务翻转率,与恒等对照/噪声地板不可区分(NEG-01,
   `RAW_REPRODUCIBLE`)。

**以上 6 条都是关于具体实现/具体 testbed/具体候选机制的窄命题,没有一条是"receiver-
conditioned typed contract 复用假设本身为假"这一原始问题的直接证伪。**

---

## 8. What Remains Untested(原始 idea 中完全未被真实实验触碰的部分)

1. **Real multi-consumer receiver-conditioned validity**——三代 testbed 全部只有一个
   固定 receiver;从未构造过"同一 producer 产物,两个真实、独立的 consumer,验证结论
   不同"这一原始问题的核心对照。v8 D4 曾经短暂靠近这个结构(RetryAgentConfig 的
   Reviewer/Chooser 是一个真实的第二 LLM consumer),但该路径 `FROZEN_NOT_ACTIVATED`,
   从未实际测量。
2. **Bytes-different / contract-equal / outcome-same 的非人为构造案例**——目前唯一
   接近的是 K2(行多重集合规范化),它是一个人为设计的浅层结构规范化,不是从真实
   consumer 语义推导出的 typed contract;也没有任何合成正对照案例证明 K2 在"应该生效"
   的场景下确实生效过。
3. **Repairable 复用档位**——三档设想(Exact/Repairable/Invalid)中,只有 Exact
   (byte-identical/B3.5)与 Invalid(完全不复用/full recompute)被间接测量过,
   "Repairable"(部分修复后可用)这一中间档位在 Route A+ v6-v8 全程从未被独立定义或
   测量(注:阶段1 早期 KV 张量层面的 `repair_cacheblend` 选择性修复,概念上接近
   Repairable,但那是 KV 张量层面的机制,未随后续 agent tool-call 层面的迁移一起
   延续)。
4. **Latent/KV state 直接传递**——阶段1 之后,项目完全转向 agent tool-call/文本层面
   的复用,原始"computation state 随消息一起传递"里"state 可以是 latent 张量而非
   仅文本"这一设想没有在 Route A+ 任何阶段被重新触碰。
5. **Heterogeneous receiver**(不同类型/不同能力的 consumer 对同一产物的不同处理)——
   未测试。
6. **实际下游计算跳过(actual downstream compute skip)**——所有测量都是"事后判定
   是否可以安全截断"(post-hoc equivalence judgment),没有一次真正在 live 执行中
   跳过下游计算并验证跳过后的最终结果与不跳过一致。
7. **Fresh-task outcome validation**——patch correctness/outcome 全程 UNKNOWN
   (NEG-24),即使某个 contract 候选未来测出非零 coverage,仍然需要独立一轮
   outcome-level 验证才能支持"安全复用"这一最终主张。

---

## 9. Salvageable Assets

### 代码
- `analysis/route_a_plus_v7/g1_matrix_pair_align.py` 的 node/edge 字段提取逻辑
  (`node_differs`/`edge_same`/`diff_ratio` 计算本身没有问题,问题在于谓词组合方式
  和命名,见 NEG-08)。
- `tracebuild/route_a_plus_v8/d3_measure.py` 的 MEASURED/INFEASIBLE/INVALID_SAMPLE
  三态分类与 `classify_mutation_size_echo` 检测逻辑——一套严谨的"样本是否可用"判定
  方法论,值得原样搬到新 testbed。
- D2 control-replay driver(trace-conditioned replay + identifiability gate 设计,
  74/76、97.37% 高比例可复现,是三代 testbed 中唯一被验证"测量装置本身可信"的一次)。
- `pipelines/tracebuild_harness.py`(Planner→Coder→Test→Reviewer→Fixer 五节点设计,
  含独立 instrumentation Test 节点,不干扰主链路)。

### 数据
- E0/Task B/pos_shift/S0 六次 null 的完整 pairs JSONL 与 EXPERIMENT_AUDIT.json
  (`runs/pairs/`,按 trace_id 划分,可作为新项目的噪声地板参照基准)。
- `runs/tracebuild_discovery/`(120 cluster 的 workflow_events,含手工复核记录)。
- `runs/route_a_plus_v8/d3_structural/SUMMARY.json` + 6 task × 2 stratum 的原始
  measurement JSON(负结果本身是干净、可信、可作为未来对照基线的数据)。

### Harness / Replay
- v7 单层 driver 设计范式(相对 AutoCodeRover 四层架构的教训性简化)。
- v8 D2 trace-conditioned replay(结构阶段零模型调用,复用冻结 trajectory 作基线)——
  这是目前唯一被证明"可以先低成本验证测量装置本身可信,再决定是否投入模型调用"的方法论。

### Tests
- `tests/route_a_plus_v7/`(26+ 项)、`tests/route_a_plus_v8/`(测 d3_structural/
  gate_v81/replay_core,共 40+ passed)——focused test 覆盖了大量已知伪影
  (`..` mtime、unsorted find、workdir 路径伪影)的回归防护,直接复用可避免重新踩坑。

### Governance
- `.claude/agents/executor.md` 的授权协议(coordinator 转达即有效,凭证纪律)。
- `EXPERIMENT_AUDIT.json` schema(`protocol_deviations` 字段强制填写的纪律)。
- "审计机制不得比被审计的科学复杂"这条负责人事后写下的红线。

### Literature
- `docs/scoop_check_2026-07-13/`(7 步查新流程 + 10 篇近邻文献的四轴比较表),novelty
  delta 论证的方法论框架可复用,但引用的具体数字(0.33%/16.17%)需要重新生成(NEG-25)。

### Writing Material
- `manuscript/paper_spine_2026-07-08.md`、`related_work.md`、
  `methodology_identity_control.md` 等(对应最初方向,已在 docs/INDEX.md 标记为历史,
  是否复用取决于 PUBLICATION_DECISION)。
- `docs/route_a_plus_paper_viability_memo_2026-07-20.md` 的三出口分析框架
  (main-track/workshop/technical-report 的差距诊断方法本身可复用于任何新项目的中期
  自我评估)。

---

## 10. Non-Negotiable Design Rules for a New Project

**仅提炼规则,不提出具体实验。**

1. 结构阶段必须先验证"testbed 的 prompt/上下文路由设计是否具备暴露目标现象所需的结构性
   前提"(如 static vs runtime read-set 是否恒等),这必须是新项目最早期、最低成本的
   一次自检,先于任何 mutation 设计或模型调用(源自 NEG-25)。
2. 必须存在真实的、独立的多个 consumer(receiver),对同一 producer 产物做比较;单一
   固定 receiver 的实验设计不能触碰原始问题的核心(源自 §8 第1条)。
3. 比较对象必须是完整 consumer invocation,不能是命令前缀、diff 相似度阈值或其他文本
   片段代理(源自 NEG-08/NEG-11/NEG-15)。
4. consumer projection(比如 probe/sentinel 捕获的观察对象)必须在真正进入下一次完整
   模型调用之后再被判定为"验证通过",不能只验证隔离的 projection 与真实调用之间的
   byte-equality(源自 NEG-10)。
5. 任何 typed/executable contract 候选,必须先给出至少一个合成正对照案例证明其"应该
   生效"时确实生效,再拿到真实数据集上测量(源自 NEG-18)。
6. Coverage/headroom 类指标必须始终拆分报告"来自 exact match 的贡献"与"来自 contract
   增量的贡献"两个独立字段,禁止合并成一个数字(源自 NEG-19/NEG-22)。
7. 任何"上游相同→下游必然相同"的因果链条假设("cascade identity"),必须先在目标
   serving 栈+文件系统栈上独立验证成立,不能默认(源自 NEG-14)。
8. 任何风险上界/统计推断,必须按 task/repository cluster 计算,不能把同一 task 的多个
   edge/mutation 当作独立 Bernoulli 样本;confirmatory 阶段的独立性假设必须在预注册
   时明确验证并留痕(源自 NEG-23,已核查未违规,但作为纪律仍需显式声明)。
9. outcome-level(真实 patch/test 判定)验证是任何"安全复用"最终主张的必要条件,
   trajectory 或 exit_status 层面的相同不能替代 outcome 验证(源自 NEG-24)。
10. 审计/harness 机制的复杂度不得超过被审计的科学问题本身的复杂度;层数(transport/
    supervisor/outer/inner 式架构)每增加一层,必须有明确的、独立于"更严谨"这一
    直觉的具体收益论证(源自 NEG-02)。
11. 用于 novelty 差异化论证的实测数字,引用时必须同时注明其产出实验的判定结论
    (GO/NO-GO/testbed 局限),不能脱离产出条件单独引用(源自 NEG-25)。
12. Post-hoc 从失败数据集中提出的新候选假设(如 K3/K4),必须显式隔离标注、禁止在
    未经独立预注册确证前作为已验证发现引用(源自 NEG-20)。

---

## 11. Evidence Gaps and Contradictions

1. **"六次 null"的确切构成矛盾**:至少 7 份文档反复使用"六次独立 null/尝试"这一表述
   (`manuscript/paper_spine_2026-07-08.md`、`related_work.md`、
   `docs/progress_and_novelty_gap_2026-07-07.md`、`docs/second_leg_brief_2026-07-07.md`、
   `docs/paper_checklist_2026-07-07.md`、`reviews/idea_review_2026-07-08.md` 等),
   但没有任何一份文档在同一处逐项点名六个具体实验。`paper_checklist_2026-07-07.md:199-201`
   给出的最接近的解释是"五次自然/恒等/扰动尝试 + pos_shift 作为第六次",本文档的 NEG-01
   按此口径采用六项列表(E0、identity 配对、判别探针、Task B、pos_shift、S0),但如实
   记录这一构成本身在原始文档间不完全一致,不强行统一为唯一权威版本。
2. **"generic Bash read-set 完整追踪的一周工程不可行性"(任务书第30项)未找到独立证据**——
   仅能找到旁证(v8 D3 的 read-set 检测是基于命令模式的启发式,而非通用数据流追踪器,
   见 `d3_measure.py:66-81` 的 `classify_mutation_size_echo`),但没有找到任何文档记录
   过"曾经尝试构建通用 Bash 数据流追踪器、耗时一周后放弃"这一具体历史事件。标记
   `UNKNOWN`,不编造。
3. **"60 个相关 microcases 被误当独立风险样本"(第22项)与"bootstrap 被过度解释"
   (第26项)经核查未发现违反证据**——TraceBuild Phase 0 的 N=60/4.87% Clopper-Pearson
   计算,其原始文档(`docs/tracebuild_route_a_plus_prereg_2026-07-13.md:7`)明确讨论了
   独立性要求("N≥60...matching the Phase 0 validator-feasibility precedent"),且同一
   文档在 N=30 discovery 阶段的场景下明确警告"必须never报告为≤5%风险上界"——显示项目
   本身对独立性假设有明确意识。早期六次 null 分析中的 cluster bootstrap CI(NEG-01)
   均正确报告为"含0/不显著",未见夸大解读为"证明安全"。**这两项经核查列为
   `NEG-23:经核查未确认存在该失败`,不强行归为负面案例——但因为 TraceBuild 从未推进到
   真正的 N≥60 confirmatory 阶段就已 NO-GO(NEG-25 阻断了该路径),"60 个 clusters
   是否真的相互独立"这一问题本身也从未在有真实数据的场景下被最终检验过,严格说是
   `UNRESOLVED` 而非"证明合规"。**
4. **v8 D4 的 SWE-agent 源码证据链止步于文档转录**——`sweagent/agent/agents.py:539-551`
   与 `reviewer.py:455-496` 的代码引用,本仓库内不存在对应的 vendored 代码(未找到
   `sweagent/` 目录),这些引用的证据等级只能是 `DOCUMENTED`(转录自
   `docs/route_a_plus_v8_swe_agent_static_qualification_2026-07-20.md`),不是
   `CODE_CONFIRMED`。如果下一个 agent 需要复核这部分,必须先定位原始 SWE-agent 仓库
   (pinned commit,若有记录)。
5. **最初 KV/LatentMAS 火花缺少仓库内一手记录**——`EVIDENCE_LEVEL=UNRESOLVED`,§3
   阶段0 已说明,仓库最早提交已经是具体化后的 KV-reuse 实现,原始最抽象层面的构想
   过程本身没有独立文档。
6. **本文档的四路并行证据搜集由子 agent 完成,已对最高风险的数字做过独立复算校验**
   (`pair_align.py:92-94` 的谓词逻辑、`d3_structural/SUMMARY.json` 的
   `pooled_gate_inputs`、`V8_FINAL_VERDICT.json` 的 K2 字段,均由本文档撰写者亲自
   用 `Read`/`python3 -m json.tool` 重新核对,与子 agent 报告完全一致),但未对全部
   25 个案例逐条独立复算,部分 `DOCUMENTED` 级别的引用(尤其 M0-M3 era 的部分)仍
   依赖子 agent 的转录,如需更高置信度应逐条重新独立核对。
