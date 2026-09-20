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

def test_registry_fallback_can_resolve_custom_install(monkeypatch) -> None:
    import scripts.env_check as env_check

    monkeypatch.setattr(
        env_check,
        "_find_windows_registry_app",
        lambda names: "VMware Workstation 17.6.0 | D:\\VMware | detected via registry",
    )
    tool = ToolCheck(
        "VMware Workstation",
        ("cybersec-0to1-command-that-does-not-exist", "--version"),
        registry_names=("vmware workstation",),
    )
    status, detail = env_check.check_tool(tool)
    assert status == "OK"
    assert "detected via registry" in detail