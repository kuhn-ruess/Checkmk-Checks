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


class AgentJSONParams(BaseModel):
    api_url: str
    username: Optional[str] = None
    password: Optional[Secret] = False


def generate_agent_json_command(params: AgentJSONParams, host_config: HostConfig):
    password = ""
    if params.password:
        password = params.password.unsafe()
    user = ""
    if params.username:
        user = params.username

    yield SpecialAgentCommand(
        command_arguments = (
            params.api_url,
            user,
            password,
        )
    )


special_agent_json = SpecialAgentConfig(
    name = "json",
    parameter_parser = AgentJSONParams.model_validate,
    commands_function = generate_agent_json_command,
)
