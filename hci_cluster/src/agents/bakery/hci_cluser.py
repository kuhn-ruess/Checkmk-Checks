#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
from typing import Any
from pathlib import Path
from cmk.base.cee.plugins.bakery.bakery_api.v1 import register, Plugin, PluginConfig, OS, FileGenerator


def get_hci_cluster_files(conf: Any) -> FileGenerator:
    yield Plugin(
        base_os=OS.WINDOWS,
        source=Path("hci_cluster.ps1"),
    )
    yield PluginConfig(
        base_os=OS.WINDOWS,
        lines=_get_lines(conf),
        target=Path("hci_cluster.cfg.ps1"),
    )

def _get_lines(conf: Dict[str, str]) -> List[str]:
    return [
        "$domain = \"{}\"".format(conf['domain']),
        "$cluster_filter = \"{}\"".format(conf['cluster_filter']),
    ]


register.bakery_plugin(
    name="hci_cluster",
    files_function=get_hci_cluster_files,
)
