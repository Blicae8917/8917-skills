# 8917-wenzhen（问诊，原 8917-blindspot）框架出处速查

调研日期：2026-07-08

## 十问与框架的对应关系

| 问 | 框架来源 | 出处 |
|---|---|---|
| Q1 置信度审计 | fabric 置信度数字化实践；自然语言模糊自信的对抗 | [danielmiessler/fabric](https://github.com/danielmiessler/fabric) |
| Q2 双向邓宁-克鲁格 | fabric `t_check_dunning_kruger`（高估区/低估区/元认知缺口四段式） | 同上 |
| Q3 盲点+未知的知 | fabric `t_find_blindspots`、`t_find_neglected_goals`；Rumsfeld matrix 的"unknown knowns"格 | [Rumsfeld Matrix](https://www.theschoolofknowledge.net/p/the-rumsfeld-matrix-explained) |
| Q4 第十人异议 | 以色列第十人原则 / IDF Devil's Advocate Unit（红队制度化：当所有人同意时，反对是职责） | [The Tenth Man Rule](https://themindcollection.com/the-tenth-man-rule-devils-advocacy/) · [Devil's Advocate Unit](https://en.wikipedia.org/wiki/Devil%27s_Advocate_Unit) |
| Q5 事前验尸 | Gary Klein premortem——"前瞻性后见之明"使失败归因准确率提升约 30% | [HBR: Performing a Project Premortem](https://hbr.org/2007/09/performing-a-project-premortem) |
| Q6 外部视角 | Kahneman outside view / reference class forecasting（基准率优先于内部精算） | [The outside view](https://corporate.jasoncollins.blog/outside-view) |
| Q7 可证伪性 | fabric `check_falsifiability`（含"移动球门柱"与"定义逃逸口"检测） | fabric patterns |
| Q8 机会成本+二阶效应 | 机会成本框架；Second-Order Thinking（"然后呢"至少两层） | [Second-Order Effects](https://builder.aws.com/content/386hy8jIPr3Q7o5YYeEy5hUq2TR/second-order-effects-the-hidden-cost-of-decisions) |
| Q9 领先一手 | 指挥官原五问第③问（保留血统） | 8917 原创 |
| Q10 止损线+谄媚自审 | 终止条件设计；LLM sycophancy 对抗实践；self-eval skill 的反通胀机制（魔鬼代言人推理对抗自评虚高） | [Forbes: Stop AI Sycophancy](https://www.forbes.com/sites/lanceeliot/2026/04/03/using-one-simple-prompt-can-stop-ai-sycophancy-and-keep-your-mind-from-being-bent-out-of-shape-by-ai/) · [Self-Eval Skill](https://mcpmarket.com/tools/skills/honest-ai-self-evaluation) |
| 执行姿态·第一性 | 指挥官原五问第⑤问（升格为贯穿姿态而非单问） | 8917 原创 |
| 执行姿态·可逆性 | Bezos one-way / two-way doors | [Blueprints](https://blueprints.guide/posts/one-way-vs-two-way-doors) |
| 执行债对账 | 军事 AAR 四问（计划 vs 实际 → 保留/改进）；2026-07-08 星岛项目三轮五问的实际教训（"分析了≠做了"） | [Four Part AAR](https://www.adventureassoc.com/the-four-part-after-action-review/) |

## 输出硬约束的出处

- 强制条数+字数上限：fabric 全系 pattern 的 "N bullets, 16 words each" 惯例
- 禁止相同开头：fabric `analyze_mistakes` 原文 "Do not start items with the same opening words"
- 分轴打分防"整体不错"：self-eval skill 的双轴（野心/执行）+ 反通胀检测
- 谄媚自审强制收尾：提问者自己不会想到要审查审查者——这是 skill 跳出提问者维度的关键机关

## 设计原理（一句话）

原五问的结构性局限是**全部锚定在同一时间点、同一视角**；本 skill 的升级本质是**换轴**——时间轴（Q5）、概率轴（Q6）、退出轴（Q10）、身份轴（Q10 自审），每轴一个最锋利的问题，胜过在原轴上堆问题数量。

## 未收录但值得知道的框架

- Roger Martin "What would have to be true?"（反推成立条件）——部分融入 Q7
- Amazon Working Backwards PR-FAQ（"最难回答的 FAQ 是什么"）——适合产品立项场景，可在 Q9 中借用
- Socratic 六类提问之第六类"反问问题本身"——已实现为【元异议】机制
