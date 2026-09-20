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
## 第二轮结论：工具链不是“全装齐才算通过”

修正后的真实环境中，Python、Git、PowerShell、OpenSSH、curl、Wireshark、VMware Workstation 与 VS Code 均可确认存在。

Burp Suite 暂未安装。本课程不为了让检查结果全绿而提前安装它；Burp 将在真正进入 Web 代理与请求重放实验前再安装和验证。

因此工具链健康检查需要区分：

```text
Required now   → 当前阶段必须可用
Deferred       → 后续课程需要时再安装
Missing        → 当前阶段必需但确实不存在
```

Burp 在 S00-L04 中属于 `Deferred`，不阻塞本课 Gate。
## 第三轮：Tool → Role → Evidence

仅仅看到版本号还不够。本轮要让关键工具完成一次最小职责验证。

### Git：证明仓库状态可追踪

```powershell
git status --short --branch
git log -1 --oneline
```

### Python：证明课程测试环境可执行

```powershell
python -m pytest -q
```

### OpenSSH：证明宿主机能管理实验 VM

```powershell
ssh cyberlab@192.168.77.10 "hostname; ip -brief address; systemctl is-active ssh"
```

### Wireshark / TShark：证明抓包引擎可调用

```powershell
& 'D:\Program Files\Wireshark\tshark.exe' --version
& 'D:\Program Files\Wireshark\tshark.exe' -D
```

这里只列出本机 capture interfaces，不开始抓包。

### VMware Workstation：证明虚拟化平台版本可追踪

```powershell
(Get-ItemProperty 'HKLM:\SOFTWARE\WOW6432Node\VMware, Inc.\VMware Workstation').ProductVersion
```

### 本轮停止点

把以上命令的完整输出发回来。重点不是全绿，而是能解释每个工具在后续课程里承担什么职责。

Burp Suite 当前保持 `DEFERRED`，不参与这一轮 Gate。
## 第三轮真实故障：Python 可用，不代表项目环境可用

第一次执行 `python -m pytest -q` 时，系统默认 Python 是 Miniconda Python 3.13.2，但其全局 `site-packages` 中存在旧版 `pyreadline 2.1`。

pytest 初始化时因此触发：

```text
AttributeError: module 'collections' has no attribute 'Callable'
```

这说明工具链还需要区分两层：

```text
Python Runtime        → python.exe 能不能运行
Project Environment  → 项目依赖是否隔离、可重复
```

课程不通过“卸掉全局坏包”来掩盖问题，而是建立仓库自己的 `.venv`。这样不会破坏其他 Conda 项目，也更接近 CI 的可重复环境。

### 下一步：建立 repo-local venv

不要使用 `--system-site-packages`。虚拟环境必须与全局 `pyreadline` 隔离。
## Project Environment Gate：通过

真实修复采用 repo-local `.venv`，没有修改全局 Miniconda 包。

验证结果：

```text
Runtime:       Python 3.13.2
pytest:        9.1.1
PyYAML:        6.0.3
global leak:   pyreadline 未进入项目 venv
test suite:    17 passed
```

因此本课程后续在 Windows 本地执行 Python 测试时，优先使用：

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

而不是假设全局 `python -m pytest` 一定可靠。

`.venv/` 已被 `.gitignore` 忽略，不进入版本控制。