#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from pydantic import BaseModel
from urllib.parse import quote_plus

from cmk.server_side_calls.v1 import (
    HostConfig,
    Secret,
    SpecialAgentCommand,
    SpecialAgentConfig,
)


class AgentSapAlmParams(BaseModel):
    instance: str
    client_id: str
    metric_filter: str
    proxy: str
    client_secret: Secret


def generate_agent_command(params: AgentSapAlmParams, host_config: HostConfig):
    args = []
    args.append('--instance')
    args.append(params.instance)
    args.append('--client-id')
    args.append(params.client_id)
    args.append('--client-secret')
    args.append(params.client_secret.unsafe())
    args.append('--filter')
    args.append(quote_plus(params.metric_filter))
    args.append('--proxy')
    args.append(quote_plus(params.proxy))

    yield SpecialAgentCommand(
        command_arguments = args
    )


special_agent_sap_cloud_alm = SpecialAgentConfig(
    name = "sap_cloud_alm",
    parameter_parser = AgentSapAlmParams.model_validate,
    commands_function = generate_agent_command,
)
