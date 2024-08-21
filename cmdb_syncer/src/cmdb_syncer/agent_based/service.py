#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
import json

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    Result,
    Service,
    State,
)


def parse_cmdb_syncer_service(string_table):
    """
    Parse Device Data to Dict
    """
    parsed = {}
    service_name = False
    for line in string_table:
        if line[0].startswith('[[['):
            service_name = line[0][3:-3]
        else:
            parsed[service_name] = json.loads(line[0])
    return parsed


def discover_cmdb_syncer_service(section):
    """
    Discover one Service per Device
    """
    for service_id in section:
        yield Service(item=service_id)


def check_cmdb_syncer_service(item, params, section):
    """
    Check single Service
    """
    state = State.OK
    data = section[item]
    yield Result(state=state, summary=data['message'])
    if data['has_error']:
        yield Result(state=State.CRIT, summary="Has Error")

    for detail in data['details']:
        yield Result(state=State.OK, summary=f"{detail['name']}: {detail['message']}")

    state = State.OK


agent_section_cmdb_syncer_service = AgentSection(
    name = "cmdb_syncer_service",
    parse_function = parse_cmdb_syncer_service,
)


check_plugin_cmdb_syncer_service = CheckPlugin(
    name = "cmdb_syncer_service",
    sections = ["cmdb_syncer_service"],
    service_name = "Service %s",
    discovery_function = discover_cmdb_syncer_service,
    check_function = check_cmdb_syncer_service,
    check_default_parameters = {},
)
