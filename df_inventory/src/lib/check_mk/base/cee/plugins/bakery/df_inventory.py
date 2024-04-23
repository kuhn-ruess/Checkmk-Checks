#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
"""
Docker df
"""
from typing import Any
from pathlib import Path
from cmk.base.cee.plugins.bakery.bakery_api.v1 import register, Plugin, OS, FileGenerator


def get_df_inventory(conf: Any) -> FileGenerator:
    """
    DF Inventory
    """

    yield Plugin(
        base_os=OS.LINUX,
        source=Path("df_inventory_linux.sh"),
        interval = 43200,
    )
    yield Plugin(
        base_os=OS.SOLARIS,
        source=Path("df_inventory_solaris.sh"),
        interval = 43200,
    )
    yield Plugin(
        base_os=OS.AIX,
        source=Path("df_inventory_aix.sh"),
        interval = 43200,
    )



register.bakery_plugin(
    name="df_inventory",
    files_function=get_df_inventory,
)
