#!/usr/bin/env python3
"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    Service,
    check_levels,
    State,
    Result,
    Metric,
)

def parse_function(string_table):
    """
    Parse
    """
    return string_table

def discover_service(section):
    """
    Discover
    """
    yield Service()


def check_service(section):
    """
    Check
    """
    if not section:
        yield Result(state=State.UNKNOWN, summary=f"No data for item {item}")
        return

    state = State.OK
    yield Result(
        state=state,
        summary="Hello World",
    )

agent_section_arcgis_certificates = AgentSection(
    name = "arcgis_certificates",
    parse_function = parse_function,
)


check_plugin_arcgis_certificates = CheckPlugin(
    name = "arcgis_certificates",
    service_name = "Certificate",
    discovery_function = discover_service,
    check_function = check_service,
)