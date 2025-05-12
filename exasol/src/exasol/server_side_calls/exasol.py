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


class ExasolParams(BaseModel):
    username: str
    password: Secret
    ignore_dbs: Optional[list] = None


def generate_exasol_command(params: ExasolParams, host_config: HostConfig):
    args = [
        "-i",
        host_config.primary_ip_config.address,
        "-u",
        params.username,
        "-p",
        params.password.unsafe(),
    ]

    if params.ignore_dbs:
        args.append("-I")
        args.append(",".join(params.ignore_dbs))

    yield SpecialAgentCommand(command_arguments = args)


special_agent_exasol = SpecialAgentConfig(
    name = "exasol",
    parameter_parser = ExasolParams.model_validate,
    commands_function = generate_exasol_command,
)
