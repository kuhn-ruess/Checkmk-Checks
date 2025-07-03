#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.agent_based.v2 import (
    get_value_store,
    Metric,
    Result,
    Service,
    State,
    AgentSection,
    CheckPlugin,
)
from cmk.plugins.lib.temperature import check_temperature, TempParamDict

from .utils.storcli2 import parse_storcli2_list


agent_section_storcli2_hwcfg = AgentSection(
    name="storcli2_hwcfg",
    parse_function=parse_storcli2_list,
)


def discover_storcli2_temp(section):
    if "Chip temperature(C)" in section.keys():
        yield Service(item="Chip")

    if "Board temperature(C)" in section.keys():
        yield Service(item="Board")

def check_storcli2_temp(item, params, section):
    if "Chip" == item and "Chip temperature(C)" in section.keys():
        yield from check_temperature(
            reading=int(section["Chip temperature(C)"]),
            params=params,
            unique_name="chip_temp",
            value_store=get_value_store(),
        )
    elif "Chip" == item and not "Chip temperature(C)" in section.keys():
        yield Result(state=State.UNKNOWN, summary="Chip temperature(C) not found")

    if "Board" == item and "Board temperature(C)" in section.keys():
        yield from check_temperature(
            reading=int(section["Board temperature(C)"]),
            params=params,
            unique_name="board_temp",
            value_store=get_value_store(),
        )
    elif "Board" == item and not "Board temperature(C)" in section.keys():
        yield Result(state=State.UNKNOWN, summary="Board temperature(C) not found")


check_plugin_storcli2_temp = CheckPlugin(
    name="storcli2_temp",
    service_name="StorCli2 Temperature %s",
    sections=["storcli2_hwcfg"],
    discovery_function=discover_storcli2_temp,
    check_function=check_storcli2_temp,
    check_ruleset_name="temperature",
    check_default_parameters=TempParamDict(
        levels=(50.0, 60.0),
    )
)
