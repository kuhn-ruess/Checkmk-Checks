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


class AgentJSONParams(BaseModel):
    api_url: str
    username: str
    password: Secret



def generate_agent_json_command(params: AgentJSONParams, host_config: HostConfig):
    yield SpecialAgentCommand(
        command_arguments = (
            params.api_url
            params.username,
            params.password.unsafe(),
        )
    )


special_agent_json = SpecialAgentConfig(
    name = "json",
    parameter_parser = AgentJSONParams.model_validate,
    commands_function = generate_agent_json_command,
)
