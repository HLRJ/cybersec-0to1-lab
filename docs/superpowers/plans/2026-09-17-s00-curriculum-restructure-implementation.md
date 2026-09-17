# S00 Curriculum Restructure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把真实完成的 Cyber Range 搭建流程正式沉淀为 S00-L01，将 Scope 顺延为 S00-L02，并让仓库、测试、CI、checkpoint 语义保持一致。

**Architecture:** S00 仍保持 5 个核心 Lab，但重新排序为 Cyber Range → Scope → Snapshot/Reset → Workstation/Toolchain → Baseline Telemetry。`192.168.77.0/24` 只作为本课程的参考实现；公开课程明确要求学习者先创建自己的隔离实验网，再把真实网段写入 Scope。

**Tech Stack:** Markdown, Python 3.12+, pytest, PyYAML, Git/GitHub Actions, VMware Workstation, Ubuntu Server, Kali Linux.

**Spec:** `docs/superpowers/specs/2026-09-17-s00-curriculum-restructure-design.md`

## Global Constraints

- 第一阶段课程正文只维护中文版，命令、协议字段、函数名等技术标识保持英文原样。
- S00-S02 不引入故意漏洞；主动安全实验只允许 loopback 或学习者明确授权的隔离实验网。
- 先创建真实实验资产，再定义 Scope；不得用虚构网段替代真实环境。
- 公共教程不得暗示所有学习者都必须使用 `VMnet2` 或 `192.168.77.0/24`；它们是参考实现。
- 课程参考环境记录：Windows Host `192.168.77.1`、Ubuntu `192.168.77.10`、Kali `192.168.77.20`、DHCP OFF、Guest 无 default route。
- 已公开的 legacy tag `s00-l01-complete` 不强制移动或删除；重构后使用无歧义的 `-v2` checkpoint。
- Kali 鼠标光标问题只能表述为“本次案例由旧 `virtualHW.version = "8"` 兼容级别触发并通过升级 Hardware Compatibility 解决”，不得泛化成所有环境的固定原因。

---

## File Map

- Create: `labs/s00/l01-cyber-range/README.md` — 从零搭建隔离 Cyber Range 的正式 Lab。
- Rename: `labs/s00/l01-scope/README.md` → `labs/s00/l02-scope/README.md` — Scope 顺延到 L02。
- Create: `docs/CHECKPOINTS.md` — 解释 legacy tags 与重构后的 v2 checkpoint。
- Create: `tests/test_course_structure.py` — 防止 S00 编号、目录和 checkpoint 再次漂移。
- Modify: `CURRICULUM.md` — 重写 S00 五课顺序和 Gate。
- Modify: `README.md` — 更新学习起点与课程路径。
- Modify: `docs/CURRICULUM_DESIGN.md` — 固化“先资产、后 Scope”的课程设计原则。
- Modify: `docs/LAB_RULES.md` — 说明参考实验网与学习者实际 Scope 的关系。
- Modify: `docs/superpowers/plans/2026-09-14-s00-s02-implementation.md` — 标记旧 S00 编号已被本计划替代，避免执行旧路线。
- Modify: `.github/workflows/ci.yml` — 从只跑两个 Scope 测试改为运行完整 pytest。

---

### Task 1: 用测试锁定新的 S00 结构

**Files:**
- Create: `tests/test_course_structure.py`

**Interfaces:**
- Consumes: 仓库目录结构和 Markdown 文档。
- Produces: CI 可执行的课程结构回归测试。

- [ ] **Step 1: 写失败测试**

```python
from pathlib import Path


def test_s00_lab_paths_follow_restructured_order() -> None:
    assert Path("labs/s00/l01-cyber-range/README.md").is_file()
    assert Path("labs/s00/l02-scope/README.md").is_file()
    assert not Path("labs/s00/l01-scope").exists()


def test_restructured_checkpoints_are_explicit() -> None:
    l01 = Path("labs/s00/l01-cyber-range/README.md").read_text(encoding="utf-8")
    l02 = Path("labs/s00/l02-scope/README.md").read_text(encoding="utf-8")
    assert "s00-l01-complete-v2" in l01
    assert "s00-l02-complete-v2" in l02


def test_curriculum_lists_s00_labs_in_order() -> None:
    text = Path("CURRICULUM.md").read_text(encoding="utf-8")
    headings = [
        "## S00-L01",
        "## S00-L02",
        "## S00-L03",
        "## S00-L04",
        "## S00-L05",
    ]
    positions = [text.index(heading) for heading in headings]
    assert positions == sorted(positions)
```

- [ ] **Step 2: 验证 RED**

Run:
```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_course_structure.py -q
```
Expected: FAIL，因为 `l01-cyber-range` 和 `l02-scope` 尚不存在。

- [ ] **Step 3: 提交测试**

```powershell
git add tests/test_course_structure.py
git commit -m "test: lock restructured S00 course layout"
```

---

