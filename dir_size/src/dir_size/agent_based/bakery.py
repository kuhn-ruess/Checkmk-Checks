#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
"""
Dir Size Monitoring
"""
from typing import Any
from pathlib import Path
from cmk.base.cee.plugins.bakery.bakery_api.v1 import (
        register, Plugin, OS, FileGenerator,
        PluginConfig
        )


def _get_config_lines(conf):
    config = []
    for entry in conf.get('folders', []):
        if not entry.startswith('/'):
            entry = "/"+entry
        if not entry.endswith('/'):
            entry = entry+"/"
        config.append(entry)
    return config


def get_dir_size(conf: Any) -> FileGenerator:
    """
    Dir Size
    """
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
        source=Path("dir_size.sh"),
        interval = interval,
    )
    yield Plugin(
        base_os=OS.SOLARIS,
        source=Path("dir_size.sh"),
        interval = interval,
    )
    yield Plugin(
        base_os=OS.AIX,
        source=Path("dir_size.sh"),
        interval = interval,
    )

    yield PluginConfig(
        base_os=OS.LINUX,
        lines = _get_config_lines(conf),
        target = Path("dir_size.cfg"),
    )

    yield PluginConfig(
        base_os=OS.SOLARIS,
        lines = _get_config_lines(conf),
        target = Path("dir_size.cfg"),
    )

    yield PluginConfig(
        base_os=OS.AIX,
        lines = _get_config_lines(conf),
        target = Path("dir_size.cfg"),
    )


register.bakery_plugin(
    name="dir_size",
    files_function=get_dir_size,
)
