from pathlib import Path
import subprocess
import sys


SCRIPT = Path("scripts/check_lab_target.py")
SCOPE = Path("scope/lab-scope.yaml")


def run_cli(target: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), target, "--scope", str(SCOPE)],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def test_cli_allows_lab_target() -> None:
    result = run_cli("192.168.56.42")
    assert result.returncode == 0
    assert "ALLOW" in result.stdout
    assert "允许" in result.stdout


def test_cli_rejects_public_target() -> None:
    result = run_cli("8.8.8.8")
    assert result.returncode == 2
    assert "DENY" in result.stdout
    assert "不在允许" in result.stdout
