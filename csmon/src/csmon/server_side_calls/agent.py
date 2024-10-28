"""
Agent CSMON

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
    username: str
    password: Secret

def csmon_arguments(params, host_config):
    """
    Build Special Agent Command Line
    """
    args: list[str | Secret] = [
        "--hostname", host_config.name,
        "--username", params.username,
        "--password", params.password.unsafe(),
    ]
    yield SpecialAgentCommand(command_arguments=args)

special_agent_csmon = SpecialAgentConfig(
    name="csmon",
    parameter_parser=ConfigParser.model_validate,
    commands_function=csmon_arguments,
)
