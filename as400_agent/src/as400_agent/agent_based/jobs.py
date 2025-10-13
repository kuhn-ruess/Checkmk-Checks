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
)


def parse_function(string_table):
    """
    Parse Device Data to Dict
    """
    parsed = {}
    found_job = None
    for line in string_table:
        if line[0].startswith('[[['):
            found_job = line[0][3:-3]
            continue
        if found_job:
            parsed.setdefault(found_job, {})
            parsed[found_job][line[0]] = line[1]
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

    for field_name, field_value in data.items():
        if field_name in [
            'JOB_TYPE', 'JOB_STATUS', 'JOB_END_REASON',
            'JOB_DESCRIPTION', 'JOB_ACTIVE_TIME',
        ]:
            yield Result(state=State.OK, summary=f"{field_name}: {field_value}")



agent_section_as400_jobs = AgentSection(
    name = "as400_agent_jobs",
    parse_function = parse_function,
)


check_plugin_as400_jobs = CheckPlugin(
    name = "as400_agent_jobs",
    sections = ["as400_agent_jobs"],
    service_name = "Job %s",
    discovery_function = discover_service,
    check_function = check_service,
    check_default_parameters = {'levels': None},
    #check_ruleset_name="as400_agent_jobs",
)
