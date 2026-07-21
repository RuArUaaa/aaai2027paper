# C4 Gate Verdict

**C4_GATE = REQUIRES_AUTHORIZATION**

日期:2026-07-21 · 主协调代理

资格门协议(`protocol.md`)与静态可行性检查(`results.json`)已完成:
控制组(正控/NC1/NC2)已预登记,真实 mutation 语料来源已确认可获得,
唯一阻塞项是 GPU + 模型调用授权。

按任务书 §七-C 条规定:gate 需要模型或 GPU 时,完成协议设计与静态可行性检查后
停止执行并标记 REQUIRES_AUTHORIZATION。本 gate 未执行任何实验。

**主席附注(与 CP2 联动的范围声明)**:C4 在 CP2 中被判 HIGH_COLLISION
(C4-P6 DIRECT + KEEP PARTIAL-strong)。即使未来获得授权,本协议也不应以
"C4 原始形式"直接进入一周实验;其残余空位(receiver×mutation 联合条件化、
task-conditioned 修复、一般 mutation 结构的可修复边界)若要保留,必须重新表述为
相对 C4-P6 的增量实验,并先确认 C4-P6 的发表状态是否变化。详见
`scoop_checks/C4_scoop_check.md` 与最终决策备忘。
