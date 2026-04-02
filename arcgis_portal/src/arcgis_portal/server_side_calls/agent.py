"""
Agent

Kuhn & Ruess GmbH
Consulting and Development
https://kuhn-ruess.de
"""
from pydantic import BaseModel
from cmk.server_side_calls.v1 import HostConfig, SpecialAgentCommand, SpecialAgentConfig, Secret


class ConfigParser(BaseModel):
    """
    Config Parser
    """
    username: str
    password: Secret
    proxy_url: str | None = None


def agent_arguments(params, host_config: HostConfig):
    """
    Build Special Agent Command Line
    """
    args: list[str | Secret] = [
        "--host-name", host_config.name,
        "--username", params.username,
        "--password", params.password.unsafe(),
    ]

    if params.proxy_url:
        args.extend(["--proxy-url", params.proxy_url])

    yield SpecialAgentCommand(command_arguments=args)


special_agent_agent = SpecialAgentConfig(
    name="arcgis_portal",
    parameter_parser=ConfigParser.model_validate,
    commands_function=agent_arguments,
)
