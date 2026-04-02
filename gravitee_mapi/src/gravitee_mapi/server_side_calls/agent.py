"""
Agent

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
from pydantic import BaseModel

from cmk.server_side_calls.v1 import HostConfig, Secret, SpecialAgentCommand, SpecialAgentConfig


class ConfigParser(BaseModel):
    """
    Config Parser
    """
    token: Secret
    environment: str = "DEFAULT"
    interval: int = 60
    no_verify_ssl: bool = False


def agent_arguments(params: ConfigParser, host_config: HostConfig):
    """
    Build Special Agent Command Line
    """
    args: list[str | Secret] = [
        "--host-name", host_config.name,
        "--token", params.token.unsafe(),
        "--environment", params.environment,
        "--interval", str(params.interval),
    ]

    if params.no_verify_ssl:
        args.append("--no-verify-ssl")

    yield SpecialAgentCommand(command_arguments=args)


special_agent_gravitee_mapi = SpecialAgentConfig(
    name="gravitee_mapi",
    parameter_parser=ConfigParser.model_validate,
    commands_function=agent_arguments,
)
