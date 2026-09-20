# S00-L03 Reset Record

## Round 1 — Current State Observation

日期：2026-09-20

VM：`cyberlab-ubuntu`

当前 VMware 状态：运行中，`You Are Here` 位于 `快照 2` 之后。

Snapshot Manager：

```text
S00-UBUNTU-BASELINE
        ↓
      快照 2
        ↓
     You Are Here
```

说明：当前状态不是 `S00-UBUNTU-BASELINE`，也不是 `快照 2` 本身，而是在 `快照 2` 之后继续产生的 working state。

### Current State Evidence

```text
hostname:
cyberlab-ubuntu

ip -brief address:
lo      UNKNOWN  127.0.0.1/8 ::1/128
ens33   UP       192.168.77.10/24 fe80::20c:29ff:fe5b:aa4f/64
ip route:
192.168.77.0/24 dev ens33 proto kernel scope link src 192.168.77.10

systemctl is-active ssh:
active

marker:
MARKER=ABSENT
```

观察结论：

- Ubuntu 仍保持 `192.168.77.10/24`；
- 只有实验网直连路由，没有 default route；
- SSH 服务处于 active；
- `~/s00-l03-marker.txt` 当前不存在。

### 学习者初始理解

1. Snapshot 和 Backup 不是一回事。学习者用“修改配置前先 `cp` 一份旧配置”的经验理解 backup；snapshot 更像把虚拟机恢复到某个时间点。

2. 在 snapshot 之后新建文件，再 Revert 回 snapshot，预计该文件不会存在。

3. 如果当前状态不在 baseline，直接 Revert 可能丢掉 snapshot 之后产生的变化。

### 校正与补充

- `cp config config.bak` 是 backup 的一种局部形式，但 backup 也可以覆盖目录、磁盘、VM 或整机。
- Snapshot 与 Backup 的关键差异不只是范围大小：VM snapshot 通常依赖原虚拟磁盘及增量链，不应视为独立灾备副本。
- Revert 到较早 snapshot 时，已有的后续 snapshot 节点通常仍可保留；最需要警惕的是当前 working state 中尚未进入任何 snapshot 的变化。

## Round 2 — Safety Checkpoint / Mutation

下一轮先创建 `S00-L03-PRE-MUTATION`，再制造 marker 文件。确认 mutation 已被观察到后，才进入 Revert。
## Round 2 — Mutation 先于 Safety Snapshot（真实学习者失误）

学习者实际执行顺序出现了一个重要偏差：

```text
原计划：PRE-MUTATION snapshot → mutation
实际：   mutation → 发现尚未创建 PRE-MUTATION snapshot
```

Snapshot Manager 截图显示仍为：

```text
S00-UBUNTU-BASELINE → 快照 2 → You Are Here
```

marker mutation 已成功：

```text
/home/cyberlab/s00-l03-marker.txt
content: S00-L03 harmless mutation
sha256: cf3da52f7632ceba64e021919198c4d17df6918bd3c4f9edc86e57804e6742af
MARKER=EXISTS
```

### 纠正策略

由于本轮 mutation 完全已知且只创建了一个 marker 文件，不需要冒险回到旧 snapshot。

先手工撤销这一个已知 mutation，重新验证 marker 不存在以及网络/SSH 仍保持 Current State，然后再创建 `S00-L03-PRE-MUTATION`。

这也形成一条课程规则：**Checkpoint 必须在 Mutation 之前创建并验证存在；不要把“准备做 snapshot”当成“已经做了 snapshot”。**
## Round 3 — First Revert / Recovery Verification

### Revert 前

```text
snapshot: S00-L03-PRE-MUTATION
marker: MARKER=EXISTS
marker sha256: cf3da52f7632ceba64e021919198c4d17df6918bd3c4f9edc86e57804e6742af
```

### 执行 Revert 时的现象

VMware 恢复 `S00-L03-PRE-MUTATION` 后，原 SSH 会话断开：

```text
Socket error Event: 32 Error: 10053
Connection closed by foreign host
```

这是符合预期的现象：虚拟机运行状态/网络状态被恢复时，已有 TCP/SSH 会话不会跨 Revert 保持。

随后重新连接 `192.168.77.10:22` 成功。

### Revert 后证据

```text
hostname: cyberlab-ubuntu
ens33: UP 192.168.77.10/24
route: 192.168.77.0/24 dev ens33 proto kernel scope link src 192.168.77.10
ssh: active
marker: MARKER=ABSENT
ping 192.168.77.1: 2/2 received, 0% packet loss
```

### 结论

- 文件系统状态确实回到了 `S00-L03-PRE-MUTATION`；
- 实验网静态 IPv4 保持正确；
- 没有出现 default route；
- SSH 服务恢复为 active；
- Windows Host 仍可从实验网访问；
- 因此不能只凭 VMware 显示“已恢复”判断成功，必须由 Guest OS 内部证据完成 verification。

登录 banner 中访问 `changelogs.ubuntu.com` 失败，与“无 Internet default route”的设计一致，但这只能作为旁证，路由表才是主要证据。