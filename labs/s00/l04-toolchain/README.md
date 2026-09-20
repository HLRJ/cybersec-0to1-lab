# S00-L04：Workstation & Toolchain

> 目标：建立一套能重复验证的 Windows 安全学习工作站，而不是靠“我记得这个软件装过”。

## 本课要学什么

后续课程会同时使用宿主机、Kali、Ubuntu 与浏览器工具。L04 先把宿主机工具链变成可观察、可重复检查的基础设施。

本课关注这些角色：

- Git：课程版本控制、checkpoint、diff 与恢复；
- Python：课程脚本、协议实验和自动化测试；
- PowerShell / Terminal：Windows 宿主机主要操作入口；
- OpenSSH：从 Windows 管理实验 VM；
- Wireshark / TShark：后续抓包、协议观察与证据保存；
- Burp Suite：后续 Web 代理、请求重放与调试；
- VMware Workstation：承载隔离 Cyber Range；
- VS Code：可选的代码/文档编辑入口。

## 安全边界

- 本课只检查本机工具，不扫描任何网络目标。
- `env_check.py` 只读，不安装、不升级、不修改系统配置。
- 某工具缺失不等于 Gate 失败；先确认课程真正需要，再决定是否安装。
## 第一轮：OBSERVE — 让机器自己报告工具链

在 Windows PowerShell 中进入仓库：

```powershell
cd G:\AINmg\Codes\cybersec\.worktrees\s00-l04-toolchain
python scripts\env_check.py
```

脚本会输出每个工具的：

```text
STATUS | TOOL | VERSION / LOCATION / NOTE
```

其中：

- `OK`：找到并成功获取版本或位置；
- `MISSING`：当前 PATH / 常见安装位置没有找到；
- `WARN`：找到了候选，但版本检测不完整。

### 第一轮停止点

运行后把完整输出发回来。

先不要为了让结果“全绿”而安装软件。我们会根据真实结果判断哪些已经满足要求、哪些只是 PATH 问题、哪些确实缺失、哪些应该延迟安装。

最终 checkpoint：`s00-l04-complete-v2`。
## 第一轮真实发现：MISSING 不等于未安装

第一次实跑中，checker 把 VMware Workstation 和 Wireshark 都报告为 `MISSING`，但随后只读检查 Windows 安装注册表发现二者实际已经安装在 `D:` 盘自定义目录。

这说明工具检测需要分层：

```text
PATH
→ 常见安装位置
→ Windows uninstall registry
→ 仍未发现才标记为 MISSING
```

课程因此升级 `env_check.py`：Windows 下会继续读取卸载注册表，但仍保持只读。

这也是 L04 的一个核心知识点：**CLI 不在 PATH、GUI 安装在自定义目录、真正未安装，是三种不同状态。**