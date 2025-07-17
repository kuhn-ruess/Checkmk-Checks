#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""


from pydantic import BaseModel
from typing import Optional # type: ignore

from cmk.server_side_calls.v1 import (
    HostConfig,
    Secret,
    SpecialAgentCommand,
    SpecialAgentConfig,
)

class AgentPowermaxUParams(BaseModel):
    username: str
    password: Secret
    port: Optional[int] = None
    use_ip: Optional[bool] = None
    disablegetSrpInfo: Optional[bool] = None
    disablegetDirectorInfo: Optional[bool] = None
    disablegetHealthScoreInfo: Optional[bool] = None
    disablegetHealthCheckInfo: Optional[bool] = None
    disablegetArrayPerformanceInfo: Optional[bool] = None
    disablegetPortGroupInfo: Optional[bool] = None
    disablegetAlertInfo: Optional[bool] = None
    disablegetMaskingViewInfo: Optional[bool] = None
    enableRemoteSymChecks: Optional[bool] = None
    cache_time: Optional[int] = None
    no_cert_check: Optional[bool] = None


def generate_powermanx_command(params: AgentPowermaxUParams, host_config: HostConfig):
    """
    Define the Arguements
    """
    args = []
    args.append("--user")
    args.append(params.username)
    args.append("--password")
    args.append(params.password.unsafe())
    if params.port:
        args.append("--port")
        args.append(str(params.port))
    if params.cache_time:
        args.append("--cache_time")
        args.append(str(params.cache_time))
    for what in [
        "disablegetSrpInfo",
        "disablegetDirectorInfo",
        "disablegetHealthScoreInfo",
        "disablegetHealthCheckInfo",
        "disablegetArrayPerformanceInfo",
        "disablegetPortGroupInfo",
        "disablegetAlertInfo",
        "disablegetMaskingViewInfo",
        "enableRemoteSymChecks",
        "no_cert_check",
        ]:
        if getattr(params, what):
            args.append(f'--{what}')

    args.append("--hostname")


    if params.use_ip:
        try:
            # Checkmk 2.3
            ip_address = host_config.ipv4_address
        except AttributeError:
            # Checkmk 2.4
            ip_address = host_config.primary_ip_config.address
        args.append(ip_address)
    else:
        args.append(host_config.name)

    yield SpecialAgentCommand(
        command_arguments = args
    )

special_agent_semu = SpecialAgentConfig(
    name = "unisphere_powermax",
    parameter_parser = AgentPowermaxUParams.model_validate,
    commands_function = generate_powermanx_command,
)