### Task 2: 创建 S00-L01 Cyber Range 并顺延 Scope

**Files:**
- Create: `labs/s00/l01-cyber-range/README.md`
- Rename: `labs/s00/l01-scope/README.md` → `labs/s00/l02-scope/README.md`

**Interfaces:**
- Consumes: 已实际完成的 VMware/Ubuntu/Kali 搭建过程。
- Produces: 不依赖聊天记录即可复现的 S00-L01，以及新的 S00-L02 Scope Lab。

- [ ] **Step 1: 用 `git mv` 顺延 Scope Lab**

```powershell
git mv labs/s00/l01-scope labs/s00/l02-scope
```

- [ ] **Step 2: 修改 Scope Lab 标题和 checkpoint**

必须把标题改为 `S00-L02`，并把通关 checkpoint 改成：

```text
s00-l02-complete-v2
```

Scope 的核心行为不变：deny-by-default、allowlist、拒绝网络地址/IPv4 广播地址、第一版只接受 IP literal。

- [ ] **Step 3: 编写 Cyber Range Lab**

`labs/s00/l01-cyber-range/README.md` 必须按以下顺序完整覆盖：

```text
目标与安全边界
→ 官方来源下载 Ubuntu/Kali
→ SHA256 完整性校验
→ 查看 Windows 现有网卡/VMnet，避免占用真实 WLAN
→ 新建独立 Host-Only VMnet，DHCP OFF
→ 规划参考地址
→ 安装 Ubuntu Server，静态 IPv4，无 gateway/DNS
→ 导入 Kali VMware 镜像，修改默认密码
→ Kali 静态 IPv4 + ipv4.never-default yes
→ 三节点连通矩阵
→ ip route 验证无 default route
→ ping 8.8.8.8 验证默认隔离
→ baseline snapshots
→ Troubleshooting：Kali 鼠标案例
→ Gate
```

参考实现必须明确标注为示例：

```text
VMnet2              192.168.77.0/24
Windows Host        192.168.77.1
Ubuntu Target       192.168.77.10
Kali Tester         192.168.77.20
```

同时记录本次验证过的版本化样本，注明“仅对该版本文件有效”：

```text
Ubuntu Server 26.04.1 amd64
SHA256 CC8A95CDE20F6CED61A322420DE00F10CC3C90CED545DAA46CB9C1A117F1D927

Kali Linux 2026.2 VMware amd64
SHA256 C65145CEF70166889E7283A230E88C832EAA8077E6E7CD37B47C0CCDC05685B0
```

课程必须教学习者“把自己下载文件的 hash 与官方当前版本发布值比较”，不能把上面两个旧版本 hash 当成未来版本通用值。

- [ ] **Step 4: 写入 Gate**

S00-L01 Gate 至少要求：

```text
1. Ubuntu/Kali/Host 在隔离实验网内按设计互通。
2. Ubuntu/Kali `ip route` 不存在 default route。
3. 直接 ping 8.8.8.8 失败，且能解释这是路由隔离而不是 DNS 问题。
4. 能说出 Host-Only 与 NAT 的核心差异。
5. Ubuntu/Kali 都创建 baseline snapshot。
6. 能说明为什么不能把真实 WLAN 网段直接当作安全实验 Scope。
7. checkpoint: s00-l01-complete-v2
```

- [ ] **Step 5: 运行结构测试**

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_course_structure.py -q
```
Expected: checkpoint/path 测试开始通过；如果 curriculum 顺序尚未改，第三个测试仍可失败，这是预期的中间状态。

- [ ] **Step 6: 提交 Lab 重构**

```powershell
git add labs/s00/l01-cyber-range labs/s00/l02-scope
git commit -m "docs: make Cyber Range the first S00 lab"
```

---

### Task 3: 同步课程总纲、规则与 legacy checkpoint 说明

**Files:**
- Create: `docs/CHECKPOINTS.md`
- Modify: `README.md`
- Modify: `CURRICULUM.md`
- Modify: `docs/CURRICULUM_DESIGN.md`
- Modify: `docs/LAB_RULES.md`
- Modify: `docs/superpowers/plans/2026-09-14-s00-s02-implementation.md`

**Interfaces:**
- Consumes: Task 2 的新 Lab 结构。
- Produces: 唯一一致的公开学习路线与 checkpoint 解释。

- [ ] **Step 1: 更新 S00 五课顺序**

统一为：

```text
S00-L01 Build Your Cyber Range
S00-L02 Authorization & Scope
S00-L03 Snapshot / Reset / Recovery
S00-L04 Workstation & Toolchain
S00-L05 Baseline Telemetry
```

原 `S00-L03 Host-Only / NAT / Routing` 的核心知识并入 L01，不再作为独立重复 Lab。

- [ ] **Step 2: 在课程设计规范写入顺序原则**

必须明确表达：

> 先创建真实、隔离、可恢复的实验资产，再基于实际实验资产定义 Scope。课程不得先虚构网段，再让学习者围绕不存在的资产做授权实验。

- [ ] **Step 3: 创建 checkpoint 兼容说明**

`docs/CHECKPOINTS.md` 至少记录：

```text
s00-l01-start       legacy：重构前 Scope starter
s00-l01-complete    legacy：重构前 Scope 完成态，不移动、不删除
s00-l01-complete-v2 新结构：Cyber Range 完成态
s00-l02-complete-v2 新结构：Scope 完成态
```

- [ ] **Step 4: 标记旧实施计划的 S00 编号已 superseded**

在 `docs/superpowers/plans/2026-09-14-s00-s02-implementation.md` 顶部增加清晰说明，指向本计划；不要删除旧计划，以保留课程设计历史。

- [ ] **Step 5: 运行结构和 Scope 测试**

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_course_structure.py tests\test_scope_policy.py tests\test_scope_cli.py -q
```
Expected: 全部 PASS。

