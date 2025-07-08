#!/usr/bin/python
from typing import Any
from pathlib import Path
from cmk.base.cee.plugins.bakery.bakery_api.v1 import register, Plugin, OS, FileGenerator

def get_discover_password(conf: Any) -> FileGenerator:
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
        source=Path("password_age"),
        interval = interval,
    )

register.bakery_plugin(
    name="password_age",
    files_function=get_discover_password,
)
