#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from pydantic import BaseModel
from typing import List, Optional

from cmk.server_side_calls.v1 import (
    HostConfig,
    Secret,
    SpecialAgentCommand,
    SpecialAgentConfig,
)


class AgentJSONEndpoint(BaseModel):
    api_url: str
    username: Optional[str] = None
    password: Optional[Secret] = None
    # Default POST keeps existing rules (saved without a method) working.
    method: Optional[str] = "post"


class AgentJSONParams(BaseModel):
    # New format: a list of endpoints, each with its own credentials.
    endpoints: Optional[List[AgentJSONEndpoint]] = None
    # Legacy single-endpoint format (kept so old rules keep working even if
    # the ruleset migration has not been applied to the stored value yet).
    api_url: Optional[str] = None
    username: Optional[str] = None
    password: Optional[Secret] = None
    method: Optional[str] = "post"


def _endpoints(params: AgentJSONParams):
    if params.endpoints:
        return params.endpoints
    if params.api_url:
        return [AgentJSONEndpoint(
            api_url=params.api_url,
            username=params.username,
            password=params.password,
            method=params.method,
        )]
    return []


def generate_agent_json_command(params: AgentJSONParams, host_config: HostConfig):
    arguments = []
    for endpoint in _endpoints(params):
        password = endpoint.password.unsafe() if endpoint.password else ""
        user = endpoint.username or ""
        arguments += [
            endpoint.api_url,
            user,
            password,
            endpoint.method or "post",
        ]

    yield SpecialAgentCommand(command_arguments=arguments)


special_agent_json = SpecialAgentConfig(
    name = "json",
    parameter_parser = AgentJSONParams.model_validate,
    commands_function = generate_agent_json_command,
)
