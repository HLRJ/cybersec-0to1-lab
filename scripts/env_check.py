from __future__ import annotations

import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ToolCheck:
    name: str
    command: tuple[str, ...] | None = None
    candidates: tuple[str, ...] = ()
    note: str = ""


def _run_version(command: tuple[str, ...]) -> tuple[str, str]:
    try:
        proc = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
            encoding="utf-8",
            errors="replace",
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return "WARN", str(exc)

    output = (proc.stdout or proc.stderr).strip()
    first_line = output.splitlines()[0] if output else f"exit={proc.returncode}"
    return ("OK" if proc.returncode == 0 else "WARN"), first_line


def _find_candidate(paths: tuple[str, ...]) -> str | None:
    expanded = [Path(os.path.expandvars(p)) for p in paths]
    return str(next((p for p in expanded if p.exists()), "")) or None


def check_tool(tool: ToolCheck) -> tuple[str, str]:
    if tool.command:
        executable = shutil.which(tool.command[0])
        if executable:
            status, detail = _run_version((executable, *tool.command[1:]))
            return status, f"{detail} | {executable}"

    candidate = _find_candidate(tool.candidates)
    if candidate:
        return "OK", f"found: {candidate}"

    suffix = f" | {tool.note}" if tool.note else ""
    return "MISSING", f"not found{suffix}"

TOOLS = (
    ToolCheck("Python", ("python", "--version")),
    ToolCheck("Git", ("git", "--version")),
    ToolCheck("PowerShell", ("powershell", "-NoProfile", "-Command", "$PSVersionTable.PSVersion.ToString()")),
    ToolCheck("OpenSSH", ("ssh", "-V")),
    ToolCheck("curl", ("curl.exe", "--version")),
    ToolCheck(
        "Wireshark",
        ("tshark", "--version"),
        (r"%ProgramFiles%\Wireshark\Wireshark.exe", r"%ProgramFiles%\Wireshark\tshark.exe"),
        "TShark in PATH is preferred for reproducible CLI checks",
    ),
    ToolCheck(
        "VMware Workstation",
        ("vmrun", "-T", "ws", "list"),
        (
            r"%ProgramFiles(x86)%\VMware\VMware Workstation\vmware.exe",
            r"%ProgramFiles%\VMware\VMware Workstation\vmware.exe",
        ),
    ),
    ToolCheck(
        "Burp Suite",
        candidates=(
            r"%LOCALAPPDATA%\Programs\BurpSuiteCommunity\BurpSuiteCommunity.exe",
            r"%ProgramFiles%\BurpSuiteCommunity\BurpSuiteCommunity.exe",
        ),
        note="Burp may be installed in a custom location",
    ),
    ToolCheck("VS Code", ("code", "--version")),
)


def main() -> int:
    print("STATUS   TOOL                 DETAIL")
    print("-" * 100)
    missing = 0
    for tool in TOOLS:
        status, detail = check_tool(tool)
        print(f"{status:<8} {tool.name:<20} {detail}")
        missing += status == "MISSING"

    print("-" * 100)
    print(f"Missing tools: {missing}")
    print("Read-only inventory complete; no software was installed or changed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())