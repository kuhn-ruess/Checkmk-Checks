#!/usr/bin/env python3

from pathlib import Path

from .bakery_api.v1 import (
   OS,
   Plugin,
   PluginConfig,
   register,
)


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
            lines=conf["label_whitelist"],
            target=Path("check_docker.cfg"),
        )   


register.bakery_plugin(
    name="check_docker",
    files_function=get_check_docker_files,
)
