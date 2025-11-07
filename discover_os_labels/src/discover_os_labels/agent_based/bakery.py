#!/usr/bin/env python3

from typing import Any  # type: ignore
from pathlib import Path

from cmk.base.cee.plugins.bakery.bakery_api.v1 import register, Plugin, OS, FileGenerator


def get_files(conf: Any) -> FileGenerator:
    mode, interval = conf.get('deployment', ("do_not_deploy", 0))
    match mode:
        case "do_not_deploy":
            return
        case "cached":
            interval: int | None = int(interval)
        case "sync":
            interval = None
    
    yield Plugin(
        base_os=OS.LINUX,
        source=Path("discover_os_labels.linux"),
        interval=interval,
    )
    
    yield Plugin(
        base_os=OS.SOLARIS,
        source=Path("discover_os_labels.solaris"),
        interval=interval,
    )
    
    yield Plugin(
        base_os=OS.AIX,
        source=Path("discover_os_labels.aix"),
        interval=interval,
    )

register.bakery_plugin(
    name="discover_os_labels",
    files_function=get_files,
)
