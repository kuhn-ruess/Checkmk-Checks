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
    register,
)


def get_files(conf: Any) -> FileGenerator:
    """Deploy the agent plug-in."""
    match conf.get("deployment", ("do_not_deploy", None)):
        case "cached", float(interval) | int(interval):
            yield Plugin(base_os=OS.LINUX, source=Path("open-iscsi"), interval=int(interval))
        case "sync", _:
            yield Plugin(base_os=OS.LINUX, source=Path("open-iscsi"))


register.bakery_plugin(
    name="open_iscsi",
    files_function=get_files,
)
