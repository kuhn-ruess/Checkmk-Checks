#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
import json
from datetime import datetime

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    Result,
    Service,
    State,
    check_levels,
    render,
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
    data = section[item]
    # The agent now passes the real API failure reason (HTTP status,
    # rate-limit message, …) in ``message`` when ``has_error`` is set.
    if data.get('has_error'):
        yield Result(state=State.CRIT,
                     summary=data.get('message', 'API error'))
        return

    yield Result(state=State.OK, summary=data['message'])
    for detail in data.get('details', []):
        yield Result(state=State.OK, summary=f"{detail['name']}: {detail['message'][:40]}")


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

def parse_cmdb_syncer_cron(string_table):
    """
    Parse Device Data to Dict
    """
    parsed = {}
    try:
        for line in json.loads(string_table[0][0]):
            parsed[line['name']] = line
    except TypeError:
        return {}
    return parsed

def discover_cmdb_syncer_cron(section):
    """
    Discover one Service per Cron
    """
    for cron_name in section:
        yield Service(item=cron_name)

def check_cmdb_syncer_cron(item, params, section):
    """
    Check single Cron
    """
    state = State.OK
    data = section[item]
    if error := data.get('error'):
        yield Result(state=State.CRIT, summary=error)
        return
    yield Result(state=state, summary=f"Last Message: {data['last_message']}")
    yield Result(state=state, summary=f"Is running: {data['is_running']}")
    yield Result(state=state, summary=f"Next planned Run: {data['next_run']}")
    # First check errors
    if data['has_error']:
        yield Result(state=State.CRIT, summary="Has Error")
    # Job never started
    if not data['last_start']:
        yield Result(state=State.WARN, summary="Job never started")
        return
    last_start_obj = datetime.strptime(data['last_start'], "%Y-%m-%d %H:%M:%S")
    now = datetime.now()
    delta = now - last_start_obj
    delta_sec = delta.total_seconds()
    yield from check_levels(
                  value=delta_sec,
                  levels_upper=params.get('max_time_since_last_start', ('no_levels', None)),
                  label="Time since last run",
                  render_func=render.time_offset,
              )

agent_section_cmdb_syncer_cron = AgentSection(
    name = "cmdb_syncer_cron",
    parse_function = parse_cmdb_syncer_cron,
)


check_plugin_cmdb_syncer_cron = CheckPlugin(
    name = "cmdb_syncer_cron",
    sections = ["cmdb_syncer_cron"],
    service_name = "Cron %s",
    discovery_function = discover_cmdb_syncer_cron,
    check_function = check_cmdb_syncer_cron,
    check_default_parameters = {
        'max_time_since_last_start': ('no_levels', None),
    },
    check_ruleset_name = "cmdb_syncer_cron",
)
