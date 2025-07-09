#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
from typing import Any
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
        base_os=OS.WINDOWS,
        source=Path("digital_signage.ps1"),
        interval=interval,
    )

register.bakery_plugin(
    name="digital_signage",
    files_function=get_files,
)