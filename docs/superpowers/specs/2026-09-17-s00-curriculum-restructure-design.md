# S00 课程结构重构设计

**日期：** 2026-09-17

> 本文件遵循仓库“核心课程稳定前只维护中文版”的语言策略。代码、命令、路径、协议字段与 Git tag 保持英文原样。

## 问题

最初的 S00 第一课被实现为 Authorization & Scope，但学习者当时还没有创建任何真实实验资产。

在第一次学习者实跑过程中，这暴露出一个错误依赖：仓库先假定了一个并不存在的 VMware 实验网段，再要求学习者围绕这个虚构网段定义授权范围。

修正后的教学原则是：

**先建立并验证真实实验资产，再基于这些实际、已授权的资产定义 Scope。**

## 决策

重新调整 Stage 00 的顺序：先让学习者搭建一个隔离的 VMware Cyber Range，再针对这套真实环境学习授权与 Scope。

### S00-L01 — Build Your Cyber Range

仓库需要记录并教学学习者实跑时采用的、可复现的环境搭建流程：

- 从官方来源下载 Ubuntu Server 与 Kali；
- 使用官方发布的 checksum 校验 SHA256；
- 创建一个专用 VMware Host-Only 网络，并关闭 DHCP；
- 为 Windows Host、Ubuntu Target 与 Kali Tester 规划地址；
- 安装/配置 Ubuntu，并导入/配置 Kali；
- 默认不给 Ubuntu/Kali 配置 Internet default route；
- 验证三节点连通性矩阵；
- 使用 `8.8.8.8` 这类 IP 地址而不是 DNS 名称验证 Internet 隔离；
- 验证通过后创建 baseline snapshot；
- 记录真实学习过程中的排障经验，包括本次 Kali 光标不可见问题：在这个具体案例中，根因是旧的 VMware virtual hardware compatibility。

学习者本次实际环境为 `192.168.77.0/24`，但公开课程必须教学习者自行发现、创建并记录自己的实验网段，而不是把 `.77` 当作所有人的固定配置。

### S00-L02 — Authorization & Scope

把现有 Scope 课程从：

`labs/s00/l01-scope/`

移动为：

`labs/s00/l02-scope/`

本课必须明确使用学习者在 L01 中已经验证过的 Cyber Range 网段。

仓库示例配置可以继续使用 `192.168.77.0/24` 作为参考实现，但正文必须说明：授权来自学习者真实、明确设计的实验环境，而不是因为目标属于 RFC1918/private address 就天然获得授权。

deny-by-default 的目标校验逻辑及其自动化测试在概念上保持不变。

## 调整后的 Stage 00 顺序

1. **S00-L01 — Build Your Cyber Range**
2. **S00-L02 — Authorization & Scope**
3. **S00-L03 — Snapshot / Reset / Recovery**
4. **S00-L04 — Workstation & Toolchain**
5. **S00-L05 — Baseline Telemetry**

S00 不引入任何故意漏洞。

## 仓库改动

预期实现改动：

- 创建 `labs/s00/l01-cyber-range/README.md`；
- 将 `labs/s00/l01-scope/` 移动/重命名为 `labs/s00/l02-scope/`；
- 更新 `README.md`、`CURRICULUM.md`、`docs/CURRICULUM_DESIGN.md` 与 `docs/LAB_RULES.md`，确保编号和前置关系一致；
- 保留 `scope/lab-scope.yaml`、`scripts/check_lab_target.py` 与现有 Scope tests，只修改因课程编号变化而需要调整的引用；
- CI 继续运行自动化 Scope tests。

## S00-L01 Gate

只有当学习者能够提供以下证据时，才算通过 L01：

- Windows Host、Ubuntu 与 Kali 都位于专用实验网络中，并且能够按计划互通；
- Ubuntu 与 Kali 都没有通往 Internet 的 default route；
- 对外部 IP 执行 `ping` 或等价测试时，因为没有路由而失败；
- 实验 VM 已建立 baseline snapshot；
- 学习者能够解释为什么 Host-Only + 无 default route 能降低误触非授权目标的风险。

## Checkpoint 与 Tag 策略

已经推送到公开仓库的 `s00-l01-complete` 指向重构前的旧 Scope 课程，因此在新的课程结构下语义已经过时。

**不要**静默 force-move、重写或删除这个公开 tag。它应保留为历史记录。

重构完成后，为修正后的课程创建新的、语义清晰的 checkpoint tag；必要时使用版本后缀，例如：

- `s00-l01-complete-v2`
- `s00-l02-complete-v2`

最终 tag 名称在实现阶段确定，并在 PR 中记录。

## 需要保留的排障内容

L01 应保留来自真实学习过程的简洁排障说明：

- 安装前先校验官方 ISO/archive 的 hash；
- 区分 VMware Host-Only adapter 与 NAT；
- 关闭 DHCP 后使用静态地址；
- Ubuntu 为了隔离，静态地址配置时故意留空 gateway/DNS；
- Kali 通过 NetworkManager 配置静态地址，并使用 `ipv4.never-default yes`；
- SSH 可作为 service-level validation 的一个有用检查项；
- Kali 鼠标光标不可见：在本次学习环境中，`open-vm-tools` 已安装，关闭 3D acceleration 也没有解决；把导入 VM 从旧的 virtual hardware compatibility（`virtualHW.version = "8"`）升级后问题消失。该结论必须作为本次案例的特定根因，而不能写成通用规律。

## 非目标

本次重构不包含以下内容：

- vulnerable services；
- scanning exercises；
- exploitation；
- Active Directory；
- Internet-facing targets；
- 把学习者的物理 LAN 纳入 Scope。

## 验收标准

当以下条件全部满足时，本次重构才算完成：

- 所有 Stage 00 文档都一致采用新的 L01/L02 编号；
- 环境搭建课程可以脱离本次聊天记录独立复现；
- 公开课程不会把 `192.168.77.0/24` 写成所有学习者必须使用的固定网段；
- Scope 继续保持 deny-by-default，并且 tests 通过；
- PR 上 CI 通过；
- 不再存在旧路径或旧文案错误地声称 Scope 是 S00-L01。
