#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from pathlib import Path
from typing import Any  # type: ignore

from cmk.base.plugins.bakery.bakery_api.v1 import (
    FileGenerator,
    OS,
    Plugin,
    PluginConfig,
    register,
)


def get_deployment(conf: Any) -> tuple[bool, int | None]:
    """Whether the plug-in is deployed, and its cache age when it runs asynchronously."""
    match conf.get("deployment", ("do_not_deploy", None)):
        case "cached", float(raw_interval) | int(raw_interval):
            return True, int(raw_interval)
        case "sync", _:
            return True, None
    return False, None


def get_files(conf: Any) -> FileGenerator:
    """Deploy the agent plug-in and its configuration."""
    deploy, interval = get_deployment(conf)
    if not deploy:
        return

    yield Plugin(base_os=OS.LINUX, source=Path("dnf_update"), interval=interval)
    yield PluginConfig(
        base_os=OS.LINUX,
        lines=[f"VETO_FILE={conf.get('veto_file', '/etc/dnf.veto')}"],
        target=Path("dnf_update.cfg"),
        include_header=True,
    )


register.bakery_plugin(
    name="dnf_update",
    files_function=get_files,
)
