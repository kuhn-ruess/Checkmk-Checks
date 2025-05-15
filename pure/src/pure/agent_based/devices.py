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
from cmk.agent_based.v2.render import (
    bytes,
)


def parse_pure_drives(string_table):
    section = {}

    for row in string_table:
        (item, status, serial, kind, capacity)  = row

        try:
            capacity = int(capacity)
        except ValueError:
            capacity = 0

        section[item] = {
            'status': status.lower(),
            'type': kind,
            'capacity': capacity,
            'serial': serial,
        }

    return section


agent_section_pure_drives = AgentSection(
    name="pure_drives",
    parse_function=parse_pure_drives,
)


def discover_pure_drives(section):
    for item in section.keys():
        yield Service(item=item)

def check_pure_drives(item, section):
    failed = []

    if item not in section.keys():
        yield Result(
            state=State.UNKNOWN,
            summary=f"Item {item} not found",
        )

    else:
        data = section[item]
        yield Result(state=State.OK, summary=f"Storage type: {data['type']}, Serial: {data['serial']}, Capacity: {bytes(data['capacity'])}")

        if data['status'].lower() == 'healthy':
            yield Result(state=State.OK, summary=f"Status: {data['status']}")

        else:
            yield Result(state=State.CRIT, summary=f"Status: {data['status']}")


check_plugin_pure_drives = CheckPlugin(
    name="pure_drives",
    sections=["pure_drives"],
    service_name="Drive %s",
    discovery_function=discover_pure_drives,
    check_function=check_pure_drives,
)
