#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
from typing import Any # type: ignore
from pathlib import Path
from cmk.base.cee.plugins.bakery.bakery_api.v1 import register, Plugin, PluginConfig, OS, FileGenerator

def get_files(conf: Any) -> FileGenerator:
    mode = conf.get('deployment', ("do_not_deploy", 0,0))
    match mode:
        case "do_not_deploy", _:
            return
        case "cached", float(raw_interval):
            interval: int | None = int(raw_interval)
        case "sync", _:
            interval = None
    yield Plugin(
        base_os=OS.LINUX,
        source=Path("ovo_agent_linux.sh"),
        interval=interval,
    )
    yield Plugin(
        base_os=OS.SOLARIS,
        source=Path("ovo_agent_solaris.sh"),
        interval=interval,
    )
    yield Plugin(
        base_os=OS.AIX,
        source=Path("ovo_agent_aix.sh"),
        interval=interval,
    )

register.bakery_plugin(
    name="ovo_agent",
    files_function=get_files,
)
