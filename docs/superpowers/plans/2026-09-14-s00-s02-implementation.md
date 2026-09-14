# S00–S02 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把已批准的中文课程设计落成一个可运行、可测试、可复现的 S00–S02 学习仓库，为 S03 安全漏洞课程建立可靠地基。

**Architecture:** 先实现安全实验边界和环境检查，再通过最小 Python 程序与抓包完成 Socket/TCP/DNS/HTTP/TLS 学习，最后构建正常版 MiniCorp v0。S00–S02 不故意埋漏洞；所有后续安全实验都建立在可恢复、可观察、可测试的基线上。

**Tech Stack:** Windows 11、Python 3.12+、pytest、VMware Workstation、Wireshark、Burp Suite、FastAPI、SQLAlchemy、SQLite、Git/GitHub。

**Spec:** `CURRICULUM.md`、`docs/CURRICULUM_DESIGN.md`

## Global Constraints

- Core Curriculum 完成前只维护中文版；技术标识保持英文原样。
- 攻击性实验只允许明确授权的本地/隔离目标。
- S00–S02 不为了演示效果提前引入故意漏洞。
- 每个 Lab 必须有证据、Gate 和稳定 Git checkpoint。
- 教学代码优先小而清晰；先原理，后工具。
- 每个实现任务完成后运行相关测试并提交小粒度 commit。

---

### Task 1: 仓库基线与课程治理

**Files:** `README.md`、`CURRICULUM.md`、`docs/CURRICULUM_DESIGN.md`、`SECURITY.md`、`CONTRIBUTING.md`、`.editorconfig`、`.gitattributes`、`.gitignore`

- [x] 固化中文课程总纲与设计规范。
- [x] 固化授权边界、贡献规则和 UTF-8/LF 文本策略。
- [x] 创建实施计划并完成首个公开仓库基线提交。
- [ ] 后续新增 Markdown/链接检查 CI，不在基线提交中假装存在运行中的课程代码。

### Task 2: S00 安全实验室

**Files:** `scope/`、`scripts/env_check.py`、`scripts/check_lab_target.py`、`docs/network/`、`progress/s00/`、`artifacts/`

- [ ] 先为 scope 解析和目标拒绝逻辑写失败测试。
- [ ] 实现 `lab-scope.yaml` 与仅接受实验目标的校验器。
- [ ] 实现环境版本检查，保存可复现工具基线。
- [ ] 完成 VMware Host-Only/NAT 拓扑、Snapshot/Reset 和 Telemetry Lab 文档。
- [ ] 通过 S00 Boss：隔离、通信、证据保存和恢复均可证明。
- [ ] 创建 `s00-l01-complete` 至 `s00-boss-complete` checkpoint。

### Task 3: S01 协议与网络原理

**Files:** `labs/s01/`、`scripts/tcp_probe.py`、`scripts/subnet_explain.py`、`progress/s01/`

- [ ] 用测试驱动实现最小 TCP client/server。
- [ ] 完成 TCP 状态机、路由/NAT、DNS、HTTP from scratch、TLS 六个 Lab。
- [ ] 每课保存对应 PCAP/结构化证据说明，不提交含敏感数据的真实抓包。
- [ ] HTTP Lab 必须将网络字节追到 parser 变量；TLS Lab 必须解释 CA 与 Burp 代理信任链。
- [ ] 通过 Unknown Service Boss，禁止只用扫描结果替代协议解释。
- [ ] 创建 S01 全部 checkpoint。

### Task 4: S02 MiniCorp v0

**Files:** `minicorp/app/`、`minicorp/tests/`、`progress/s02/`

- [ ] 建立 FastAPI 最小应用与 `/health` 测试。
- [ ] 加入 SQLAlchemy/SQLite、User/Order、Session/Transaction/Repository 测试。
- [ ] 加入注册、登录、登出、当前用户与密码哈希测试。
- [ ] 加入 owner/role 授权模型，并对匿名/普通用户/所有者/管理员做决策测试。
- [ ] 加入结构化日志、request id、审计事件和敏感信息不落日志测试。
- [ ] 通过 S02 Boss：能完整追踪 HTTP → Middleware → Router → Service → Repository → Database。
- [ ] 创建 S02 全部 checkpoint；通过后才允许进入 S03。

### Task 5: CI 与阶段验收

**Files:** `.github/workflows/`、`tests/`、课程文档

- [ ] 增加基础 Python 测试 CI 与 Markdown/链接检查。
- [ ] 增加实验目标安全边界测试，确保公网地址默认拒绝。
- [ ] 确认 Windows 本地与 GitHub Actions 上的测试入口一致。
- [ ] 每个 Stage Boss 通过后更新 README 进度，而不是预先标记完成。

## 实施顺序

严格按 `Task 1 → S00 → S01 → S02 → CI/阶段验收` 推进。任何阶段如果 Gate 未通过，不提前进入下一 Stage，也不为了“看起来内容多”批量创建空 Lab。
