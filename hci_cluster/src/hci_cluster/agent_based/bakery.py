#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
from typing import Any
from pathlib import Path
from cmk.base.cee.plugins.bakery.bakery_api.v1 import register, Plugin, PluginConfig, OS, FileGenerator


def _deployment(conf: Any) -> tuple[bool, int | None]:
    """
    Return (deploy, interval).

    Rules written before 2.1.0 are a plain dict (deploy synchronously) or
    ``None`` (do not deploy) — they stay valid until they are edited once.
    """
    if conf is None:
        return False, None
    match conf.get("deployment", ("sync", None)):
        case "do_not_deploy", _:
            return False, None
        case "cached", raw_interval:
            return True, int(raw_interval)
        case _:
            return True, None


def get_hci_cluster_files(conf: Any) -> FileGenerator:
    deploy, interval = _deployment(conf)
    if not deploy:
        return

    yield Plugin(
        base_os=OS.WINDOWS,
        source=Path("hci_cluster.ps1"),
        interval=interval,
    )
    yield PluginConfig(
        base_os=OS.WINDOWS,
        lines=_get_lines(conf),
        target=Path("hci_cluster.cfg.ps1"),
    )


# The PowerShell plug-in switches on "Inclusion" / "Exclusion" and ignores
# everything else. Rule values are python identifiers since 2.1.0, older rules
# carry the capitalized strings and pass through unchanged.
_FILTER_TYPES = {
    "no_filter": "None",
    "inclusion": "Inclusion",
    "exclusion": "Exclusion",
}


def _get_lines(conf):
    filter_type = conf.get('filter_type', 'no_filter')
    return [
        "$domain = \"{}\"".format(conf['domain']),
        "$FilterTyp = \"{}\"".format(_FILTER_TYPES.get(filter_type, filter_type)),
        "$FilterPattern = \"{}\"".format(conf.get('filter_pattern', '')),
    ]


register.bakery_plugin(
    name="hci_cluster",
    files_function=get_hci_cluster_files,
)
