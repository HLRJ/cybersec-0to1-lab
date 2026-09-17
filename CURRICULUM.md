# 网络安全攻防 0→1 实战 Lab — 课程总纲

> **构建它 → 攻破它 → 追踪它 → 修复它 → 检测它 → 再验证它。**

课程状态：v0.2 中文主版本  
当前范围：10 个 Stage / 58 个核心 Lab；S00、S01、S02 已细化到可实施粒度。  
语言策略：核心课程完成前只维护中文版；代码、命令、协议字段、API、函数名保持英文原样。

## 1. 课程使命

这不是 Kali 命令合集、漏洞百科、CTF 题库或考证速记。第一目标是让课程维护者自己沿着一个持续演化的真实工程，把网络安全从协议、代码、操作系统一路学到企业攻防；第二目标才是让其他学习者 clone 仓库后沿同样的 checkpoint、实验代码、抓包、日志和测试复现学习路线。

贯穿课程的统一闭环：

```text
RUN → OBSERVE → BUILD → BREAK → TRACE → SOURCE DIVE
    → ROOT CAUSE → FIX → DETECT → TEST → VERIFY → REFLECT
```

每个核心 Lab 至少回答：发生了什么、为什么发生、哪一层代码/协议/权限导致、留下什么证据、为什么修复有效、如何证明不会回归。

## 2. 安全与授权边界

所有攻击性实验只允许针对：
1. 仓库明确提供的实验目标；
2. 学习者自己拥有并明确用于实验的环境；
3. 获得明确书面授权的目标。

默认实验网建议使用隔离虚拟网络，例如 `192.168.77.0/24`。后续主动探测和漏洞验证工具必须设计为默认拒绝意外公网目标。

> 如果不能明确说明为什么自己有权测试这个目标，它就不属于课程授权范围。

## 3. 代码深度分级

| 等级 | 名称 | 要求 |
|---|---|---|
| C1 | Read | 能定位并解释相关代码或配置 |
| C2 | Trace | 能跨组件追踪数据流、控制流或权限流 |
| C3 | Implement | 能自己实现关键机制、漏洞版或安全版 |
| C4 | Internals | 能继续追到协议、运行时、驱动或 OS 机制 |

课程不会把“会用工具”当作深度。工具必须建立在原理和代码理解之后。

## 4. 核心路线：10 Stage / 58 Lab

| Stage | 主题 | Lab 数 | 主深度 |
|---|---|---:|---|
| S00 | 建立安全实验室 | 5 | C1–C2 |
| S01 | 从数据包到进程 | 6 | C2–C4 |
| S02 | 先构建，再攻击 | 5 | C2–C3 |
| S03 | 攻破服务器端 | 9 | C2–C4 |
| S04 | 攻破浏览器端 | 5 | C2–C4 |
| S05 | 像攻击者一样读代码 | 6 | C3–C4 |
| S06 | 理解并突破主机边界 | 6 | C2–C4 |
| S07 | 企业网络与 Active Directory | 6 | C3–C4 |
| S08 | 看见攻击：检测与紫队 | 6 | C2–C4 |
| S09 | 最终综合 Cyber Range | 4 | 综合 |

### S03 — 服务器端安全

Broken Access Control、SQL Injection、Path Traversal、File Upload、Command Injection、SSRF、Authentication & Session、API/JWT、Business Logic & Race Conditions。

### S04 — 浏览器端安全

Same-Origin Policy、XSS、CSRF/SameSite、CORS/postMessage、OAuth/WebSocket/UI Trust。

### S05 — AppSec 与代码审计

Source→Propagation→Sink、Call Graph/Control Flow、Secure Coding、Semgrep/CodeQL、Dependency/Secret/SBOM/SCA、Threat Modeling + ASVS。

### S06 — 主机安全

Linux 用户/权限/进程、sudo/capability/service/cron、Linux 日志与加固、Windows SID/Token/ACL/Integrity、Service/Registry/Task/PowerShell、Event Log/Sysmon。

### S07 — 企业网络与 AD

