"""
Agent Azure Special

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
    tenant_id: str
    client_id: str
    client_secret: Secret
    subscription_id: str
    proxy_url: str | None = None

def azure_arguments(params, host_config):
    """
    Build Special Agent Command Line
    """
    args: list[str | Secret] = [
        "--tenant-id", params.tenant_id,
        "--client-id", params.client_id,
        "--client-secret", params.client_secret.unsafe(),
        "--subscription-id", params.subscription_id,
    ]
    
    if params.proxy_url:
        args.extend(["--proxy-url", params.proxy_url])
    
    yield SpecialAgentCommand(command_arguments=args)

special_agent_azure = SpecialAgentConfig(
    name="azure_extra",
    parameter_parser=ConfigParser.model_validate,
    commands_function=azure_arguments,
)



