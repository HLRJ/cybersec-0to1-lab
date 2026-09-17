# 课程设计规范

版本：v0.2 中文主版本  
项目：`cybersec-0to1-lab`  
适用对象：课程维护者、未来贡献者、自动化开发代理。

## 1. 设计目标

课程第一目标是维护者自己学透网络安全；第二目标是公开后让其他学习者能复现同一条路线。课程必须可运行、可修改、可调试、可恢复、可测试，而不是只可阅读。

## 2. 语言策略

Core Curriculum 完成并稳定前只维护中文版。中文用于 README、课程正文、Lab 指引、Boss/Gate、设计规范和注释说明；代码、命令、协议字段、API、函数名、类名、库名保持英文原样。英文版作为后续发布工作统一制作，不在早期双语维护。

## 3. 教学闭环

每个核心安全 Lab 原则上使用同一循环：

```text
RUN → OBSERVE → BUILD → BREAK → TRACE → SOURCE DIVE
    → ROOT CAUSE → FIX → DETECT → TEST → VERIFY → REFLECT
```

并非每一课都必须有人为漏洞；S00–S02 重点是建立环境、协议模型和正常系统。S03 之后才系统性加入故意漏洞。

## 4. 代码深度等级

- C1 Read：读懂并定位相关代码/配置。
- C2 Trace：跨组件追踪数据流、调用流、权限流。
- C3 Implement：亲手实现关键机制、安全版或故障版。
- C4 Internals：继续追到协议、解析器、运行时、数据库驱动或 OS 内部机制。

“会运行安全工具”不能单独构成 C3/C4。

## 5. Lab Definition of Done

一个 Lab 只有同时满足以下条件才算完成：

- 学习目标明确且前置知识可追溯；
- 示例代码可运行，命令可复现；
- 至少保存一种可验证证据：测试结果、PCAP、日志、截图或结构化输出；
- 能解释根因或底层机制，而不是只复述步骤；
- 若存在安全缺陷，必须提供修复并重新验证；
- 关键行为有自动化测试或明确的手工 Gate；
- 文档不存在未说明的跳步；
- 对应 Git checkpoint 已定义。

## 6. Boss / Gate 规则

Boss 不应只是多个小题拼接。Boss 必须减少提示，要求学习者迁移能力，并输出可审查成果。

Gate 的判断依据采用三类证据：

1. **Task**：能否完成可观察任务；
2. **Knowledge**：能否解释为何这样工作；
3. **Skill**：能否在陌生但同类环境中迁移。

只会照抄命令不能通过 Gate。

## 7. MiniCorp 设计原则

MiniCorp 是贯穿课程的持续演化工程，而不是每章重新出现一台无关靶机。S02 建立最小正常版本；S03 才在独立 checkpoint 中引入故意漏洞；后续逐渐增加浏览器、Linux/Windows、AD、Telemetry 与 Detection。

每次扩展遵守 YAGNI：只添加当前 Stage 为了学习目标真正需要的组件。
## 8. 安全边界设计

攻击性代码默认只能指向课程提供或学习者显式声明的实验目标。后续目标校验工具需要：

- 支持明确配置的实验网段；
- 默认拒绝未授权公网地址；
- 对解析后的主机名再次检查实际目标地址；
- 错误信息必须说明为什么拒绝，而不是静默跳过。

课程文档不能以“仅供学习”一句话代替技术护栏。

## 9. Git 教学设计

每个 Lab 的状态尽量通过标签或稳定 checkpoint 表达：

```text
sXX-lYY-start
sXX-lYY-baseline / vulnerable
sXX-lYY-fixed / exercise
sXX-lYY-complete
```

漏洞课必须允许学习者通过 `git diff` 直接看到 vulnerable 与 fixed 之间的关键代码差异。Boss 使用 `sXX-boss-start` / `sXX-boss-complete`。

## 10. 外部课程借鉴原则

可以借鉴成熟平台的教学方法和公开知识框架，但不复制其受版权保护的题目、答案或课程正文。

- PortSwigger：Web 学习顺序与大量迁移练习；
- pwn.college：渐进挑战、底层原理和综合 Boss；
- SEED Labs：协议/系统实验与“亲手验证”方法；
- PentesterLab：源码审计与白盒安全；
- TryHackMe / HTB Academy：陌生环境迁移、AD 与企业攻防；
- OWASP WSTG / ASVS：测试方法与安全验收；
- MITRE ATT&CK：后期企业攻击行为与检测映射。

## 11. 早期阶段约束

S00：不教漏洞利用。先创建真实、隔离、可恢复的实验资产，再基于这些真实资产定义 Scope，随后完成恢复、工具链与 Telemetry；不围绕虚构网段教授授权。
S01：先用代码和抓包理解协议，再引入扫描/代理工具。  
S02：构建正常 MiniCorp，不为了“有靶场”而提前埋漏洞。  
只有 S02 Boss 通过，才进入 S03。
