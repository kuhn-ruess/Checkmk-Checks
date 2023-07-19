#!/usr/bin/env python3

from pathlib import Path

from .bakery_api.v1 import (
   OS,
   Plugin,
   PluginConfig,
   register,
)


def _get_check_docker_config_lines(conf):
    yield "[[whitelist]]"
    yield from conf.get("label_whitelist", [])
    yield "[[replacements]]"
    yield from (e[0] + " " + e[1] for e in conf.get("label_replacements", []))


def get_check_docker_files(conf):
    interval = conf.get("interval")
    yield Plugin(
      base_os=OS.LINUX,
      source=Path('check_docker.py'),
      target=Path('check_docker.py'),
      interval=interval,
    )
    if "label_whitelist" in conf:
        yield PluginConfig(
            base_os=OS.LINUX,
            lines=list(_get_check_docker_config_lines(conf)),
            target=Path("check_docker.cfg"),
        )


register.bakery_plugin(
    name="check_docker",
    files_function=get_check_docker_files,
)
