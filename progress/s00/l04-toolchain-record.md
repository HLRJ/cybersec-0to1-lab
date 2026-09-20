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