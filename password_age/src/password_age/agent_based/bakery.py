#!/usr/bin/python
from typing import Any
from pathlib import Path
from cmk.base.cee.plugins.bakery.bakery_api.v1 import register, Plugin, OS, FileGenerator

def get_discover_password(conf: Any) -> FileGenerator:
    mode, interval = conf.get('deployment', ("do_not_deploy", 0))
    match mode:
        case "do_not_deploy":
            return
        case "cached":
            interval = int(interval)
        case "sync":
            interval = None

    yield Plugin(
        base_os=OS.LINUX,
        source=Path("password_age.sh"),
        interval = interval,
    )

register.bakery_plugin(
    name="password_age",
    files_function=get_discover_password,
)
