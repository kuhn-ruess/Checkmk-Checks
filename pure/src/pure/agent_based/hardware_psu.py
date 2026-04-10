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


agent_section_pure_hardware_psu = AgentSection(
    name="pure_hardware_psu",
    parse_function=parse_pure_hardware,
)


def discover_pure_hardware_psu(section):
    for item, data in section.items():
        if "PSU" in data:
            yield Service(item=item)


def check_pure_hardware_psu(item, section):
    data = section[item]

    if data["status"].lower() == "ok":
        state = State.OK
    else:
        state = State.CRIT

    yield Result(
        state=state,
        summary=f"PSU State: {data['status']}"
    )


check_plugin_pure_hardware_psu = CheckPlugin(
    name="pure_hardware_psu",
    sections=["pure_hardware"],
    service_name="PSU %s",
    discovery_function=discover_pure_hardware_psu,
    check_function=check_pure_hardware_psu,
)
