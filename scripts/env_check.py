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
    registry_names: tuple[str, ...] = ()
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


def _find_windows_registry_app(names: tuple[str, ...]) -> str | None:
    if os.name != "nt" or not names:
        return None

    try:
        import winreg
    except ImportError:
        return None

    roots = (
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
    )
    wanted = tuple(name.casefold() for name in names)

    for hive, key_path in roots:
        try:
            with winreg.OpenKey(hive, key_path) as root:
                index = 0
                while True:
                    try:
                        subkey_name = winreg.EnumKey(root, index)
                    except OSError:
                        break
                    index += 1
                    try:
                        with winreg.OpenKey(root, subkey_name) as subkey:
                            display_name = str(winreg.QueryValueEx(subkey, "DisplayName")[0])
                            if not any(token in display_name.casefold() for token in wanted):
                                continue
                            try:
                                version = str(winreg.QueryValueEx(subkey, "DisplayVersion")[0])
                            except OSError:
                                version = "unknown-version"
                            try:
                                location = str(winreg.QueryValueEx(subkey, "InstallLocation")[0]).strip()
                            except OSError:
                                location = ""
                            if not location:
                                try:
                                    location = str(winreg.QueryValueEx(subkey, "DisplayIcon")[0]).split(",", 1)[0]
                                except OSError:
                                    location = "registry entry"
                            return f"{display_name} {version} | {location} | detected via registry"
                    except OSError:
                        continue
        except OSError:
            continue
    return None


def check_tool(tool: ToolCheck) -> tuple[str, str]:
    if tool.command:
        executable = shutil.which(tool.command[0])
        if executable:
            status, detail = _run_version((executable, *tool.command[1:]))
            return status, f"{detail} | {executable}"

    candidate = _find_candidate(tool.candidates)
    if candidate:
        return "OK", f"found: {candidate}"

    registry_app = _find_windows_registry_app(tool.registry_names)
    if registry_app:
        suffix = f" | {tool.note}" if tool.note else ""
        return "OK", f"{registry_app}{suffix}"

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
        command=("tshark", "--version"),
        candidates=(r"%ProgramFiles%\Wireshark\Wireshark.exe", r"%ProgramFiles%\Wireshark\tshark.exe"),
        registry_names=("wireshark",),
        note="TShark in PATH is preferred for reproducible CLI checks",
    ),
    ToolCheck(
        "VMware Workstation",
        command=("vmrun", "-T", "ws", "list"),
        candidates=(
            r"%ProgramFiles(x86)%\VMware\VMware Workstation\vmware.exe",
            r"%ProgramFiles%\VMware\VMware Workstation\vmware.exe",
        ),
        registry_names=("vmware workstation",),
    ),
    ToolCheck(
        "Burp Suite",
        candidates=(
            r"%LOCALAPPDATA%\Programs\BurpSuiteCommunity\BurpSuiteCommunity.exe",
            r"%ProgramFiles%\BurpSuiteCommunity\BurpSuiteCommunity.exe",
        ),
        registry_names=("burp suite", "burpsuite"),
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