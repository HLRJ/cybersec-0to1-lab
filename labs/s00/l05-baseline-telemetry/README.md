# S00-L05：Baseline Telemetry

> 目标：先知道“正常时发生了什么”，以后才能判断“异常从哪里出现”。

## 本课要学什么

同一次正常 HTTP 请求，会在不同观察层留下不同证据：

```text
Process / Socket
      ↓
Network Packet
      ↓
HTTP Request / Response
      ↓
Application Log
      ↓
Timestamp / Request ID Correlation
```

本课不引入漏洞，也不做攻击。只在已授权的 `127.0.0.0/8` 与 `192.168.77.0/24` 内建立正常行为基线。

## 第一轮：OBSERVE — 先记录服务启动前的基线

这一轮**不要运行 `scripts/demo_service.py`，不要开始抓包**。先证明服务启动前系统是什么状态。
### Step 1：Windows 时间与 VMnet2

```powershell
Get-Date -Format o

Get-NetIPAddress `
  -InterfaceAlias 'VMware Network Adapter VMnet2' `
  -AddressFamily IPv4 |
  Select-Object InterfaceAlias,IPAddress,PrefixLength

& 'D:\Program Files\Wireshark\tshark.exe' -D | Select-String 'VMnet2'
```

这里再次按接口名称识别 VMnet2，不依赖上节课临时出现的接口编号。

### Step 2：确认 demo 端口启动前没有监听

```powershell
Get-NetTCPConnection -State Listen -LocalPort 8000 -ErrorAction SilentlyContinue
```

如果没有输出，记录为：

```text
BASELINE_PORT_8000=NOT_LISTENING
```
### Step 3：记录 Windows 当前监听面

```powershell
Get-NetTCPConnection -State Listen |
  Where-Object {
    $_.LocalAddress -in @('0.0.0.0','::','127.0.0.1','192.168.77.1')
  } |
  Sort-Object LocalAddress,LocalPort |
  Select-Object LocalAddress,LocalPort,OwningProcess
```

这一份输出是 observation，不代表这些监听端口都属于课程资产。

### Step 4：记录 Ubuntu 基线与时间

```powershell
ssh cyberlab@192.168.77.10 "date --iso-8601=seconds; hostname; ip -brief address; ip route; ss -lntp"
```

重点观察：

- Windows 和 Ubuntu 各自的时间与时区偏移；
- Ubuntu 是否仍为 `192.168.77.10/24`；
- 是否仍然没有 Internet default route；
- SSH 是否仍在监听；
- 当前有哪些其他 TCP listener。

### 第一轮停止点

把以上完整输出发回来。我们先解释 baseline，再启动最小 HTTP 服务。

最终 checkpoint：`s00-l05-complete-v2`。