AD/LDAP/DNS/GPO、Kerberos、NTLM/SMB、ACL/Delegation/Service Account、Attack Path/BloodHound、企业身份综合 Lab。

### S08 — 检测与紫队

Telemetry Engineering、Windows Event/Sysmon、Zeek/Suricata、Sigma/Detection-as-Code、Incident Timeline、Purple Team Validation。

### S09 — 最终 Cyber Range

Recon + 架构还原、Security Assessment + Attack Path、Code Fix + Hardening + Detection、Incident Investigation + Final Report。

---
# 5. S00 — 建立安全实验室

阶段目标：建立一个**合法、隔离、可恢复、可观察**的实验环境。后续任何安全实验都必须可重复、可回滚、有证据。

## S00-L01 — 授权范围与实验规则

**深度：C1**

学什么：Authorization、Scope、Rules of Engagement；资产、账号、时间窗口、允许动作、禁止动作；证据保存与敏感信息边界。

写什么：
- `scope/lab-scope.yaml`：明确允许网段、禁止公网目标、实验所有者、恢复方式；
- `docs/LAB_RULES.md`：课程安全规则。

做什么实验：
- 给出 6 个目标案例，判断哪些可测、哪些必须拒绝；
- 修改 scope 后验证边界变化。

通关：
- 能解释“技术上能做”和“被授权做”的区别；
- 能写出一份清晰、可执行的测试范围；
- checkpoint：`s00-l01-complete`。

## S00-L02 — 安全工作站与工具链

**深度：C1**

学什么：Git、Python、Wireshark、Burp、VMware、终端与证据目录的角色。

写什么：
- `scripts/env_check.py`：检查 Python、Git、常用工具是否存在并输出版本；
- `artifacts/.gitkeep`：统一证据目录。

实验：在 Windows 主机运行环境检查并保存一次工具版本基线。

通关：能说明每个工具解决什么问题；`python scripts/env_check.py` 可重复执行；checkpoint：`s00-l02-complete`。

## S00-L03 — 隔离网络：Host-Only / NAT / Routing

**深度：C2**

学什么：IP、子网、默认网关、Host-Only、NAT、路由、DNS 的边界。

写什么：
- `docs/network/lab-topology.md`；
- `scripts/check_lab_target.py`：第一版只接受配置的实验网段。

实验：
- 主机、Kali、Ubuntu 在隔离网互通；
- 比较 Host-Only 与 NAT 的路径差异；
- 验证公网 IP 被目标检查脚本拒绝。

通关：能画出数据包从主机到 VM 的路径；能解释为什么实验网与公司/公网环境隔离；checkpoint：`s00-l03-complete`。

## S00-L04 — Snapshot / Reset / Reproduce

**深度：C1**

学什么：可重复实验、快照、基线、恢复点、变更记录。

写什么：
- `docs/RESET_GUIDE.md`；
- `progress/s00/l04-reset-record.md`。

实验：建立 Ubuntu 基线快照；故意改坏配置；恢复快照并验证服务状态回到基线。

通关：同一实验可重复三次得到一致结果；checkpoint：`s00-l04-complete`。

## S00-L05 — Baseline Telemetry

**深度：C2**

学什么：网络流量、应用日志、系统日志、时间线与 correlation。

写什么：
- `scripts/demo_service.py`：最小本地 HTTP 服务；
- `progress/s00/l05-telemetry-map.md`。

实验：正常访问服务；保存 PCAP、应用日志和系统侧连接信息；用时间戳把一次正常请求关联起来。

通关：能从“一个请求”指出至少三个可观测位置；checkpoint：`s00-l05-complete`。

### S00 Boss — Build the Range

交付：scope、拓扑图、两台实验 VM、基线 PCAP/日志、Snapshot/Reset 流程。

Gate：证明环境隔离、通信正常、证据可保存、快照可恢复。

---
# 6. S01 — 从数据包到进程

阶段目标：不先背 OSI 七层，从自己写进程和 Socket 开始，把网络行为一直追到 TCP、DNS、HTTP 与 TLS。

## S01-L01 — Process → Socket → Port

**深度：C3**

