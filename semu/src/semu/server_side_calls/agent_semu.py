#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from pydantic import BaseModel

from cmk.server_side_calls.v1 import (
    HostConfig,
    Secret,
    SpecialAgentCommand,
    SpecialAgentConfig,
)


class AgentSEMUParams(BaseModel):
    username: str
    password: Secret


def generate_semu_agent_command(params: AgentSEMUParams, host_config: HostConfig):
    args = []
    args.append(host_config.name)
    args.append(params.username)
    args.append(params.password.unsafe())

    yield SpecialAgentCommand(
        command_arguments = (
            [arg for arg in args]
        )
    )


special_agent_semu = SpecialAgentConfig(
    name = "semu",
    parameter_parser = AgentSEMUParams.model_validate,
    commands_function = generate_semu_agent_command,
)
