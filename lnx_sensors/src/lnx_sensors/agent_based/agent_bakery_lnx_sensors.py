#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from pathlib import Path

from .bakery_api.v1 import (
   OS,
   Plugin,
   register,
)


def get_lnx_sensors_files():
    yield Plugin(
        base_os=OS.LINUX,
        source=Path("lnx_sensors"),
    )


register.bakery_plugin(
    name="lnx_sensors",
    files_function=get_lnx_sensors_files,
)
