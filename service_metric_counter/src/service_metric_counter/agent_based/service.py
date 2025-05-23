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
            parsed[line[0]] = float(line[1])
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
    total = section[item]

    metric_label = params.get('metric_label', "Count")
    metric_name = params.get('metric_name', "count")

    yield from check_levels(
         total,
         levels_upper = params['levels'],
         label = metric_label,
         metric_name = metric_name,
    )




agent_section_cmdb_syncer_service = AgentSection(
    name = "service_metric_counter",
    parse_function = parse_function,
)


check_plugin_cmdb_syncer_service = CheckPlugin(
    name = "service_metric_counter",
    sections = ["service_metric_counter"],
    service_name = "Service %s",
    discovery_function = discover_service,
    check_function = check_service,
    check_default_parameters = {'levels': None},
    check_ruleset_name="service_metric_counter",
)
