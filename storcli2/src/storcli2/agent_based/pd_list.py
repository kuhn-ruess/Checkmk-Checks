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


agent_section_storcli2_pd_list = AgentSection(
    name="storcli2_pd_list",
    parse_function=parse_storcli2_table,
)


def reparse_section(data):
    ret = {}

    for key, value in data.items():
        controller, slot = key.split(":")

        if controller not in ret:
            ret.setdefault(controller, {})

        ret[controller][slot] = value

    if len(ret.keys()) == 1:
        return ret[list(ret.keys())[0]]
    else:
        return data

def discover_storcli2_pd_list(section):
    data = reparse_section(section)

    for controller_slot in data.keys():
        yield Service(item=controller_slot)

def check_storcli2_pd_list(item, section):
    data = reparse_section(section)

    if item not in data.keys():
        yield Result(state=State.UNKNOWN, summary="Controller/Slot not found")
    else:
        values = data[item]

        output = f"State: {values['State']}"
        if "Conf" != values["State"]:
            yield Result(state=State.CRIT, summary=output)
        else:
            yield Result(state=State.OK, summary=output)

        output = f"Status: {values['Status']}"
        if "Online" != values["Status"]:
            yield Result(state=State.CRIT, summary=output)
        else:
            yield Result(state=State.OK, summary=output)

        output = f"SP: {values['Sp']}"
        if "U" != values["Sp"]:
            yield Result(state=State.CRIT, summary=output)
        else:
            yield Result(state=State.OK, summary=output)


check_plugin_storcli2_pd_list = CheckPlugin(
    name="storcli2_pd_list",
    service_name="StorCli2 PD %s",
    sections=["storcli2_pd_list"],
    discovery_function=discover_storcli2_pd_list,
    check_function=check_storcli2_pd_list,
)
