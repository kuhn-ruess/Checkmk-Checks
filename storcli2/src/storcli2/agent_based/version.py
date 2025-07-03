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


agent_section_storcli2_version = AgentSection(
    name="storcli2_version",
    parse_function=parse_storcli2_list,
)


def discover_storcli2_version(section):
    yield Service()

def check_storcli2_version(section):
    if "Firmware Version" in section.keys():
        yield Result(state=State.OK, summary=f"Firmware Version: {section['Firmware Version']}")
    else:
        yield Result(state=State.UNKNOWN, summary="Firmware version not found")

    if "Package Version" in section.keys():
        yield Result(state=State.OK, summary=f"Package Version: {section['Package Version']}")
    else:
        yield Result(state=State.UNKNOWN, summary="Package version not found")

    if "Driver Version" in section.keys():
        yield Result(state=State.OK, summary=f"Driver Version: {section['Driver Version']}")
    else:
        yield Result(state=State.UNKNOWN, summary="Driver version not found")


check_plugin_storcli2_version = CheckPlugin(
    name="storcli2_version",
    service_name="StorCli2 Version",
    sections=["storcli2_version"],
    discovery_function=discover_storcli2_version,
    check_function=check_storcli2_version,
)
