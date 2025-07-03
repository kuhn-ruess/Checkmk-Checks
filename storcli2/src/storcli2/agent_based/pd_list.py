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
    map_state = {
        "UConf": "Unconfigured",
        "UConfUnsp": "Unconfigured Unsupported",
        "Conf": "Configured",
        "Unusbl": "Unusable",
        "GHS": "Global Hot Spare",
        "DHS": "Dedicated Hot Spare",
        "UConfShld": "Unconfigured Shielded",
        "ConfShld": "Configured Shielded",
        "Shld": "JBOD Shielded",
        "GHSShld": "GHS Shielded",
        "DHSShld": "DHS Shielded",
        "UConfSntz": "Unconfigured Sanitize",
        "ConfSntz": "Configured Sanitize",
        "JBODSntz": "JBOD Sanitize",
        "GHSSntz": "GHS Sanitize",
        "DHSSntz": "DHS Sanitize",
        "UConfDgrd": "Unconfigured Degraded",
        "ConfDgrd": "Configured Degraded",
        "JBODDgrd": "JBOD Degraded",
        "GHSDgrd": "GHS Degraded",
        "DHSDgrd": "DHS Degraded",
        "Various": "Multiple LU/NS Status",
        "U": "Up/On",
        "D": "Down/PowerSave",
        "T": "Transitioning",
        "F": "Foreign",
    }
    data = reparse_section(section)

    if item not in data.keys():
        yield Result(state=State.UNKNOWN, summary="Controller/Slot not found")
    else:
        values = data[item]

        output = f"State: {map_state[values['State']]}"
        if "Conf" != values["State"]:
            yield Result(state=State.CRIT, summary=output)
        else:
            yield Result(state=State.OK, summary=output)

        output = f"Status: {values['Status']}"
        if "Online" != values["Status"]:
            yield Result(state=State.CRIT, summary=output)
        else:
            yield Result(state=State.OK, summary=output)

        output = f"SP: {map_state[values['Sp']]}"
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
