#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de

Motion sensor check contributed by Kamil Jablonski (GitHub: Jarowitt)
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

MAP_ERROR = {
    "0": (State.OK, "normal"),
    "1": (State.OK, "info"),
    "2": (State.WARN, "warning"),
    "3": (State.CRIT, "error"),
    "4": (State.CRIT, "critical"),
    "5": (State.CRIT, "failure"),
}


def parse_netbotz_motion(string_table):
    """Map the motion sensor table to a dict keyed by sensor id."""
    return {
        item: {
            "value": value,
            "label": label,
            "enclosure": enclosure,
            "error": MAP_ERROR.get(error_status, (State.UNKNOWN, f"unknown error status ({error_status})")),
        }
        for item, value, error_status, label, enclosure in string_table
    }


snmp_section_netbotz_motion = SimpleSNMPSection(
    name="netbotz_motion",
    parse_function=parse_netbotz_motion,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.52674.500.4.2.3.1",
        oids=[
            "1",  # NetBotz50-MIB::motionSensorId
            "2",  # NetBotz50-MIB::motionSensorValue
            "3",  # NetBotz50-MIB::motionSensorErrorStatus
            "4",  # NetBotz50-MIB::motionSensorLabel
            "5",  # NetBotz50-MIB::motionSensorEncId
        ],
    ),
    detect=startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.52674.500"),
)


def discover_netbotz_motion(section):
    """One service per motion sensor."""
    for item in section:
        yield Service(item=item)


def check_netbotz_motion(item, params, section):
    """Report the motion state with the configured state for detected motion."""
    if not (sensor := section.get(item)):
        return
    prefix = f"[{sensor['label']}] ({sensor['enclosure']}), State"
    if sensor["value"] == "0":
        yield Result(state=State.OK, summary=f"{prefix}: noMotion")
    elif sensor["value"] == "1":
        yield Result(state=State(params["motion_detected"]), summary=f"{prefix}: motionDetected")
    else:
        yield Result(state=State.UNKNOWN, summary=f"{prefix}: undefined ({sensor['value']})")
    if sensor["error"][0] != State.OK:
        yield Result(state=sensor["error"][0], summary=f"Error status: {sensor['error'][1]}")


check_plugin_netbotz_motion = CheckPlugin(
    name="netbotz_motion",
    service_name="Motion %s",
    discovery_function=discover_netbotz_motion,
    check_function=check_netbotz_motion,
    check_ruleset_name="netbotz_motion",
    check_default_parameters={"motion_detected": 0},
)
