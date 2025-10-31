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


class ServiceCounterParams(BaseModel):
    service_filters: list
    timeout: float


def generate_service_counter_command(params: ServiceCounterParams, host_config: HostConfig):
    args = []

    if params.timeout:
        args.append(f"{params.timeout}")
    else:
        args.append("2.5")

    for item in params.service_filters:
        args_list = []
        for what in ['name', 'service_pattern', 'host_label_pattern',
                'host_name_pattern', 'host_label_pattern_negated', 'site_name_pattern']:
            args_list.append(item.get(what, "None"))

        args.append("|".join(args_list))

    yield SpecialAgentCommand(
        command_arguments = (
            [arg for arg in args]
            #f"{params.timeout}" if params.timeout else "2.5",
            #[f"{item['name']}|{item['pattern']}" for item in params.service_filters]
            #f"{item['name']}|{item['pattern']}" for item in params.service_filters
        )
    )


special_agent_service_counter = SpecialAgentConfig(
    name = "service_counter",
    parameter_parser = ServiceCounterParams.model_validate,
    commands_function = generate_service_counter_command,
)