学什么：进程、socket、bind、listen、accept、connect、IP:Port。

写什么：
- `labs/s01/l01-socket/src/server.py`；
- `labs/s01/l01-socket/src/client.py`；
- 对应 pytest。

实验：client/server 本机通信；改监听地址比较 `127.0.0.1` 与 `0.0.0.0`；用 `netstat`/`ss` 观察监听状态。

通关：能从进程解释到端口；能说明端口不是“程序名字”；checkpoint：`s01-l01-complete`。

## S01-L02 — TCP 状态机与 Wireshark

**深度：C4**

学什么：SYN/SYN-ACK/ACK、FIN、RST、sequence/ack number、重传。

写什么：`scripts/tcp_probe.py`，仅针对实验地址进行连接探测；`progress/s01/l02-tcp-trace.md`。

实验：抓三次握手和正常关闭；访问未监听端口观察 RST；对比应用成功与连接失败。

通关：能用 PCAP 解释为什么一个端口表现为 open/closed；checkpoint：`s01-l02-complete`。

## S01-L03 — IP / Subnet / Routing / NAT

**深度：C3**

学什么：CIDR、ARP、路由表、默认网关、NAT。

写什么：`scripts/subnet_explain.py`，输入 CIDR 输出网络地址、主机范围、广播地址；`progress/s01/l03-route-map.md`。

实验：修改 VM 网络参数；比较同网段通信与经网关通信；观察 NAT 前后的地址。

通关：能仅根据地址和路由表解释数据包下一跳；checkpoint：`s01-l03-complete`。

## S01-L04 — DNS

**深度：C3**

学什么：resolver、A/AAAA/CNAME、递归、缓存、DNS 报文。

写什么：`labs/s01/l04-dns/src/dns_query.py`，构造/解析最小 DNS 查询；测试固定样例报文。

实验：`nslookup`/`dig` 与自写脚本对比；Wireshark 观察 Query/Response。

通关：能从域名解释到最终 IP，并指出本机 resolver 角色；checkpoint：`s01-l04-complete`。

## S01-L05 — HTTP from Scratch

**深度：C4**

学什么：request line、headers、body、status line、Content-Length、connection。

写什么：
- `labs/s01/l05-http-from-scratch/src/server.py`：仅用标准库处理最小 GET；
- `labs/s01/l05-http-from-scratch/src/parser.py`：解析 request line 与 headers；
- 对应单元测试。

实验：浏览器、`curl`、原始 socket 三种方式访问同一服务；抓包对照字节流与程序变量。

通关：能把一个 HTTP 请求从网络字节映射到 parser 中的变量；能解释 `Content-Length`、连接关闭与响应边界；checkpoint：`s01-l05-complete`。

## S01-L06 — TLS / CA / HTTPS / Burp 原理

**深度：C4**

学什么：TLS 位于 HTTP 与 TCP 之间的作用；证书、公钥、私钥、CA、证书链、hostname verification；为什么代理导入本地 CA 后可以观察 HTTPS。

写什么：
- `labs/s01/l06-tls/src/https_server.py`：本地自签名 HTTPS 服务；
- `progress/s01/l06-certificate-chain.md`：证书链与信任关系图。

实验：访问自签名站点观察证书告警；导入仅供实验使用的本地 CA；用 Burp 观察本地 HTTPS 请求；Wireshark 对比明文 HTTP 与 TLS 流量。

通关：能解释“HTTPS 并不是 HTTP 消失了，而是 HTTP 运行在 TLS 之上”；能解释 Burp 的 TLS 终止与重新建立；checkpoint：`s01-l06-complete`。

### S01 Boss — Unknown Service

只提供一个实验 IP。要求判断主机是否可达、开放端口、服务类型、协议证据与网络路径，并用 PCAP 解释至少一个判断。

Gate：不能只贴扫描结果；必须解释工具如何依据协议响应得出结论。

---
# 7. S02 — 先构建，再攻击

阶段目标：先构建一个正常、可测试、可观察的 MiniCorp v0。S02 不为了“有靶场”而提前埋漏洞；只有理解请求生命周期、数据访问、身份、授权与日志之后，S03 才开始系统性引入安全缺陷。

