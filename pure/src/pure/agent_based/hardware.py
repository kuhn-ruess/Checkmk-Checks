#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    Result,
    Service,
    State,
)

from .utils.pure import (
    parse_pure_hardware,
)


agent_section_pure_hardware = AgentSection(
    name="pure_hardware",
    parse_function=parse_pure_hardware,
)


def discover_pure_hardware(section):
    for item, data in section.items():
        if "default" in data:
            yield Service(item=item)

def check_pure_hardware(item, section):
    if item not in section.keys():
        yield Result(
            state=State.UNKNOWN,
            summary=f"Item {item} not found",
        )

    else:
        data = section[item]

        if data["status"].lower() == "ok":
            state = State.OK
        else:
            state = State.CRIT

        yield Result(
            state=state,
            summary=f"Device State: {data['status']}"
        )


check_plugin_pure_hardare = CheckPlugin(
    name="pure_hardware",
    sections=["pure_hardware"],
    service_name="Hardware %s",
    discovery_function=discover_pure_hardware,
    check_function=check_pure_hardware,
)
