#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from pydantic import BaseModel
from typing import Optional

from cmk.server_side_calls.v1 import (
    HostConfig,
    Secret,
    SpecialAgentCommand,
    SpecialAgentConfig,
)


class PureParams(BaseModel):
    token: Secret


def generate_pure_command(params: PureParams, host_config: HostConfig):
    args = [
        "-i",
        host_config.primary_ip_config.address,
        "-t",
        params.token.unsafe(),
    ]

    yield SpecialAgentCommand(command_arguments = args)


special_agent_pure = SpecialAgentConfig(
    name = "pure",
    parameter_parser = PureParams.model_validate,
    commands_function = generate_pure_command,
)
