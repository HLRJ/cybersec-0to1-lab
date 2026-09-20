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