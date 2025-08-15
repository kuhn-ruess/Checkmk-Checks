#!/usr/bin/env python3

from typing import Any  # type: ignore
from pathlib import Path

from cmk.base.cee.plugins.bakery.bakery_api.v1 import register, Plugin, OS, FileGenerator


def get_files(conf: Any) -> FileGenerator:
    mode = conf.get('deployment', ("do_not_deploy", 0))
    match mode:
        case "do_not_deploy", _:
            return
        case "cached", float(raw_interval):
            interval: int | None = int(raw_interval)
        case "sync", _:
            interval = None
    
    yield Plugin(
        base_os=OS.LINUX,
        source=Path("df_inventory_linux.sh"),
        interval=interval,
    )
    
    yield Plugin(
        base_os=OS.SOLARIS,
        source=Path("df_inventory_solaris.sh"),
        interval=interval,
    )
    
    yield Plugin(
        base_os=OS.AIX,
        source=Path("df_inventory_aix.sh"),
        interval=interval,
    )


register.bakery_plugin(
    name="df_inventory",
    files_function=get_files,
)
