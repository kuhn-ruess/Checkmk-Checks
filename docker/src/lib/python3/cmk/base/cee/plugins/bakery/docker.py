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


def _get_check_docker_config_lines(conf):
    """
    Get Config Lines
    """
    config = []

    config.append(f"timeout={conf.get('timeout', 30)}")
    config.append(f"piggyback={conf.get('piggyback', False)}")

    config.append("[[whitelist]]")
    for entry in conf.get("label_whitelist", []):
        config.append(entry)

    config.append("[[replacements]]")
    for entry in conf.get("label_replacments", []):
        config.append(f"{entry[0]} {entry[1]}")

    return config


def get_check_docker_files(conf):
    """
    Get Files
    """
    yield Plugin(
        base_os = OS.LINUX,
        source = Path("check_docker.py"),
        interval = conf.get("interval", 120),
    )

    yield PluginConfig(
        base_os = OS.LINUX,
        lines = _get_check_docker_config_lines(conf),
        target = Path("check_docker.cfg"),
    )


register.bakery_plugin(
    name="check_docker",
    files_function=get_check_docker_files,
)
