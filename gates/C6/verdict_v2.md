# C6 Gate Verdict v2(更正版,取代 v1 结论)

日期:2026-07-21 · 主协调代理
v1(`gates/C6/verdict.md`)把结论写成"query-relative 失效判定不安全 / 结构前提普遍不存在",
评审认定该因果解释超出证据。本文件取代 v1 结论;v1 文件与全部原始数据保留原样。

## 更正后的判定

```
C6_GATE_V1 = FAIL_MEASUREMENT
TEXT_USAGE_PROXY = INVALID
NATURAL_SELECTIVE_CONSUMPTION = UNRESOLVED
```

**撤回**:
- ~~"query-relative invalidation 不安全"~~;
- ~~"结构前提在两个 testbed 家族普遍不存在(模式级证据)"~~;
- ~~把 5.07% flip 解释为"未引用 doc 导致的额外翻转"~~。

## 为什么 5.07% 不能作为机制证据(接受评审三点)

1. **未与噪声地板配对比较**:同一批数据的 identity-control flip 率约 5–7%
   (C3 协议记录:Task A 5.1%/4.7%,Task B 6.1%/7.3%)。5.07% 与之同量级;
   v1 未计算 real-vs-identity 的配对差值或置信区间,不能声称存在额外翻转。
2. **"未引用" ≠ "未使用"**:全上下文路由下,未写出标题不等于模型未使用;
   引用通道系统性低估使用,账面 89.4% 失效减少与"5.07% 反向证据"都建立在
   同一个失效的文本代理上,两个方向都不可采信。
3. **测试断言锁死描述性方向**:v1 focused test 只保证重跑得到同一描述,
   不证明显著性、不证明 citation 是有效 usage oracle、不证明机制不安全。

## v1 仍然成立的发现(限测量层)

- 句子级 verbatim 使用区域测量**退化**(中位数 0,98% 零使用):FAIL_MEASUREMENT 成立;
- 引用通道作为 usage 代理**未通过探索性验证**(cited 0/53 vs not-cited 5.07%,不显著,
  且即使显著也无法区分因果方向):TEXT_USAGE_PROXY = INVALID 成立;
- 文本类 usage/等价代理在旧项目(difflib)+ 本轮(verbatim、citation)共三次失效——
  作为**测量方法**的负知识成立;作为**机制**的否定不成立。

## 对后续 testbed 的约束(替代旧结论)

任何 C6 后续 gate 的 usage/dependency 信号必须来自:

- workflow 原生路由(consumer 实际收到的输入集合);
- artifact access log / tool call / read trace;
- framework 显式声明的 consumer input;

**不得**来自:最终文本 substring、Jaccard、引用提及、LLM 输出中是否出现标题。
若候选 testbed 只能提供文本代理 → testbed 资格直接 FAIL_MEASUREMENT,
且其 flip 数据不得被解释为机制证据。

## 与 CP4 的联动(详见 decision_v2)

C6_NOVELTY 降为 **NARROW_GAP / CONDITIONAL_CLEAR_GAP**
(见 `scoop_checks/C6_novelty_revision.md`);
gate 状态为 FAIL_MEASUREMENT(机制 UNRESOLVED)。
"自然选择性消费是否存在"重新成为开放的实证问题——评审批准后,
选项 A(公开 agent 框架 trace 审计,usage 信号须满足本节约束)才是合法下一步。
