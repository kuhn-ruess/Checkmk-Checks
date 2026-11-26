#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de

Smoke sensor check contributed by Kamil Jablonski (GitHub: Jarowitt)
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

MAP_STATE = {
    "-1": (State.UNKNOWN, "undefined"),
    "0": (State.OK, "noSmoke"),
    "1": (State.CRIT, "smokeDetected"),
}

MAP_ERROR = {
    "0": (State.OK, "normal"),
    "1": (State.OK, "info"),
    "2": (State.WARN, "warning"),
    "3": (State.CRIT, "error"),
    "4": (State.CRIT, "critical"),
    "5": (State.CRIT, "failure"),
}


def parse_netbotz_smoke(string_table):
    """Map the smoke sensor table to a dict keyed by sensor id."""
    return {
        item: {
            "label": label,
            "state": MAP_STATE.get(value, (State.UNKNOWN, f"unknown state ({value})")),
            "error": MAP_ERROR.get(error_status, (State.UNKNOWN, f"unknown error status ({error_status})")),
        }
        for item, value, error_status, label in string_table
    }


snmp_section_netbotz_smoke = SimpleSNMPSection(
    name="netbotz_smoke",
    parse_function=parse_netbotz_smoke,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.52674.500.4.2.12.1",
        oids=[
            "1",  # NetBotz50-MIB::smokeSensorId
            "2",  # NetBotz50-MIB::smokeSensorValue
            "3",  # NetBotz50-MIB::smokeSensorErrorStatus
            "4",  # NetBotz50-MIB::smokeSensorLabel
        ],
    ),
    detect=startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.52674.500"),
)


def discover_netbotz_smoke(section):
    """One service per smoke sensor."""
    for item in section:
        yield Service(item=item)


def check_netbotz_smoke(item, section):
    """Report the smoke state and a non normal error status."""
    if not (sensor := section.get(item)):
        return
    yield Result(state=sensor["state"][0], summary=f"[{sensor['label']}], State: {sensor['state'][1]}")
    if sensor["error"][0] != State.OK:
        yield Result(state=sensor["error"][0], summary=f"Error status: {sensor['error'][1]}")


check_plugin_netbotz_smoke = CheckPlugin(
    name="netbotz_smoke",
    service_name="Smoke %s",
    discovery_function=discover_netbotz_smoke,
    check_function=check_netbotz_smoke,
)
