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
## 第二轮：建立安全 Checkpoint，再制造可观察变化

第一轮真实观察得到的 Snapshot 树是：

```text
S00-UBUNTU-BASELINE
        ↓
      快照 2
        ↓
     You Are Here
```

因此本轮**不直接 Revert 到 baseline**。当前 working state 可能包含 `快照 2` 之后的正常变化。

### Step 4：创建本课专用安全 Snapshot

在当前 `You Are Here` 位置创建：

```text
S00-L03-PRE-MUTATION
```

建议描述：

```text
Known-good state before S00-L03 harmless mutation
```

创建后再次打开 Snapshot Manager，确认 `You Are Here` 位于这个新 snapshot 之后。

**此时仍不要 Revert 或 Delete 任何 snapshot。**
### Step 5：制造一个无害、可验证的 Mutation

在 Ubuntu 执行：

```bash
printf 'S00-L03 harmless mutation\n' > ~/s00-l03-marker.txt
ls -l ~/s00-l03-marker.txt
cat ~/s00-l03-marker.txt
sha256sum ~/s00-l03-marker.txt
```

然后再次执行：

```bash
test -e ~/s00-l03-marker.txt && echo "MARKER=EXISTS" || echo "MARKER=ABSENT"
```

本轮期望：

```text
MARKER=EXISTS
```

### 第二轮停止点

把下面两项发回来后再继续：

1. 创建 `S00-L03-PRE-MUTATION` 后的 Snapshot Manager 截图；
2. marker 的 `ls`、`cat`、`sha256sum` 和 `MARKER=EXISTS` 输出。

确认安全 checkpoint 和 mutation 都存在之后，我们才执行第一次 Revert。
### 常见失误：先 Mutation，后想起 Snapshot

如果已经执行了 mutation，却发现还没有创建 safety snapshot：

- 不要立刻回到更老的 snapshot；
- 先判断 mutation 是否完全已知、是否可以安全手工撤销；
- 对于本课这种单一 marker 文件，可以先删除 marker，并重新验证 Current State；
- 再创建 `S00-L03-PRE-MUTATION`；
- 然后重新执行 mutation。

这条规则背后的重点是：**Snapshot 的顺序本身也是实验设计的一部分。**