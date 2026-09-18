"""
Agent

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
from pydantic import BaseModel

from cmk.server_side_calls.v1 import HostConfig, SpecialAgentCommand, SpecialAgentConfig


class ConfigParser(BaseModel):
    """
    Config Parser
    """
    patterns: list[str]
    staleness: float = 1.5
    sockets: list[str] = []
    timeout: int = 30


def agent_arguments(params: ConfigParser, host_config: HostConfig):
    """
    Build Special Agent Command Line
    """
    args: list[str] = []

    for pattern in params.patterns:
        args += ["--pattern", pattern]

    args += [
        "--staleness", str(params.staleness),
        "--timeout", str(params.timeout),
    ]

    for livestatus_socket in params.sockets:
        args += ["--socket", livestatus_socket]

    yield SpecialAgentCommand(command_arguments=args)


special_agent_servicegroup_states = SpecialAgentConfig(
    name="servicegroup_states",
    parameter_parser=ConfigParser.model_validate,
    commands_function=agent_arguments,
)
