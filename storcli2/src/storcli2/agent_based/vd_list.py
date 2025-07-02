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

from .utils.storcli2 import parse_storcli2_table


agent_section_storcli2_vd_list = AgentSection(
    name="storcli2_vd_list",
    parse_function=parse_storcli2_table,
)


def discover_storcli2_vd_list(section):
    for item in section.keys():
        yield Service(item=item)

def check_storcli2_vd_list(item, section):
    if item not in section.keys():
        yield Result(state=State.UNKNOWN, summary="Item not found")

    else:
        for key, value in section[item].items():
            if "State" == key and "Optl" != value:
                yield Result(state=State.CRIT, summary=f"{key}: {value}")

            elif "Access" == key and "RW" != value:
                yield Result(state=State.CRIT, summary=f"{key}: {value}")

            else:
                yield Result(state=State.OK, summary=f"{key}: {value}")


check_plugin_storcli2_vd_list = CheckPlugin(
    name="storcli2_vd_list",
    service_name="StorCli2 VD %s",
    sections=["storcli2_vd_list"],
    discovery_function=discover_storcli2_vd_list,
    check_function=check_storcli2_vd_list,
)
