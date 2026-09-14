from __future__ import annotations

from dataclasses import dataclass
from ipaddress import IPv4Network, IPv6Network, ip_address, ip_network
from pathlib import Path
from typing import Iterable

import yaml


Network = IPv4Network | IPv6Network


@dataclass(frozen=True)
class TargetDecision:
    allowed: bool
    reason: str


def load_allowed_networks(path: Path) -> list[Network]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    raw_networks = data.get("allowed_networks")
    if not isinstance(raw_networks, list) or not raw_networks:
        raise ValueError("scope 文件必须包含非空 allowed_networks 列表")
    return [ip_network(str(item), strict=True) for item in raw_networks]


def evaluate_target(target: str, allowed_networks: Iterable[Network]) -> TargetDecision:
    try:
        address = ip_address(target)
    except ValueError:
        return TargetDecision(False, "第一版目标校验只接受 IP 地址，不解析主机名或 URL")

    for network in allowed_networks:
        if address.version != network.version or address not in network:
            continue
        if address == network.network_address:
            return TargetDecision(False, f"{address} 是实验网段 {network} 的网络地址")
        if isinstance(network, IPv4Network) and address == network.broadcast_address:
            return TargetDecision(False, f"{address} 是实验网段 {network} 的广播地址")
        return TargetDecision(True, f"{address} 位于允许的实验网段 {network}")

    return TargetDecision(False, f"{address} 不在允许的实验网段中")


def _use_utf8_output() -> None:
    import sys

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    import argparse

    _use_utf8_output()
    parser = argparse.ArgumentParser(description="检查目标是否位于课程允许的实验网段")
    parser.add_argument("target", help="目标 IP 地址")
    parser.add_argument("--scope", type=Path, default=Path("scope/lab-scope.yaml"))
    args = parser.parse_args(argv)

    decision = evaluate_target(args.target, load_allowed_networks(args.scope))
    prefix = "ALLOW" if decision.allowed else "DENY"
    print(f"{prefix}: {decision.reason}")
    return 0 if decision.allowed else 2


if __name__ == "__main__":
    raise SystemExit(main())
