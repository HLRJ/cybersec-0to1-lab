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

Snapshot 是为短期回滚服务的时间点检查点。VMware snapshot 通常依赖原虚拟磁盘以及 snapshot chain，因此它并不是一个可以脱离原 VM 独立保存的长期灾备副本。

Backup 可以是文件级、目录级、磁盘级或整机级；核心在于它作为独立恢复副本被保存、验证和管理。

因此本课程采用下面的判断：

- destructive experiment 前：优先创建 snapshot；
- 需要快速重复实验：使用 known-good snapshot / checkpoint；
- 无法轻易重建的重要数据：另做 backup；
- 长期保存或灾难恢复：不能只依赖 snapshot；
- Revert 后：必须重新验证 Guest OS，而不是只看 VMware UI。

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
## Revert 后为什么 SSH 会断开

如果通过 SSH 操作实验 VM，执行 VMware Revert 时原 SSH 会话通常会断开。

原因不是 SSH 配置损坏，而是虚拟机状态发生回滚，原 TCP 会话两端的运行状态已经不再连续。

因此恢复验证应包含：

```text
Revert
→ 等待 Guest 恢复
→ 重新建立 SSH
→ 检查 hostname / IP / route / service / mutation evidence
```

“SSH 重新连接成功”可以作为 service-level evidence，但不能替代 Guest 内部状态检查。
## 多状态恢复验证

只验证一个 marker 文件还不够证明恢复流程可靠。

第二轮实验同时改变：

```text
Persistent state → marker file
Runtime state    → cron service
```

Revert 后两个状态同时恢复，同时 SSH 与实验网继续正常。

这说明验证恢复时应覆盖不同类型的 evidence，而不是只检查“VM 能不能开机”。

推荐恢复验证最少包含：

- 一个持久化文件/配置状态；
- 一个运行时 service state；
- IP / route；
- 一个可实际使用的服务连接；
- 与 Host 的实验网连通性。