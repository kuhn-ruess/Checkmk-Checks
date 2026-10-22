#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from typing import Optional

from pydantic import BaseModel

from cmk.server_side_calls.v1 import (
    HostConfig,
    SpecialAgentCommand,
    SpecialAgentConfig,
)


class AriaAutomationParams(BaseModel):
    protocol: str = "http"
    port: int = 8008
    address: Optional[str] = None
    node_name: Optional[str] = None
    cluster_host: Optional[str] = None
    verify_cert: bool = True
    timeout: int = 30


def _address(params: AriaAutomationParams, host_config: HostConfig) -> str:
    """Return the address to query: rule value, host IP address or host name."""
    if params.address:
        return params.address
    try:
        address = host_config.primary_ip_config.address
    except ValueError:
        address = None
    if not address:
        return host_config.name
    return f"[{address}]" if ":" in address else address


def generate_aria_automation_command(params: AriaAutomationParams, host_config: HostConfig):
    """Build the command line of the special agent."""
    url = f"{params.protocol}://{_address(params, host_config)}:{params.port}/api/v1/services/cluster"
    args = [
        "--url", url,
        "--node-name", params.node_name or host_config.name,
        "--timeout", str(params.timeout),
    ]
    if params.cluster_host:
        args += ["--cluster-host", params.cluster_host]
    if not params.verify_cert:
        args.append("--no-cert-check")
    yield SpecialAgentCommand(command_arguments=args)


special_agent_aria_automation = SpecialAgentConfig(
    name="aria_automation",
    parameter_parser=AriaAutomationParams.model_validate,
    commands_function=generate_aria_automation_command,
)
