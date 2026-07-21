# C4 Gate Protocol — Repairable reuse / selective recomputation

状态：**REQUIRES_AUTHORIZATION**(需要本地模型 + KV 操作(GPU),本轮不执行)
日期：2026-07-21 · 主协调代理(科学主席)亲自撰写

## 1. 最小操作语义(主席定义)

- **被修复的计算对象**:单一 receiver 的上下文 KV cache;上游 artifact 的一个字段/区段发生内容 mutation 后,其中已失效的部分。
- **affected region**:内容变化区域之外、因"prefill 时已把 field-conditioned 结论写入下游 token(note tokens)"而失效的下游 KV 子集(C4-P6 的因果发现:受影响区域 ≠ 内容变化区域)。
- **affected region 识别**:三档候选——(i) 位置界:mutation 点之后的全部 suffix(上界,必正确);(ii) 因果探针:locality patching / knockout 定位 note tokens(P6 方法);(iii) KV-deviation 选择器(CacheBlend 式,P6 已证其在此场景追错对象——作为机制鉴别 arm)。
- **repair operation**:只重算受影响 region 的 KV,保留其余。
- **full recomputation baseline**:整个上下文 prefill 重算。
- **correctness/outcome oracle**:双级——(a) decision-identical:下游决策与 from-scratch 完全一致(P6 标准);(b) task outcome:任务级判定(测试/EM)。
- **repair overhead**:重算 token 比例、延迟 vs full recompute。
- **repair 后保留的计算**:未受影响 region 的全部 KV(问题 + 未受影响下游段)。

## 2. 控制组设计(预登记)

### Positive control(按机制理论应可修复)
- 场景:结构化记录 QA(form-filling 变体):上下文 = 一条多字段记录 + 一个依赖某字段的决策问题。
- mutation:改变该字段的值(不动其他字节)。
- 理论预测(P6 机制):受影响区域 = 下游 note tokens;(i) suffix 重算必恢复 decision-identical;(ii) erratum/选择性修复在 CoT 在场时恢复。
- 通过判据:suffix-repair arm 在全部正控实例上 decision-identical;选择性 arm 报告恢复率(不预设通过线——它是测量对象)。
- 纪律:正控实例在机制理论写出后、任何实验前构造;不得从事后数据中挑选(NEG-18 纪律)。

### Negative control(理论上应失败/回退全量)
- NC1:intent mutation——改变问题本身(非字段值):note-token 结构无定义,任何选择性 repair 应不可恢复 → 正确行为是回退 full recompute。
- NC2:CacheBlend-selector arm:按 KV-deviation 选择器修复 field mutation,按 P6 证据预期失败(追 changed keys 而非 note tokens)。若它成功,则 P6 的因果论断在吾辈设置下不成立——这本身是可发表的分歧证据。
- 通过判据:gate 承认 NC 判定的标准是"选择性 repair 在 NC1 上恢复率显著低于正控"且"系统能识别并回退";NC2 仅作机制鉴别,不设通过线。

### 真实 mutation 可行性审查(静态,本轮完成)
- 候选来源 1:τ²-bench 状态转移(P6 已用,但其无公开代码,需自行复现——独立实现反而加强证据)。
- 候选来源 2:ToolSandbox world-state 变更(C3-P1,NAACL'25,有公开代码)。
- 候选来源 3:旧仓库 Task A 扰动 trace(自然扰动,已冻结)。
- 结论:真实 mutation 语料可获得,不构成阻塞;阻塞项仅为模型/GPU 授权。

## 3. 静态可行性检查(本轮完成,见 results.json)

- P6(arXiv:2606.17107)无公开代码 → 机制需独立复现:工作量 = KV 操作层(修改 vLLM/HF 的 prefill 掩码)+ 因果探针脚本,估计 3–5 天工程;无不可行项。
- 模型需求:一台 80GB 级 GPU + 一个开源 8B 级模型(需 CoT 开关能力)。
- 与旧项目关系:不复用 Route A+ harness;KV 层实验与阶段1 kvlib 概念相近但协议全新(受影响区域识别 + 三档修复 + 双 oracle)。

## 4. 预登记判定标准

- GATE_PASS(可进一周实验):正控 suffix-repair 100% decision-identical;选择性 arm 恢复率 > field-only 且 < suffix(即三档真的分出层次);NC1 回退正确触发。
- GATE_FAIL_MECHANISM:正控 suffix-repair 都无法恢复 decision-identical → repair 概念本身在吾辈设置下不成立。
- GATE_FAIL_NO_HEADROOM:选择性 arm 恢复率 = suffix(无成本差异)或 = 0(无修复能力)。
- 当前状态:**REQUIRES_AUTHORIZATION**——上述任何一项都需 GPU + 模型,未获授权,不执行。