初始架构：

```text
Browser
  ↓
FastAPI
  ↓
Service
  ↓
Repository
  ↓
SQLAlchemy
  ↓
SQLite
```

## S02-L01 — FastAPI Request Lifecycle

**深度：C3**

学什么：ASGI、Middleware、Router、Dependency、Service、Response Model；一个请求在应用中的调用链。

写什么：
- `minicorp/app/main.py`；
- `minicorp/app/api/health.py`；
- `minicorp/app/core/request_id.py`；
- `minicorp/tests/test_health.py`。

实验：对 `/health` 设置断点，从 middleware 跟到 route；记录 request id；用测试客户端重放请求。

通关：能画出 HTTP 请求进入 FastAPI 后的调用链，并能在代码中指出每一步；checkpoint：`s02-l01-complete`。

## S02-L02 — Database & ORM

**深度：C3**

学什么：ORM、Session、Transaction、Repository、模型与持久化边界。

写什么：User/Order 最小模型、数据库 session、repository 和 CRUD 测试。

实验：建立测试数据库；创建用户和订单；故意触发事务回滚；比较 ORM 对象、SQL 与数据库状态。

通关：能解释 Session 生命周期和事务边界；能追踪一次 API 写操作到 SQL；checkpoint：`s02-l02-complete`。

## S02-L03 — Identity：密码、Cookie、Session、JWT

**深度：C3**

学什么：password hashing、salt、session id、cookie 属性、token 的身份表示；认证与身份生命周期。

写什么：注册、登录、登出、当前用户接口；密码哈希与认证测试。

实验：观察登录前后 Cookie/Token 变化；重启服务后验证不同身份方案的状态差异。

通关：能解释密码为何不能明文保存，能区分 Session 与 JWT 的状态模型；checkpoint：`s02-l03-complete`。

## S02-L04 — Authorization：角色、资源与权限

**深度：C3**

学什么：Authentication 与 Authorization 的区别；subject/resource/action；owner、role、policy。

写什么：普通用户与管理员最小权限模型；资源 owner 检查；授权单元测试。

实验：分别以匿名、普通用户、资源所有者、管理员访问同一资源，记录决策结果。

通关：能把权限判断从业务代码中明确定位出来；能解释“已登录”为什么不等于“有权访问”；checkpoint：`s02-l04-complete`。

## S02-L05 — Logging & Security Testing Baseline

**深度：C3**

学什么：结构化日志、request id、审计日志、敏感信息脱敏、pytest、安全回归测试思路。

写什么：统一日志配置、审计事件模型、基础 API 测试、日志测试。

实验：执行注册、登录、授权成功/失败请求；用 request id 把 HTTP 请求与应用日志关联；确认密码/Token 不进入日志。

通关：正常功能有测试；关键安全决策有日志；日志不泄露敏感信息；checkpoint：`s02-l05-complete`。

### S02 Boss — Explain MiniCorp Before Breaking It

交付：MiniCorp v0、架构图、数据流图、Trust Boundary、身份与授权模型、日志地图、测试结果。

Gate：随机选择一次请求，学习者必须从 HTTP → Middleware → Router → Service → Repository → Database 完整追踪；能指出认证、授权、日志和事务分别发生在哪里。通过后才进入 S03。

---

# 8. 后续阶段与外部训练

核心 Lab 负责“原理 + 代码 + 攻击/失效 + 修复 + 检测 + 回归”；成熟外部平台负责陌生环境迁移和额外题量。后续可按课程主题链接 PortSwigger Web Security Academy、pwn.college、SEED Labs、PentesterLab、TryHackMe、HTB Academy，但不复制其受版权保护的题目、答案或课程文本。

# 9. Advanced Tracks

Core 毕业后再增加：Web Deep、Binary/Reverse Engineering、Fuzzing/Vulnerability Research、Cloud/Container/Kubernetes、Software Supply Chain/DevSecOps、AI/LLM/Agent Security。

这些方向不阻塞 Core 0→1 主线。
