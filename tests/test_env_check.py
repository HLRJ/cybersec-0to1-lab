import sys

from scripts.env_check import ToolCheck, _run_version, check_tool


def test_run_version_reports_current_python() -> None:
    status, detail = _run_version((sys.executable, "--version"))
    assert status == "OK"
    assert "Python" in detail


def test_missing_command_is_reported_without_installing_anything() -> None:
    tool = ToolCheck(
        "Definitely Missing",
        ("cybersec-0to1-command-that-does-not-exist", "--version"),
    )
    status, detail = check_tool(tool)
    assert status == "MISSING"
    assert detail.startswith("not found")