# FABLE5 Abstract Submission Recommendation — 今日摘要裁决

> **Disposition (2026-07-22): PARTIALLY_ACCEPTED.** This is an independent
> review input. Section 3 is superseded by
> `docs/AAAI27_ABSTRACT_SUBMISSION.md`; do not paste the experimental-claim
> version below into OpenReview. See `docs/FABLE5_OWNER_DECISION_A.md`.

日期:2026-07-22(摘要截止日)
审查者:Claude Fable 5(独立首席研究审查者)

## 0. 官方约束(一手核实)

- AAAI-27:摘要截止 **2026-07-21 23:59 AoE** = **北京时间今天 19:59**;
  全文截止 2026-07-28 AoE(北京时间 7-29 19:59)。
- 摘要阶段必须提交:完整标题 + 完整摘要。
- **Program Chairs 保留对"摘要与终稿间实质性改动"直接拒稿的权利**——
  今天写下的每一个承诺都必须在一周后兑现或可无损降级。
- 正文上限约 7 页 + 2 页参考文献(共 9 页)。

来源:aaai.org AAAI-27 主页与 Submission Instructions(2026-07-22 抓取)。

## 1. 现状核查

**仓库中不存在任何标题、摘要、TL;DR、topics 或论文骨架。** 全仓库搜索
`manuscript/ paper/ abstract title tldr submission prereg` 仅命中研究过程
文档。因此本审查回答的不是"现有摘要是否合格",而是"今天应提交什么"。

对 §八 各问的回答:

1. **当前摘要完整/真实/不过度承诺?** 不适用——不存在。
2. **是否锁死在可能无法完成的实验上?** 风险在于新写的摘要;下方草案
   把 live 实验写为"controlled empirical evaluation…we report the
   realized savings, overheads, and agreement",正/零/负结果均可兑现;
   唯一无法兑现的情形是实验完全没跑成,此时删去该句、保留前三个贡献,
   属于收缩而非换题(见 §5 允许修改范围)。
3. **是否过度偏向纯 measurement paper?** 草案主身份就是 measurement +
   methodology——这是证据能支撑的唯一诚实身份,不是过度偏向。
4. **能否容纳 actual-skip 正结果 / 零收益 / verifier-testbed failure /
   measurement framing?** 是,逐项验证见 §4 表。
5. **全文加入实验构成换题吗?** 不构成:摘要已包含该实验的中性描述。
6. **今天不能出现的词**:见 §5 禁用表。
7. **必须保留的表达**:见 §5 保留表。

## 2. 裁决

```text
ABSTRACT_SUBMISSION = REVISE_THEN_GO
```

含义:不存在可直接提交的摘要;采用(或负责人微调)下方草案后,**今天
19:59(北京时间)前必须提交**。摘要提交是免费期权——即使一周后选择
撤回,也不损失任何东西;不提交则一切路线关闭。

## 3. 推荐提交内容

### Recommended title

> **Measure Before You Reuse: An Identifiability-First Study of
> Computation Reuse in LLM Agent Workflows**

备选(若负责人偏好更保守):
"When Can a Computation-Reuse Claim Be Trusted? Qualifying Testbeds,
Verifiers, and Realized Savings in LLM Agent Workflows"

### Recommended TL;DR

> Text-level usage proxies and public agent-framework traces cannot
> currently substantiate computation-reuse claims; we provide a
> preregistered qualification framework, a verifier-cost model for
> speculative reuse, and a controlled evaluation of exact reuse with
> outcome-level validation.

### Recommended abstract(≈200 词)

