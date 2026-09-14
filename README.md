# 网络安全攻防 0→1 实战 Lab

> **Build it. Break it. Trace it. Fix it. Detect it.**

一套以真实代码工程为主轴的中文网络安全课程：从 Socket、TCP、DNS、HTTP/TLS 开始，亲手构建 MiniCorp，再逐步进入 Web 安全、源码审计、Linux/Windows、Active Directory、检测工程与 Purple Team。

## 为什么做这个项目

第一目标：我们自己沿着仓库真正把网络安全学透。

第二目标：课程稳定后，让其他学习者也能 clone、运行、修改、调试、修复并完成同样的 Gate。

这不是 Kali 命令合集，也不是漏洞百科。每个核心安全 Lab 都追求：

```text
运行 → 观察 → 构建 → 攻击/破坏 → 追踪 → 源码/协议深入
    → 根因 → 修复 → 检测 → 测试 → 再验证 → 复盘
```

## 当前状态

**课程设计阶段已完成，仓库进入实施阶段。**

- 10 个 Stage
- 58 个核心 Lab
- S00 / S01 / S02 已细化到可实施粒度
- 当前只维护中文版
- S03 之前不提前教授漏洞利用

## 从这里开始
1. 阅读 [课程总纲](CURRICULUM.md)
2. 阅读 [课程设计规范](docs/CURRICULUM_DESIGN.md)
3. 查看 [S00–S02 实施计划](docs/superpowers/plans/2026-09-14-s00-s02-implementation.md)
4. 后续从 S00-L01 开始实际学习

## 核心路线

`S00 实验室 → S01 协议 → S02 构建 MiniCorp → S03 Server-side → S04 Browser → S05 AppSec → S06 Host → S07 AD → S08 Detection/Purple → S09 Cyber Range`

## 安全边界

本仓库的攻击性实验只允许用于：

- 仓库明确提供的靶场；
- 你自己拥有并明确用于实验的环境；
- 获得明确书面授权的目标。

**不能明确说明授权来源的目标，不属于本课程测试范围。**

## 语言

核心课程完成前只维护中文版。代码、命令、协议、API、函数名等技术标识保留英文原样；英文版在 Core 稳定后统一制作。

## License

MIT。课程内容和代码可以学习、修改和再发布，但请遵守目标系统授权边界，并尊重外部课程与资料的版权。
