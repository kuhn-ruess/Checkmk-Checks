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
    """Deploy the agent plug-in, synchronously or asynchronously."""
    match conf.get("deployment", ("do_not_deploy", None)):
        case "cached", float(raw_interval) | int(raw_interval):
            yield Plugin(base_os=OS.LINUX, source=Path("xfs_quota"), interval=int(raw_interval))
        case "sync", _:
            yield Plugin(base_os=OS.LINUX, source=Path("xfs_quota"))


register.bakery_plugin(
    name="xfs_quota",
    files_function=get_files,
)
