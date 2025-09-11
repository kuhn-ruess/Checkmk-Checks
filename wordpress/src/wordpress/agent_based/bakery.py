#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
from typing import Any # type: ignore
from pathlib import Path
from cmk.base.cee.plugins.bakery.bakery_api.v1 import (
    register,
    Plugin,
    PluginConfig,
    OS,
    FileGenerator,
    PluginConfig,
)


def _get_config(conf):
    return [
        f'BASEDIR="{conf.get('base_dir', '/var/www/sites.d')}"',
        f'SEACH_STRING="{conf.get('search_string', 'deploy/current')}"',
    ]


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
        source=Path("wp_instances.php"),
        interval=interval,
    )

    yield PluginConfig(
        base_os=OS.LINUX,
        lines=_get_config(conf),
        target=Path("wp_instances.cfg"),
    )

register.bakery_plugin(
    name="wordpress_instances",
    files_function=get_files,
)