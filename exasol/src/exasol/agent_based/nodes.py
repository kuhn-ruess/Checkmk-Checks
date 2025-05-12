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

def parse_exasol_nodes(string_table):
    nodes = {}

    for node, state in string_table:
        nodes[node] = state

    return nodes


agent_section_exasol_nodes = AgentSection(
    name = "exasol_nodes",
    parse_function = parse_exasol_nodes,
)


def discover_exasol_nodes(section):
    for node in section.keys():
        yield Service(item=node)


def check_exasol_nodes(item, section):
    if item not in section.keys():
        yield Result(state.UNKNOWN, summary="Item not found")

    else:
        text = f"Node in state {section[item]}"

        if "Running" != section[item]:
            yield Result(state=State.CRIT, summary=text)
        else:
            yield Result(state=State.OK, summary=text)


check_plugin_exasol_nodes = CheckPlugin(
    name = "exasol_nodes",
    sections = ["exasol_nodes"],
    service_name = "Node %s",
    discovery_function = discover_exasol_nodes,
    check_function = check_exasol_nodes,
)
