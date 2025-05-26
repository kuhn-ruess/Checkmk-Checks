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
            parsed[line[0]] = {
                    'value': float(line[1]),
                    'metric': line[2],
                    'label': line[3],
                    }
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
