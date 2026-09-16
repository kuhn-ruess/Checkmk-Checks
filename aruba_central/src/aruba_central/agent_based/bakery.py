#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from pathlib import Path
from typing import Any  # type: ignore

from cmk.base.cee.plugins.bakery.bakery_api.v1 import (
    FileGenerator,
    OS,
    Plugin,
    register,
)


def get_files(conf: Any) -> FileGenerator:
    """Deploy the cencli plugin for Linux and Windows."""
    mode = conf.get("deployment", ("do_not_deploy", None))
    match mode:
        case "do_not_deploy", _:
            return
        case "cached", float(raw_interval):
            interval: int | None = int(raw_interval)
        case "sync", _:
            interval = None
        case _:
            return

    yield Plugin(
        base_os=OS.LINUX,
        source=Path("aruba_central.py"),
        interval=interval,
    )
    yield Plugin(
        base_os=OS.WINDOWS,
        source=Path("aruba_central.ps1"),
        interval=interval,
    )


register.bakery_plugin(
    name="aruba_central",
    files_function=get_files,
)
