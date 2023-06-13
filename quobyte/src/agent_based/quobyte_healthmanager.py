#!/usr/bin/env python3

from .agent_based_api.v1 import (
    register,
    Result,
    Service,
    State,
)
def parse_quobyte_health(string_table):
    """
    Parse lines into dict
    """
    parsed = {}
    for line in string_table:
        parsed[line[0]] = line[1]
    return parsed

def discover_quobyte_healthmanager(section):
    """
    Discover one Service
    """
    yield Service()

def check_quobyte_healthmanager(params, section):
    """
    Check single Device
    """
    state = State.OK
    if section.get('system_health'):
        if section['system_health'] != 'HEALTHY':
            state = State.CRIT
        yield Result(state=state, summary=f"Device State: {section['system_health']}")
    yield Result(state=State.OK, summary=f"Defective Devices: {section['defective_devices']}")

register.agent_section(
    name="quobyte_healthmanager",
    parse_function=parse_quobyte_health,
)

register.check_plugin(
    name="quobyte_healthmanager",
    sections=["quobyte_healthmanager"],
    service_name="Healthmanager",
    discovery_function=discover_quobyte_healthmanager,
    check_function=check_quobyte_healthmanager,
    check_default_parameters={},
)
