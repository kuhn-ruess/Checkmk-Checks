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


agent_section_storcli2_tool = AgentSection(
    name="storcli2_tool",
    parse_function=parse_storcli2_list,
)


def discover_storcli2_tool(section):
    yield Service()

def check_storcli2_tool(section):
    if "ERROR" in section.keys():
        yield Result(state=State.UNKNOWN, summary=f"{' '.join(section['ERROR'])}")

    else:
        if "CLI Version" in section.keys():
            yield Result(state=State.OK, summary=f"CLI Version: {section['CLI Version']}")
        else:
            yield Result(state=State.UNKNOWN, summary="CLI version not found")

        if "Controller" in section.keys():
            yield Result(state=State.OK, summary=f"Controller: {section['Controller']}")
        else:
            yield Result(state=State.UNKNOWN, summary=f"Controller not found: {section['Description']}")

        if "Status" in section.keys():
            yield Result(state=State.OK, summary=f"Status: {section['Status']}")
        else:
            yield Result(state=State.UNKNOWN, summary="Status not found")


check_plugin_storcli2_tool = CheckPlugin(
    name="storcli2_tool",
    service_name="StorCli2 Tool",
    sections=["storcli2_tool"],
    discovery_function=discover_storcli2_tool,
    check_function=check_storcli2_tool,
)
