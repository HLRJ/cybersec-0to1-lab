from pathlib import Path

import pytest

from scripts.check_lab_target import evaluate_target, load_allowed_networks


@pytest.fixture()
def scope_file(tmp_path: Path) -> Path:
    path = tmp_path / "lab-scope.yaml"
    path.write_text(
        """version: 1
allowed_networks:
  - 127.0.0.0/8
  - 192.168.56.0/24
""",
        encoding="utf-8",
    )
    return path


def test_load_allowed_networks(scope_file: Path) -> None:
    networks = load_allowed_networks(scope_file)
    assert [str(network) for network in networks] == ["127.0.0.0/8", "192.168.56.0/24"]

def test_allows_configured_lab_ip(scope_file: Path) -> None:
    decision = evaluate_target("192.168.56.42", load_allowed_networks(scope_file))
    assert decision.allowed is True
    assert "192.168.56.0/24" in decision.reason


def test_rejects_public_ip(scope_file: Path) -> None:
    decision = evaluate_target("8.8.8.8", load_allowed_networks(scope_file))
    assert decision.allowed is False
    assert "不在允许的实验网段" in decision.reason


def test_rejects_unconfigured_private_ip(scope_file: Path) -> None:
    decision = evaluate_target("10.0.0.8", load_allowed_networks(scope_file))
    assert decision.allowed is False


def test_rejects_hostname_in_first_version(scope_file: Path) -> None:
    decision = evaluate_target("example.com", load_allowed_networks(scope_file))
    assert decision.allowed is False
    assert "IP 地址" in decision.reason


def test_rejects_network_and_broadcast_addresses(scope_file: Path) -> None:
    networks = load_allowed_networks(scope_file)
    assert evaluate_target("192.168.56.0", networks).allowed is False
    assert evaluate_target("192.168.56.255", networks).allowed is False


def test_repository_scope_is_safe_by_default() -> None:
    scope = Path("scope/lab-scope.yaml")
    networks = load_allowed_networks(scope)
    assert evaluate_target("127.0.0.1", networks).allowed is True
    assert evaluate_target("192.168.56.10", networks).allowed is True
    assert evaluate_target("10.0.0.10", networks).allowed is False
    assert evaluate_target("8.8.8.8", networks).allowed is False
