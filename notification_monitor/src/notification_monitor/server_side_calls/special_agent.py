#!/usr/bin/env python3
"""
This module defines the configuration and command
generation logic for the Notification Monitor special agent.

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from pydantic import BaseModel

from cmk.server_side_calls.v1 import (
    HostConfig,
    SpecialAgentCommand,
    SpecialAgentConfig,
)


class NotificationMonitorParams(BaseModel):
    """
    Parameters for configuring the Notification Monitor.
    """
    timeout: float
    command_regex: str
    path: str


def generate_command(params: NotificationMonitorParams, host_config: HostConfig):
    """
    Generates a special agent command based on the
    provided notification monitor parameters and host configuration.

    Args:
        params (NotificationMonitorParams): Parameters for the
        notification monitor, including timeout and path.
        host_config (HostConfig): Configuration for the target host.

    Yields:
        SpecialAgentCommand: An object representing the command to be
        executed with the constructed arguments.

    Notes:
        - If 'timeout' is not specified in params, a default value of "15" is used.
        - The 'path' from params is always included in the command arguments.
    """
    args = []

    if params.timeout:
        args.append(f"{params.timeout}")
    else:
        args.append("15")

    args.append(params.path)
    args.append(params.command_regex)

    yield SpecialAgentCommand(
        command_arguments = args
    )


special_agent_service_counter = SpecialAgentConfig(
    name = "notification_monitor",
    parameter_parser = NotificationMonitorParams.model_validate,
    commands_function = generate_command,
)
