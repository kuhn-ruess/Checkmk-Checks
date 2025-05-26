#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from pydantic import BaseModel

from cmk.server_side_calls.v1 import (
    HostConfig,
    Secret,
    SpecialAgentCommand,
    SpecialAgentConfig,
)


class ServiceMetricCounterParams(BaseModel):
    service_filters: list
    timeout: float
    path: str


def generate_service_counter_command(params: ServiceMetricCounterParams, host_config: HostConfig):
    args = []

    if params.timeout:
        args.append(f"{params.timeout}")
    else:
        args.append("2.5")

    args.append(params.path)

    for item in params.service_filters:
        args.append(f"{item['service_name']}|{item['ls_pattern']}|{item['metric']}|{item['metric_label']}")

    yield SpecialAgentCommand(
        command_arguments = (
            [arg for arg in args]
        )
    )


special_agent_service_counter = SpecialAgentConfig(
    name = "service_metric_counter",
    parameter_parser = ServiceMetricCounterParams.model_validate,
    commands_function = generate_service_counter_command,
)
