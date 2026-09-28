#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from pathlib import Path
from typing import Any  # type: ignore

from cmk.base.cee.plugins.bakery.bakery_api.v1 import (
    DebStep,
    FileGenerator,
    OS,
    Plugin,
    register,
    RpmStep,
    Scriptlet,
    ScriptletGenerator,
    SystemBinary,
    SystemConfig,
)

UNIT = "cmk-aide-run"


def get_mode(conf: Any) -> tuple[str, dict]:
    """The deployment mode and its options."""
    mode, options = conf.get("deployment", ("do_not_deploy", None))
    return mode, options or {}


def get_config(conf: Any, mode: str) -> list[str]:
    """Lines of /etc/cmk-aide.cfg, read by cmk-aide-run and the agent plug-in."""
    lines = [
        f"MODE={mode}",
        f"RESULT_DIR={conf.get('result_dir', '/var/lib/cmk-aide')}",
        f"TIMEOUT={int(conf.get('timeout', 600))}",
        f"MAX_LINES={int(conf.get('max_lines', 2000))}",
    ]
    lines += [f"JOB {job['name']} {job['config']}" for job in conf.get("jobs", [])]
    return lines


def get_units(interval: int) -> tuple[list[str], list[str]]:
    """The systemd service and timer that run cmk-aide-run."""
    service = [
        "[Unit]",
        "Description=AIDE file integrity check for Checkmk",
        "",
        "[Service]",
        "Type=oneshot",
        f"ExecStart=/bin/sh -c 'exec {UNIT}'",
        "Nice=19",
        "IOSchedulingClass=idle",
    ]
    timer = [
        "[Unit]",
        "Description=Run the AIDE file integrity check for Checkmk",
        "",
        "[Timer]",
        "OnBootSec=5min",
        f"OnUnitActiveSec={interval}s",
        f"RandomizedDelaySec={min(interval // 10, 300)}s",
        "",
        "[Install]",
        "WantedBy=timers.target",
    ]
    return service, timer


def get_files(conf: Any) -> FileGenerator:
    """Deploy cmk-aide-run, the agent plug-in, the configuration and the timer."""
    mode, options = get_mode(conf)
    if mode == "do_not_deploy":
        return

    interval = None
    if mode == "inline" and (cache_age := options.get("cache_age")):
        interval = int(cache_age)

    yield Plugin(base_os=OS.LINUX, source=Path("aide"), interval=interval)
    yield SystemBinary(base_os=OS.LINUX, source=Path("aide/cmk-aide-run"), target=Path(UNIT))
    yield SystemConfig(
        base_os=OS.LINUX,
        lines=get_config(conf, mode),
        target=Path("cmk-aide.cfg"),
        include_header=True,
    )

    if mode == "timer":
        service, timer = get_units(int(options.get("interval", 3600)))
        yield SystemConfig(
            base_os=OS.LINUX,
            lines=service,
            target=Path("systemd/system") / f"{UNIT}.service",
            include_header=True,
        )
        yield SystemConfig(
            base_os=OS.LINUX,
            lines=timer,
            target=Path("systemd/system") / f"{UNIT}.timer",
            include_header=True,
        )


def get_scriptlets(conf: Any) -> ScriptletGenerator:
    """Enable the timer after installation and disable it on removal."""
    mode, _options = get_mode(conf)
    if mode == "do_not_deploy":
        return

    if mode == "timer":
        install = [
            "if command -v systemctl >/dev/null 2>&1; then",
            "    systemctl daemon-reload",
            f"    systemctl enable --now {UNIT}.timer",
            f"    systemctl start --no-block {UNIT}.service",
            "fi",
        ]
    else:
        install = [
            "if command -v systemctl >/dev/null 2>&1; then",
            f"    systemctl disable --now {UNIT}.timer >/dev/null 2>&1 || true",
            "    systemctl daemon-reload",
            "fi",
        ]
    yield Scriptlet(step=RpmStep.POST, lines=install)
    yield Scriptlet(step=DebStep.POSTINST, lines=install)

    remove = [
        "if command -v systemctl >/dev/null 2>&1; then",
        f"    systemctl disable --now {UNIT}.timer >/dev/null 2>&1 || true",
        "fi",
    ]
    yield Scriptlet(step=RpmStep.PREUN, lines=['if [ "$1" = 0 ]; then'] + remove + ["fi"])
    yield Scriptlet(step=DebStep.PRERM, lines=['if [ "$1" = remove ]; then'] + remove + ["fi"])


register.bakery_plugin(
    name="aide",
    files_function=get_files,
    scriptlets_function=get_scriptlets,
)
