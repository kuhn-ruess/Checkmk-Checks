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
        continue
    return parsed


def discover_service(section):
    """
    Discover
    """
    for service_id in section:
        yield Service(item=service_id)


def check_service(item, params, section):
    """
    Check single Service
    """
    data = section[item]

    yield from check_levels(
         data['value'],
         levels_upper = params['levels'],
         label = data['label'],
         metric_name=data['metric'],
    )




agent_section_cmdb_syncer_service = AgentSection(
    name = "as400_agent_jobs",
    parse_function = parse_function,
)


check_plugin_cmdb_syncer_service = CheckPlugin(
    name = "as400_agent_jobs",
    sections = ["as400_agent_jobs"],
    service_name = "Job %s",
    discovery_function = discover_service,
    check_function = check_service,
    check_default_parameters = {'levels': None},
    check_ruleset_name="as400_agent_jobs",
)
