#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.agent_based_api.v2 import (
    AgentSection,
    CheckPlugin,
    Result,
    Service,
    State,
)


def parse_quobyte_services(string_table):
    """
    Parse Device Data to Dict
    """
    parsed = {}
    for line in string_table:
        parsed[line[0]] = line[1]
    return parsed


def discover_quobyte_services(section):
    """
    Discover one Service per Device
    """
    for service_id in section:
        yield Service(item=service_id)


def check_quobyte_services(item, params, section):
    """
    Check single Service
    """
    state = State.OK
    status = section[item]
    if status != 'True':
        state = State.Crit
    yield Result(state=state, summary=f"Serice status: {status}")


agent_section_quobyte_services = AgentSection(
    name = "quobyte_services",
    parse_function = parse_quobyte_services,
)


check_plugin_quobyte_services = CheckPlugin(
    name = "quobyte_services",
    sections = ["quobyte_services"],
    service_name = "Service %s",
    discovery_function = discover_quobyte_services,
    check_function = check_quobyte_services,
    check_default_parameters = {},
)
