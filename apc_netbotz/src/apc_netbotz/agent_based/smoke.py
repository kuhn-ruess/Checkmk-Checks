#!/usr/bin/env python3

"""
NetBotz Smoke Sensor Check Plugin for CheckMK (Agent Based API v2)
Based on Kuhn & Rue� GmbH netbotz_leak plugin
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


def parse_netbotz_smoke(string_table):
    map_state = {
        "-1": (State.UNKNOWN, "undefined"),
        "0": (State.OK, "noSmoke"),
        "1": (State.CRIT, "smokeDetected"),
    }

    parsed = {}

    for item, value, label in string_table:
        parsed[item] = {
            "label": label,
            "state": map_state.get(value, (State.UNKNOWN, f"unknown state ({value})")),
        }

    return parsed


snmp_section_netbotz_smoke = SimpleSNMPSection(
    name="netbotz_smoke",
    parse_function=parse_netbotz_smoke,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.52674.500.4.2.12.1",
        oids=[
            "1",  # NetBotz50-MIB::smokeSensorId
            "2",  # NetBotz50-MIB::smokeSensorValue
            "4",  # NetBotz50-MIB::smokeSensorLabel
        ],
    ),
    detect=startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.52674.500"),
)


def discover_netbotz_smoke(section):
    for item in section:
        yield Service(item=item)


def check_netbotz_smoke(item, section):
    if item not in section:
        yield Result(state=State.UNKNOWN, summary="Item not found")
        return

    sensor = section[item]
    yield Result(
        state=sensor["state"][0],
        summary=f"[{sensor['label']}], State: {sensor['state'][1]}",
    )


check_plugin_netbotz_smoke = CheckPlugin(
    name="netbotz_smoke",
    service_name="Smoke %s",
    discovery_function=discover_netbotz_smoke,
    check_function=check_netbotz_smoke,
)