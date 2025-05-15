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


agent_section_pure_hardware_fan = AgentSection(
    name="pure_hardware_fan",
    parse_function=parse_pure_hardware,
)


def discover_pure_hardware_fan(section):
    for item, data in section.items():
        if "FAN" in data:
            yield Service(item=item)

def check_pure_hardware_fan(item, section):
    data = section[item]

    if data["status"].lower() == "ok":
        state = State.OK
    else:
        state = State.CRIT

    yield Result(
        state=state,
        summary=f"FAN State: {data['status']}"
    )


check_plugin_pure_hardware_fan = CheckPlugin(
    name="pure_hardware_fan",
    sections=["pure_hardware"],
    service_name="FAN %s",
    discovery_function=discover_pure_hardware_fan,
    check_function=check_pure_hardware_fan,
)