- [ ] **Step 6: 提交课程文档同步**

```powershell
git add README.md CURRICULUM.md docs
git commit -m "docs: align S00 curriculum with real lab workflow"
```

---

### Task 4: 让 CI 覆盖完整课程回归测试

**Files:**
- Modify: `.github/workflows/ci.yml`

**Interfaces:**
- Consumes: 全部 pytest 测试。
- Produces: PR 合并前统一 CI Gate。

- [ ] **Step 1: 把 CI 测试命令改为完整 pytest**

将：

```yaml
- name: Run S00 scope tests
  run: python -m pytest tests/test_scope_policy.py tests/test_scope_cli.py -q
```

改为：

```yaml
- name: Run test suite
  run: python -m pytest -q
```

保留：

```yaml
cache: pip
cache-dependency-path: requirements-dev.txt
```

- [ ] **Step 2: 本地执行与 CI 等价的测试**

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```
Expected: 所有测试 PASS。

- [ ] **Step 3: 提交 CI 更新**

```powershell
git add .github/workflows/ci.yml
git commit -m "ci: run full course test suite"
```

---

### Task 5: 全量验证、PR、Merge 与 v2 checkpoint

**Files:**
- No new production files.
- Verify all modified files from Tasks 1-4.

**Interfaces:**
- Consumes: 完整重构分支。
- Produces: 通过 CI 的 main，以及语义正确的新 checkpoint tags。

- [ ] **Step 1: 最终本地验证**

```powershell
.\.venv\Scripts\python.exe -m pytest -q
git status --short
git diff origin/main...HEAD --check
```
Expected: pytest 全绿、工作区 clean、`git diff --check` 无错误。

- [ ] **Step 2: 搜索旧编号残留**

检查所有会误导学习者的 `S00-L01 Scope`、`l01-scope`、旧 S00-L02/L03/L04/L05 顺序引用。Legacy tag 文档中的历史记录允许保留，但必须带 `legacy` 说明。

- [ ] **Step 3: 推送分支并创建 PR**

```powershell
git push -u origin docs/s00-curriculum-restructure
```

PR base 必须为 `main`，正文写明：课程顺序重构、Cyber Range 真实复现、legacy tag 策略、pytest/CI 结果。

- [ ] **Step 4: 等待 GitHub Actions 成功**

只有 `Run test suite` 成功后才能 merge。

- [ ] **Step 5: 合并 PR 后同步本地 main 并再次测试**

```powershell
cd G:\AINmg\Codes\cybersec
git switch main
git pull --ff-only origin main
.\.venv\Scripts\python.exe -m pytest -q
```

Expected: 合并后的 main 全部测试 PASS。

- [ ] **Step 6: 创建新的无歧义 checkpoint**

在确认 merge commit 同时包含完整 L01/L02 课程内容后创建：

```powershell
git tag -a s00-l01-complete-v2 -m "S00-L01 Cyber Range complete after curriculum restructure"
git tag -a s00-l02-complete-v2 -m "S00-L02 Scope complete after curriculum restructure"
git push origin s00-l01-complete-v2 s00-l02-complete-v2
```

不得移动或删除：

```text
s00-l01-start
s00-l01-complete
```

---

## Acceptance Checklist

- [ ] 新学习者只看仓库即可完成 Ubuntu + Kali + Host-Only Cyber Range 搭建。
- [ ] 公共课程清楚区分“参考实现 `192.168.77.0/24`”与“学习者自己的实际实验网”。
- [ ] Cyber Range 是 S00-L01，Scope 是 S00-L02。
- [ ] S00 仍然保持 5 个核心 Lab，没有重复的独立 Host-Only Lab。
- [ ] Scope 安全策略保持 deny-by-default，无行为回退。
- [ ] legacy tags 未被重写。
- [ ] 新 v2 checkpoint 语义无歧义。
- [ ] GitHub Actions 运行完整 pytest 并通过。
- [ ] 合并后的 main 再次本地验证通过。
