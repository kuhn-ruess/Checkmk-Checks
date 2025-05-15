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


def parse_pure_array(string_table):
    section = {}

    for row in string_table:
        (item, version, revision, id)  = row

        section[item] = {
            'version': version,
            'revision': revision,
            'id': id,
        }

    return section

agent_section_pure_array = AgentSection(
    name="pure_array",
    parse_function=parse_pure_array,
)


def discover_pure_array(section):
    for item in section.keys():
        yield Service(item=item)

def check_pure_array(item, section):
    failed = []

    if item not in section.keys():
        yield Result(
            state=State.UNKNOWN,
            summary=f"Item {item} not found",
        )

    data = section[item]
    if item not in section.keys():
        yield Result(
            state=State.CRIT,
            summary=f"CRIT, Storage OS: Purity, Software version: {data['version']}",
            details=f"Software revision: {data['revision']}, Array ID: {data['id']}",
        )
    else:
        yield Result(
            state=State.OK,
            summary=f"OK, Storage OS: Purity, Software version: {data['version']}",
            details=f"Software revision: {data['revision']}, Array ID: {data['id']}",
        )


check_plugin_pure_array = CheckPlugin(
    name="pure_array",
    sections=["pure_array"],
    service_name="Array %s",
    discovery_function=discover_pure_array,
    check_function=check_pure_array,
)
