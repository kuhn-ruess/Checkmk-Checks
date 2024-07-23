#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from pydantic import BaseModel
from cmk.server_side_calls.v1 import (
    ActiveCheckCommand,
    ActiveCheckConfig,
)


class VideotextParams(BaseModel):
    url: str
    pattern: str
    timeout: float | None = None
    warn: float | None = None
    crit: float | None = None



def videotext_arguments(params, host_config):
    yield ActiveCheckCommand(
        service_description = "Videotext",
        command_arguments = (
            "-u",
            params.url,
            "-p",
            params.pattern,
            "-t",
            params.timeout if params.timeout else "2.5",
            "-w",
            params.warn if params.warn else "900.0",
            "-c",
            params.crit if params.crit else "1200.0",
        )
    )


active_check_videotext = ActiveCheckConfig(
    name = "videotext",
    parameter_parser = VideotextParams.model_validate,
    commands_function = videotext_arguments,
)
