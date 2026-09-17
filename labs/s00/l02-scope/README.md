# S00-L02：授权范围与实验规则

> 目标：在已有隔离实验资产的基础上，建立“授权范围”这个安全工程的第一条边界。
> 顺序说明：先完成 S00-L01，建立真实、隔离的实验资产，再根据你实际创建的 Host-Only 网段定义 Scope。仓库中的 `192.168.77.0/24` 是课程参考实现，不要求所有学习者使用同一网段。

## 你要学会什么

完成本课后，你应该能解释：

- Authorization 和 Scope 分别解决什么问题；
- 为什么“技术上能访问”不等于“有权测试”；
- 为什么安全工具更适合使用 allowlist；
- CIDR `192.168.77.0/24` 在本仓库参考实现的 scope 中代表什么；
- 为什么网络地址和广播地址不应作为普通主机目标。

## 本课文件

先阅读，不要急着改：

```text
scope/lab-scope.yaml
scripts/check_lab_target.py
tests/test_scope_policy.py
tests/test_scope_cli.py
docs/LAB_RULES.md
```

## Exercise 1：先预测，再运行

不要先看测试答案。先写下你对下面 6 个目标的预测：`ALLOW` 还是 `DENY`，以及为什么。

1. `127.0.0.1`
2. `192.168.77.42`
3. `192.168.77.0`
4. `192.168.77.255`
5. `192.168.1.20`
6. `8.8.8.8`

## Exercise 2：亲手运行

在本课 worktree 根目录运行：

```powershell
.\.venv\Scripts\python.exe scripts\check_lab_target.py 127.0.0.1
.\.venv\Scripts\python.exe scripts\check_lab_target.py 192.168.77.42
.\.venv\Scripts\python.exe scripts\check_lab_target.py 192.168.77.0
.\.venv\Scripts\python.exe scripts\check_lab_target.py 192.168.77.255
.\.venv\Scripts\python.exe scripts\check_lab_target.py 192.168.1.20
.\.venv\Scripts\python.exe scripts\check_lab_target.py 8.8.8.8
```

注意：`DENY` 返回退出码 `2` 是设计行为，不表示脚本崩溃。

再运行自动化测试：

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_scope_policy.py tests\test_scope_cli.py -q
```

## Exercise 3：读代码

打开 `scripts/check_lab_target.py`，找到并解释：

- `ip_network(..., strict=True)`；
- `ip_address(target)`；
- `address in network`；
- `network.network_address`；
- `network.broadcast_address`。

## Exercise 4：修改范围并验证

先不要直接改。预测：如果把 `scope/lab-scope.yaml` 中的 `192.168.77.0/24` 改成 `192.168.99.0/24`，哪些测试会失败？为什么？

然后再修改、运行测试、观察失败，并把配置恢复回来。恢复后测试应重新通过。

## Gate：你需要向我反馈什么

请把以下内容发给我：

1. 6 个目标的 `ALLOW/DENY` 预测与实际结果；
2. 你对 `/24` 的理解；
3. 为什么 `192.168.77.0` 和 `192.168.77.255` 被拒绝；
4. 修改为 `192.168.99.0/24` 后，哪些测试失败；
5. 你认为“只禁止公网”与“只允许明确实验网段”哪种策略更安全，为什么。

不要求第一次全部答对。你的错误和疑问会用于改进课程。

## 通关标准

你能够独立说明授权、scope、allowlist、CIDR 和目标校验之间的关系，并能通过修改配置预测测试行为，本课才算完成。

完成后才创建：`s00-l02-complete-v2`。
