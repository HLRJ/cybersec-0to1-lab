# Checkpoints

本文件记录课程 checkpoint 的当前语义，以及课程结构调整后保留的历史 tag。

## Legacy checkpoints

| Tag | 状态 | 含义 |
|---|---|---|
| `s00-l01-start` | legacy | 2026-09-17 重构前的 Scope starter |
| `s00-l01-complete` | legacy | 重构前 Scope Lab 的完成状态；已经公开推送，不移动、不删除、不覆盖 |

这些 tag 只用于保留仓库历史。不要根据旧名称推断当前课程编号。

## Current S00 checkpoints

| Tag | 当前含义 |
|---|---|
| `s00-l01-complete-v2` | S00-L01 Build Your Cyber Range 完成 |
| `s00-l02-complete-v2` | S00-L02 Authorization & Scope 完成 |
| `s00-l03-complete-v2` | S00-L03 Snapshot / Reset / Recovery 完成 |
| `s00-l04-complete-v2` | S00-L04 Workstation & Toolchain 完成 |
| `s00-l05-complete-v2` | S00-L05 Baseline Telemetry 完成 |

## 规则

- 已公开 tag 不做静默强制移动；
- 课程重构导致语义变化时，使用新且无歧义的 tag；
- checkpoint 只在对应 Gate 已实际通过、测试通过并进入 `main` 后创建；
- tag 是学习状态的稳定锚点，不替代课程文档本身。