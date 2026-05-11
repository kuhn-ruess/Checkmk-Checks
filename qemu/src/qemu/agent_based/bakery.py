#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
"""Agent bakery hook for the qemu plugin."""
from pathlib import Path
from typing import Any

from cmk.base.cee.plugins.bakery.bakery_api.v1 import (
    FileGenerator,
    OS,
    Plugin,
    register,
)


def get_qemu_files(conf: Any) -> FileGenerator:
    mode = conf.get("deployment", ("do_not_deploy", None))
    if mode[0] == "do_not_deploy":
        return
    yield Plugin(
        base_os=OS.LINUX,
        source=Path("qemu"),
    )


register.bakery_plugin(
    name="qemu",
    files_function=get_qemu_files,
)
