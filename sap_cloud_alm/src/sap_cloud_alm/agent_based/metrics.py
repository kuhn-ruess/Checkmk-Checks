#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
import ast

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    Service,
    check_levels,
    State,
    Result,
    Metric
)


def parse_function(string_table):
    """
    Parse Device Data to Dict
    """
    parsed = {}
    for line in string_table:
        if line[0].startswith('[[['):
            found_metric = line[0][3:-3]
        else:
            parsed[found_metric] = ast.literal_eval(line[0])
    return parsed


def discover_service(section):
    """
    Discover
    """
    for service_id in section:
        yield Service(item=service_id)


def check_service(item, section):
    """
    Check Metric
    """
    data = section.get(item)
    if not data:
        yield Result(state=State.UNKNOWN, summary=f"No data for item {item}")
        return

    for field_name, field_value in data.items():
        state = State.OK
        if field_name == 'warningStratus' and field_value != 0.0:
            state = State.WARN
        elif field_name == 'criticalStatus' and field_value != 0.0:
            state = State.CRIT
        elif field_name == 'valueAvg':
            yield Metric(name=field_name, value=field_value)
        yield Result(state=state, summary=f"{field_name}: {field_value}")



agent_section_sap_cloud_alm_metrics = AgentSection(
    name = "sap_cloud_alm_metrics",
    parse_function = parse_function,
)


check_plugin_sap_cloud_alm_metrics = CheckPlugin(
    name = "sap_cloud_alm_metrics",
    service_name = "Metric %s",
    discovery_function = discover_service,
    check_function = check_service,
)
