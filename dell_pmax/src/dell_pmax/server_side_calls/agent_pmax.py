#!/usr/bin/env python
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

class AgentDellPowermaxParams(BaseModel):
    username: str
    password: Secret

def generate_powermanx_command(params: AgentDellPowermaxParams, host_config: HostConfig):
    """
    Define the Arguements
    """
    print(host_config)
    args = []
    args.append("-r")
    args.append(params.username)
    args.append("-s")
    args.append(params.password.unsafe())
    args.append("-a")
    args.append(host_config.ipv4_config.address)

    yield SpecialAgentCommand(
        command_arguments = args
    )


special_agent_semu = SpecialAgentConfig(
    name = "dellpmax",
    parameter_parser = AgentDellPowermaxParams.model_validate,
    commands_function = generate_powermanx_command,
)
