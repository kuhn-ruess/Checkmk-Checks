#!/usr/bin/env python3

"""
NetBotz Motion Sensor Check Plugin for CheckMK (Agent Based API v2)
Based on Kuhn & Rueï¿½ GmbH netbotz_leak plugin
by kamil.jablonski@gmail.com
"""

from cmk.agent_based.v2 import (
    CheckPlugin,
    Result,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    State,
    startswith,
)


def parse_netbotz_motion(string_table):
    map_state = {
        "-1": (State.UNKNOWN, "undefined"),
        "0": (State.OK, "noMotion"),
        "1": (State.WARN, "motionDetected"),
    }

    map_error = {
        "0": (State.OK, "normal"),
        "1": (State.OK, "info"),
        "2": (State.WARN, "warning"),
        "3": (State.CRIT, "error"),
        "4": (State.CRIT, "critical"),
        "5": (State.CRIT, "failure"),
    }

    parsed = {}

    for item, value, error_status, label, camera_id in string_table:
        parsed[item] = {
            "label": label,
            "camera_id": camera_id,
            "state": map_state.get(value, (State.UNKNOWN, f"unknown state ({value})")),
            "error": map_error.get(error_status, (State.UNKNOWN, f"error code {error_status}")),
        }

    return parsed


snmp_section_netbotz_motion = SimpleSNMPSection(
    name="netbotz_motion",
    parse_function=parse_netbotz_motion,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.52674.500.4.2.3.1",
        oids=[
            "1",  # motionSensorId
            "2",  # motionSensorValue (0 = no-motion)
            "3",  # motionSensorErrorStatus (0 = normal)
            "4",  # motionSensorLabel
            "5",  # motionSensorEnclosureId (np. camera-52)
        ],
    ),
    detect=startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.52674.500"),
)


def discover_netbotz_motion(section):
    for item in section:
        yield Service(item=item)


def check_netbotz_motion(item, section):
    if item not in section:
        yield Result(state=State.UNKNOWN, summary="Item not found")
        return

    sensor = section[item]
    yield Result(
        state=sensor["state"][0],
        summary=f"[{sensor['label']}] ({sensor['camera_id']}), State: {sensor['state'][1]}",
    )

    if sensor["error"][0] != State.OK:
        yield Result(
            state=sensor["error"][0],
            summary=f"Error status: {sensor['error'][1]}",
        )


check_plugin_netbotz_motion = CheckPlugin(
    name="netbotz_motion",
    service_name="Motion %s",
    discovery_function=discover_netbotz_motion,
    check_function=check_netbotz_motion,
)