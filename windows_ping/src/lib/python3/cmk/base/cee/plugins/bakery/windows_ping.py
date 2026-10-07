#!/usr/bin/env python3
"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
from pathlib import Path
from typing import Any

from cmk.base.cee.plugins.bakery.bakery_api.v1 import (
    OS,
    FileGenerator,
    Plugin,
    PluginConfig,
    register,
)


def _ps_string(value: str) -> str:
    """Quote a value as PowerShell single quoted string."""
    return "'" + str(value).replace("'", "''") + "'"


def _ps_levels(levels: Any) -> tuple[str, str]:
    """Return warn/crit as PowerShell literals, $null when levels are off."""
    match levels:
        case ("fixed", (warn, crit)):
            return f"{float(warn):g}", f"{float(crit):g}"
    return "$null", "$null"


def _get_lines(conf: Any) -> list[str]:
    """Build the PowerShell config read by windows_ping.ps1."""
    lines = ["$Targets = @("]
    for target in conf.get("targets", []):
        address = target["address"].strip()
        name = target.get("name", "").strip()
        lines.append(f"    @{{ Address = {_ps_string(address)}; Name = {_ps_string(name)} }}")
    lines.append(")")
    warn_rta, crit_rta = _ps_levels(conf.get("rta_levels", ("fixed", (100.0, 500.0))))
    warn_pl, crit_pl = _ps_levels(conf.get("loss_levels", ("fixed", (40.0, 80.0))))
    lines += [
        f"$Count = {int(conf.get('count', 1))}",
        f"$TimeoutMs = {int(conf.get('timeout', 1000))}",
        f"$WarnRta = {warn_rta}",
        f"$CritRta = {crit_rta}",
        f"$WarnPl = {warn_pl}",
        f"$CritPl = {crit_pl}",
    ]
    return lines


def get_windows_ping_files(conf: Any) -> FileGenerator:
    """Deploy the ping plug-in and its target list to Windows hosts."""
    match conf.get("deployment", ("sync", None)):
        case "do_not_deploy", _:
            return
        case "cached", raw_interval:
            interval: int | None = int(raw_interval)
        case _:
            interval = None

    yield Plugin(
        base_os=OS.WINDOWS,
        source=Path("windows_ping.ps1"),
        interval=interval,
    )
    yield PluginConfig(
        base_os=OS.WINDOWS,
        lines=_get_lines(conf),
        target=Path("windows_ping.cfg.ps1"),
        include_header=True,
    )


register.bakery_plugin(
    name="windows_ping",
    files_function=get_windows_ping_files,
)
