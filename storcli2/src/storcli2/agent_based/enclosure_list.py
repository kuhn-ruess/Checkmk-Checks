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


agent_section_storcli2_enclosure_list = AgentSection(
    name="storcli2_enclosure_list",
    parse_function=parse_storcli2_table,
)


def discover_storcli2_enclosure_list(section):
    for eid in section.keys():
        yield Service(item=eid)

def check_storcli2_enclosure_list(item, section):
    if item not in section.keys():
        yield Result(state=State.UNKNOWN, summary="Enclosure not found")
    else:
        values = section[item]

        yield Result(state=State.OK, summary=f"State: {values['State']}")
        yield Result(state=State.OK, summary=f"ProdID: {values['ProdID']}")

        output = f"Alarms: {values['Alms']}"
        if int(values["Alms"]) > 0:
            yield Result(state=State.CRIT, summary=output)
        else:
            yield Result(state=State.OK, summary=output)


check_plugin_storcli2_enclosure_list = CheckPlugin(
    name="storcli2_enclosure_list",
    service_name="StorCli2 Enclosure %s",
    sections=["storcli2_enclosure_list"],
    discovery_function=discover_storcli2_enclosure_list,
    check_function=check_storcli2_enclosure_list,
)
