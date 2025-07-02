#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.agent_based.v2 import (
    Metric,
    Result,
    Service,
    State,
    AgentSection,
    CheckPlugin,
)

from .utils.storcli2 import parse_storcli2_list


agent_section_storcli2_status = AgentSection(
    name="storcli2_status",
    parse_function=parse_storcli2_list,
)


def discover_storcli2_status(params, section):
    data = {}

    for key, value in section.items():
        skip = False

        for key_filter in params["filters"]:

            if key_filter.endswith("*"):
                if key.startswith(key_filter[:-1]):
                    skip = True

            elif key_filter == key:
                skip = True

        if not skip:
            data[key] = value

    yield Service(item=None, parameters=data)

def check_storcli2_status(params, section):
    for key, value in section.items():
        if key in params.keys():
            if value != params[key]:
                yield Result(state=State.CRIT, notice=f"{key}: current={value}, discovery={params[key]}")
            else:
                yield Result(state=State.OK, notice=f"{key}: {value}")
        else:
            continue


check_plugin_storcli2_status = CheckPlugin(
    name="storcli2_status",
    service_name="StorCli2 Status",
    sections=["storcli2_status"],
    discovery_function=discover_storcli2_status,
    discovery_ruleset_name="discover_storcli2_status",
    discovery_default_parameters={
        "filters": []
    },
    check_function=check_storcli2_status,
    check_default_parameters={},
)
