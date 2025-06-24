#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
from typing import Any
from pathlib import Path
from cmk.base.cee.plugins.bakery.bakery_api.v1 import register, Plugin, PluginConfig, OS, FileGenerator

def get_files(conf: Any) -> FileGenerator:
    yield Plugin(
        base_os=OS.LINUX,
        source=Path("cifs_df"),
    )

register.bakery_plugin(
    name="cifs_df",
    files_function=get_files,
)
