# Reset / Recovery 指南

> 本文件将在 S00-L03 的真实实验过程中逐步完善，不提前假设学习者的 Snapshot 树。

## 核心原则

恢复不是“点了 Revert 就算成功”。

必须同时有：

```text
Known State
→ Mutation
→ Observable Difference
→ Revert
→ Verification
```

## Snapshot 与 Backup

本节暂不直接给结论。

先在实际恢复实验完成后，根据观察补充：

- snapshot 保存了什么；
- snapshot 依赖哪些虚拟磁盘状态；
- revert 会改变什么；
- delete snapshot 实际意味着什么；
- 为什么长期灾备不能只依赖 snapshot。

## 当前参考 Baseline

```text
S00-UBUNTU-BASELINE
S00-KALI-BASELINE
```

这些名字来自课程真实搭建过程，仅作为参考实现。
## 第一轮实验得到的关键认识

### Snapshot 不等于 Backup

Snapshot 是某个时间点的 VM 状态检查点，但通常依赖原虚拟磁盘和后续增量链。

Backup 的范围可以很小，也可以很大：既可以是一个配置文件副本，也可以是完整磁盘或整机备份。判断关键不是“备份是不是整个系统”，而是它是否作为可恢复副本被独立保存和管理。

因此：

- snapshot 适合短期实验回滚；
- backup 适合独立恢复与长期保护；
- 不能因为“有 snapshot”就认为已经完成灾备。

### Revert 前先识别 Working State

真实环境中当前树为：

```text
S00-UBUNTU-BASELINE → 快照 2 → You Are Here
```

直接回旧 baseline 前，必须先确认当前 working state 是否包含仍需保留的变化。课程因此先增加 `S00-L03-PRE-MUTATION`，把本轮实验风险限定在一个明确 checkpoint 之后。