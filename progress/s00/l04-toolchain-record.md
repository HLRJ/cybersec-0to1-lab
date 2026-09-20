# S00-L04 Toolchain Record

## Round 1 — Windows Workstation Inventory

日期：

执行命令：

```powershell
python scripts\env_check.py
```

完整输出：

```text
等待学习者第一次真实运行。
```

## 待分析

- 已满足课程要求的工具：
- 仅 PATH / 位置问题：
- 确实缺失的工具：
- 可以延迟安装的工具：
- 版本兼容性问题：
## Round 1 — 实际结果

学习者第一次运行输出：

```text
OK       Python               Python 3.13.2 | D:\NewProgramFiles\Miniconda\python.EXE
OK       Git                  git version 2.50.1.windows.1 | C:\Program Files\Git\cmd\git.EXE
OK       PowerShell           5.1.19041.6456 | C:\Windows\System32\WindowsPowerShell\v1.0\powershell.EXE
OK       OpenSSH              OpenSSH_for_Windows_9.5p1, LibreSSL 3.8.2 | C:\Windows\System32\OpenSSH\ssh.EXE
OK       curl                 curl 8.13.0 ... | C:\Windows\system32\curl.exe
MISSING  Wireshark            not found
MISSING  VMware Workstation   not found
MISSING  Burp Suite           not found
OK       VS Code              1.138.0 | D:\program files\Microsoft VS Code\bin\code.CMD
```

随后只读核查 Windows 卸载注册表，发现：

```text
VMware Workstation 17.6.0
D:\Program Files (x86)\VMware\VMware Workstation\

Wireshark 4.4.0 x64
D:\Program Files\Wireshark
```

结论：VMware 与 Wireshark 是第一版 checker 的假阴性；二者已安装，但 CLI 不在 PATH 且使用了自定义安装盘。Burp Suite 暂未在 PATH、常见目录或卸载注册表中发现。
## Round 2 — 修正后的真实结果

升级为 PATH + 常见路径 + Windows uninstall registry 后，学习者再次运行：

```text
OK       Python               Python 3.13.2
OK       Git                  git version 2.50.1.windows.1
OK       PowerShell           5.1.19041.6456
OK       OpenSSH              OpenSSH_for_Windows_9.5p1, LibreSSL 3.8.2
OK       curl                 curl 8.13.0
OK       Wireshark            Wireshark 4.4.0 x64 | detected via registry
OK       VMware Workstation   VMware Workstation 17.6.0 | detected via registry
MISSING  Burp Suite           not found
OK       VS Code              1.138.0
```

结论：

- VMware 与 Wireshark 的检测假阴性已经修复；
- OpenSSH 在学习者真实 PowerShell 中版本检测正常；
- Burp Suite 目前确实未发现，但它不是 S00-L04 的当前必需工具；
- Burp 延迟到 Web 安全课程真正需要代理/重放 HTTP 请求时再安装。
## Round 3 — Tool → Role → Evidence

等待学习者执行：

```text
Git evidence:

Python evidence:

SSH evidence:

TShark evidence:

VMware evidence:
```
## Round 3 — Python 环境故障

执行 `python -m pytest -q` 时，工具链验证没有通过。当前 `python` 解析到：

```text
D:\NewProgramFiles\Miniconda\python.exe
Python 3.13.2
```

全局环境中同时存在：

```text
pytest 9.1.1
pyreadline 2.1
```

pytest 初始化 capture 时导入 `readline`，最终进入旧版 `pyreadline` 并触发：

```text
AttributeError: module 'collections' has no attribute 'Callable'
```

只读检查还发现本机有 Python 3.11 与 3.9。仓库 `.gitignore` 已忽略 `.venv/`。

### Root Cause

这不是课程测试本身失败，而是全局 Miniconda 环境被一个与现代 Python 不兼容的 `pyreadline 2.1` 污染。

### 决策

不卸载用户全局包。课程采用 repo-local `.venv` 隔离开发依赖，并用虚拟环境内的 Python 运行 pytest。
## Round 4 — Repo-local venv Recovery

学习者没有修改全局 Miniconda 环境，而是在仓库 worktree 中创建：

```text
.venv/
```

执行：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m pip list
.\.venv\Scripts\python.exe -m pytest -q
```

实际结果：

```text
Python 3.13.2
pytest 9.1.1
PyYAML 6.0.3
pyreadline: not installed in project venv
17 passed in 0.69s
```

结论：项目环境与全局 Miniconda `site-packages` 成功隔离；无需卸载用户全局 `pyreadline` 即可恢复课程测试。

pip 提示自身存在新版本，但当前依赖安装与测试均成功，因此本课不为追求最新版本而升级 pip。