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
)


def parse_function(string_table):
    """
    Parse Device Data to Dict
    """
    parsed = {}
    for line in string_table:
        print(line)
        continue
    return parsed


def discover_service(section):
    """
    Discover
    """
    yield Service()


def check_service(section):
    """
    Check single Service
    """
    data = section[item]
    yield Result(state=State.OK, summary="Hallo Welt")


agent_section_cmdb_syncer_service = AgentSection(
    name = "semu_frames",
    parse_function = parse_function,
)


check_plugin_cmdb_syncer_service = CheckPlugin(
    name = "semu_frames",
    sections = ["semu_frames"],
    service_name = "Framerate",
    discovery_function = discover_service,
    check_function = check_service,
)