> Reusing previously completed computation — cached tool results, recorded
> model invocations, or repaired intermediate state — is an increasingly
> popular way to reduce the cost of LLM agent workflows. We argue that such
> claims currently rest on measurement foundations that have not been
> examined, and we examine them. First, using trace-conditioned replay with
> identifiability controls, we show that common text-level usage and
> equivalence proxies (output similarity, verbatim overlap, citation
> mentions) repeatedly fail as instruments for deciding whether reuse
> changed downstream behavior. Second, we introduce a preregistered
> testbed-qualification framework that distinguishes delivery, typed
> projection, and actual-read evidence, and apply it to three widely used
> open-source agent frameworks at pinned commits; within this audit, none
> exposes public runtime traces sufficient to substantiate selective
> computation-reuse claims. Third, we derive a cost model for speculative
> reuse with post-hoc verification, making explicit how verifier cost and
> blame attribution determine when reuse can pay. Finally, we conduct a
> controlled empirical evaluation of exact reuse — response-level and
> validated tool-result reuse under controlled state mutation — and report
> the realized computation skips, validation overheads, and outcome-level
> agreement. Together these results give a concrete standard for when a
> reuse claim is, and is not, supported.

自检:摘要中**没有任何尚未获得的具体实验数字**;没有把未来工作写成已
完成的结果(第四贡献承诺的是"报告实测值",不承诺方向或量级)。

### Topics / Keywords

- **Primary topic**:Intelligent Agents / LLM-based Agents(评测与分析方向;
  以提交系统实际 taxonomy 为准,选最接近 "agents — evaluation and
  analysis" 的条目)
- **Secondary topics**:Machine Learning — Evaluation & Benchmarks /
  Reproducibility;ML Systems(efficiency)
- **Keywords**:LLM agents; computation reuse; caching; speculative
  execution; verification cost; measurement validity; testbed
  qualification; reproducibility

## 4. 四种终局的兼容性验证

| 一周后的终局 | 摘要句子如何兑现 |
|---|---|
| actual-skip 正结果 | "report the realized computation skips…" 直接兑现,加实测数字 |
| 零收益/命中塌缩 | 同句兑现("realized skips"可以是接近零的实测值);结论句不变 |
| 实验 harness failure(Day 3 NO-GO) | 删除第四句或降格为 frozen-trace 分析表述;前三贡献自洽成文;属贡献收缩,非换题 |
| 纯 measurement/boundary framing | 摘要主身份本就是 measurement;无需改动 |

## 5. 措辞纪律

**今天禁止出现的词/句**(任何一个都构成兑现风险或诚实性问题):

- "novel caching/reuse mechanism"、"we propose a system"
- 任何具体数字(5.07%、13.7%、97.37%、1.69×…)
- "safe to reuse"、"reuse is (un)safe"
- "receiver-conditioned validity" 作为贡献(只可在正文 discussion 出现)
- "provenance-based invalidation"、"query-relative maintenance"(C6 强形式已关闭)
- "across the agent-framework ecosystem"(必须限定 within this audit)
- "first"/"state-of-the-art"/"significant speedup"

**必须保留的表达**(保证探索空间):

- "within this audit / at pinned commits"(框架结论的范围限定)
- "controlled empirical evaluation…report the realized…"(方向中性的实验句)
- "when reuse **can** pay"(条件式,不是 "reuse pays")
- "identifiability(-first)"(论文身份锚点)

**允许在全文前修改的范围**(不触发 substantial-change 风险):

- 删除或弱化第四句(实验句)——收缩贡献;
- 微调框架数量表述的限定语;
- 标题副标题微调(主标题 "Measure Before You Reuse" 不动);
- 增补关键词。

**不得发生的实质变化**:

- 把论文改写为机制/系统论文("we build X that speeds up Y");
- 把 audit 结论升格为生态普遍性结论;
- 加入摘要未涵盖的全新主贡献(如新的 C6' 实验线);
- 更换主标题语义。

## 6. 今日执行清单(P0)

1. 负责人确认标题+摘要文本(可微调,不改语义);
2. 北京时间 19:59 前在提交系统完成:标题、摘要、作者、topics/keywords;
3. 保存提交编号与确认邮件,追加记录到 `docs/RESEARCHSTUDIO_HANDOFF.md`
   (下一轮再提交,本轮不改该文件);
4. 提交完成后的第一项检查:重新打开提交系统核对已存文本与本文件 §3
   逐字一致(防止字段截断/编码丢字)。
