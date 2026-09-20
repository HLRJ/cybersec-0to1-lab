# S00-L03：Snapshot / Reset / Recovery

> 目标：把“虚拟机坏了就重装”升级成“能够证明环境已经恢复到一个已知状态”。

## 本课要学什么

这一课不引入漏洞，也不追求复杂工具。重点是建立后续所有攻防实验都会依赖的恢复能力：

- 区分当前状态、baseline snapshot、临时 checkpoint 与 backup；
- 在修改实验机之前先知道“正常状态”是什么；
- 制造一个无害、可观察的状态变化；
- Revert 后用证据证明状态真的恢复，而不是只相信 VMware 界面；
- 记录一套能够重复执行的 Reset 流程。

当前参考环境已经有：

```text
Ubuntu: S00-UBUNTU-BASELINE
Kali:   S00-KALI-BASELINE
```

本课优先复用这些真实 baseline，不重新虚构一套环境。

## 安全规则

- 本课所有操作只针对自己的 VMware Cyber Range。
- 第一轮只做观察，不修改系统、不 Revert。
- 在确认 Snapshot Manager 中的实际树结构之前，不假定 baseline 就是当前状态。
- 如果 current state 中存在尚未保存的重要修改，先确认再决定是否创建临时 safety snapshot。
## 第一轮：OBSERVE — 先确认“现在在哪里”

### Step 1：查看 Ubuntu Snapshot Manager

打开：

```text
VMware Workstation
→ 选择 cyberlab-ubuntu
→ VM
→ Snapshot
→ Snapshot Manager
```

确认并记录：

- 是否存在 `S00-UBUNTU-BASELINE`；
- `You Are Here` 当前位于 baseline 之前、之后，还是其他 snapshot 分支；
- 除 baseline 外是否还有其他 snapshot；
- 当前 VM 是运行、暂停还是关机状态。

**现在不要点 Go To / Revert / Delete。**

最好截一张 Snapshot Manager 图，后续放进课程作为真实证据。

### Step 2：记录 Ubuntu 当前状态

在 Ubuntu 当前状态执行：
```bash
hostname
ip -brief address
ip route
systemctl is-active ssh
test -e ~/s00-l03-marker.txt && echo "MARKER=EXISTS" || echo "MARKER=ABSENT"
```

把实际输出记录到：

```text
progress/s00/l03-reset-record.md
```

这里暂时把它称为 **Current State**，不要提前叫 Baseline。

### Step 3：回答三个问题

不用查资料，先按自己的理解回答：

1. Snapshot 和 Backup 是一回事吗？为什么？
2. 如果创建 snapshot 后又新建一个文件，Revert 回 snapshot 后，你预计这个文件还在吗？
3. 如果 `You Are Here` 不在 `S00-UBUNTU-BASELINE` 上，直接 Revert 可能丢掉什么？

## 本轮停止点

完成上面三步后先停下来，把 Snapshot Manager 截图、5 条状态命令输出、三个问题的回答发回来。
下一轮我们再根据你的**真实 snapshot 树**执行：

```text
BASELINE EVIDENCE
→ HARMLESS MUTATION
→ PROVE MUTATION
→ REVERT
→ PROVE RECOVERY
→ REPEAT
```

不会先假设恢复步骤。

## 最终 Gate（先知道目标，不要求现在完成）

- 能明确指出恢复基线；
- 能制造并证明一个无害状态变化；
- 能执行 Revert；
- 能用命令证据证明恢复成功；
- 同一恢复流程重复执行得到一致结果；
- 能解释 Snapshot 为什么不能替代 Backup。

完成 Gate 后才创建：

```text
s00-l03-complete-v2
```