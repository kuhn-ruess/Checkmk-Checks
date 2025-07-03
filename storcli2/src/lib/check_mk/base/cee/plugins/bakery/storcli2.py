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
   PluginConfig,
   register,
)


def get_storcli2_lines(conf):
    config = []
    config.append(f"$STORCLI2_PATH=\'{conf.get('path', 'C:\\Program Files\\LSI\\storCLI2.exe')}\'")
    return config


def get_storcli2_files(conf):
    yield Plugin(
        base_os=OS.WINDOWS,
        source=Path("storcli2.ps1"),
    )

    yield PluginConfig(
        base_os = OS.WINDOWS,
        lines = get_storcli2_lines(conf),
        target = Path("storcli2.ps1"),
        include_header = True,
    )


register.bakery_plugin(
    name="storcli2",
    files_function=get_storcli2_files,
)
