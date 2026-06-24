"""
Agent Icinga

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
from pydantic import BaseModel
from cmk.server_side_calls.v1 import SpecialAgentCommand, SpecialAgentConfig, Secret

class ConfigParser(BaseModel):
    """
    Config Parser
    """
    host_name: str
    username: str
    password: Secret
    ssl_verify: bool = True
    group_services: bool = True
    piggyback_prefix: str = ""

def icinga_arguments(params, host_config):
    """
    Build Special Agent Command Line
    """
    args: list[str | Secret] = [
        "--hostname", params.host_name,
        "--username", params.username,
        "--password", params.password.unsafe(),
    ]
    if not params.ssl_verify:
        args.append(
            "--no-verify"
        )
    if not params.group_services:
        args.append("--no-group")
    if params.piggyback_prefix:
        args += ["--piggyback-prefix", params.piggyback_prefix]
    yield SpecialAgentCommand(command_arguments=args)

special_agent_icinga = SpecialAgentConfig(
    name="icinga",
    parameter_parser=ConfigParser.model_validate,
    commands_function=icinga_arguments,
)