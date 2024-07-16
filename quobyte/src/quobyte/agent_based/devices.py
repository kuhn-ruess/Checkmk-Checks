#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    Result,
    Service,
    State,
    get_value_store,
)
from cmk.plugins.lib.df import df_check_filesystem_single


def parse_quobyte_devices(string_table):
    """
    Parse Device Data to Dict
    """
    parsed = {}
    for line in string_table:
        if line[0] == 'device_id':
            current_device = line[1]
        else:
            parsed.setdefault(current_device, {})
            parsed[current_device][line[0]]=line[1]
    return parsed


def discover_quobyte_devices(section):
    """
    Discover one Service per Device
    """
    for device_id in section:
        yield Service(item=device_id)


def check_quobyte_devices(item, params, section):
    """
    Check single Device
    """
    try:
        device = section[item]
    except:
        yield Result(state=State.CRIT, summary="Device not found anymore")
        return

    yield Result(state=State.OK, summary=f"Mount Point: {device['current_mount_path']}")
    yield Result(state=State.OK, summary=f"Serial Number: {device['device_serial_number']}")
    if "device_label" in device:
        yield Result(state=State.OK, summary=f"Label: {device['device_label']}")

    # Check Device Mode
    state = State.OK
    if device['device_status'] in params['modes']['critical']:
        state = State.CRIT
    elif device['device_status'] in params['modes']['warning']:
        state  = State.WARN
    yield Result(state=state, summary=f"Device Mode: {device['device_status']}")

    if device['health_status'] not in  ['HEALTHY', 'DECOMMISSIONED']:
        yield Result(state=State.CRIT, summary=f"Health Status: {device['health_status']}")

    # Check Usage
    yield from df_check_filesystem_single(
        get_value_store(),
        item,
        float(device['total_disk_space_bytes'])/1024/1024,
        (float(device['total_disk_space_bytes']) - float(device["used_disk_space_bytes"]))/1024/1024,
        0,
        None,
        None,
        {'levels' : params['usage_levels'],
         'trend_range': 1,
        },
    )


agent_section_quobyte_devices = AgentSection(
    name = "quobyte_devices",
    parse_function = parse_quobyte_devices,
)


check_plugin_quobyte_devices = CheckPlugin(
    name = "quobyte_devices",
    sections = ["quobyte_devices"],
    service_name = "Device %s",
    discovery_function = discover_quobyte_devices,
    check_function = check_quobyte_devices,
    check_default_parameters = {
        'usage_levels': (90.0, 95.0),
        'modes' : {
            'warning' : ['DECOMMISSIONED', 'DRAIN', 'REGENERATE'],
            'critical' : ['OFFLINE'],
        }
    },
    check_ruleset_name = "quobyte_devices",
)
