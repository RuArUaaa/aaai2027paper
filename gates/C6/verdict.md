# C6 Gate Verdict

**C6_GATE = FAIL_TESTBED_OR_MECHANISM(query-relative 失效判定在本 testbed 不仅不可测,而且被证明不安全)**

日期:2026-07-21 · 主协调代理(主席终裁,非 DRAFT)

## 关键数字(100 真实 4-agent RAG traces,992 个 doc artifact,CPU-only 可复现)

**子代理脚本有一个未初始化变量 bug,主席已修复(`analyse_workflow.py` line ~297)并复核全部输出;句子级测量退化后,主席补写引用通道分析(`analyse_doc_level.py`)。**

### 句子级(verbatim 使用区域,子代理)
- used-region 中位数 = 0,98.1% 的 (artifact, consumer) 对零使用(agent 意译,不照抄)——**测量退化**;
- mutation 4297 例:exact 失效 17188,query-relative 失效 47,dead region 99%。

### 文档级(引用通道,workflow 自带的 addressing rule,主席)
- 引用率 8.7%(reader 平均每 trace 引 1.33 篇,verifier 0.95,writer 0.32);
- 84.8% 的 doc 无人引用;8.9% 被 ≥2 consumer 引用;
- mutation 992 例:exact 失效 2976(每 mutation 牵连全部 3 个下游),query-relative 失效 260 → **账面减少 91.3%(cost-weighted 89.4%)**。

### 探索性验证(对 E0 真实扰动的下游 flip,1000 pairs)
- 被引用 (n=53):real flip 率 **0.0%**;
- 未被引用 (n=947):real flip 率 **5.07%**。

## 判定

预登记判据:
- (a) repeated-consumer coverage ≥30%:incidence 级 92.8% 通过,但那是"每个 agent 收全部 10 篇 doc"的全上下文路由,与 NEG-25 的 task_b.py 同一失效模式;**usage 级(引用 ≥2 方)只有 8.9%,FAIL**;
- (b) query-relative cost 减少 ≥20%:账面通过(89.4%),但建立在未通过验证的 usage 信号上,不予采信;
- (c) oracle 可用率 100%:PASS;
- (d) used-region 测量非退化:**FAIL**——句子级退化;文档级非退化但**探索性验证失败**:引用不预测真实敏感度,方向上甚至相反(虽未达统计显著,n=53)。

→ overall = FAIL_TESTBED_OR_MECHANISM。focused tests:5/5 通过(`test_gate.py`)。

## 这个 FAIL 教给我们什么(主席解读)

1. **隐含使用主导显式引用**:未被引用的 doc 依然造成 5% 的下游 flip——consumer 读了全部 10 篇并受到未具名影响。在此结构下,**query-relative 失效判定(只让引用方重算)会产生真实错误**;exact replay 的"全部失效"反而是正确的。这不是"测不出来",是"该机制在此 testbed 不安全"的直接证据。
2. **与 NEG-25 形成跨 testbed 模式**:TraceBuild task_b.py(全上下文 prompt)与 E0 4-agent RAG(全 doc 路由)两个独立 testbed 家族,都以"每个 consumer 接收全部上下文"的方式消灭了选择性消费。**C6 的结构前提(天然选择性消费)在两个真实 agent workflow 中均不存在**——这从单点失败升级为模式级证据。
3. **文本级 usage 代理第三次失败**(difflib Oracle、句子 verbatim、引用通道):usage/等价性的文本代理与真实下游敏感度持续脱钩,与 NEG-11/NEG-16 一致。
4. **抢救条件(精确定位)**:C6 若要存在,需要一个 consumer 原生只接触其所需 artifact 子集的 workflow(选择性路由是设计属性而非事后窄化),例如按模块分工的代码分析 agent、ToolSandbox 式按需工具读取。找到之前,C6 不得重启;找到之后,usage 信号可由路由本身提供(不再需要文本代理)。

## 与 CP2 的联动

CP2 判 C6 = CLEAR_GAP(novelty 层面空位真实存在)。本 gate 证明其**结构前提在当前可得 testbed 上不成立**。按 CP4 规则,C6 不得成为主候选;作为 BACKUP 保留,重启条件见 `docs/researchstudio_collision_decision_memo.md`。
