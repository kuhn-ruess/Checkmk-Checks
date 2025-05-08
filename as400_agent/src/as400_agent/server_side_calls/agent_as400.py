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


class AgentAs400Params(BaseModel):
    driver: str
    system: str
    uid: str
    password: Secret


def generate_as400_agent_command(params: AgentAs400Params, host_config: HostConfig):
    args = []
    args.append(params.driver)
    args.append(params.system)
    args.append(params.uid)
    args.append(params.password.unsafe())

    yield SpecialAgentCommand(
        command_arguments = (
            [arg for arg in args]
        )
    )


special_agent_as400 = SpecialAgentConfig(
    name = "as400_agent",
    parameter_parser = AgentAs400Params.model_validate,
    commands_function = generate_as400_agent_command,
)
