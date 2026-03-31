#!/usr/bin/env pytrhon3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""


from cmk.agent_based.v2 import (
    Service,
    Result,
    State,
    SimpleSNMPSection,
    SNMPTree,
    startswith,
    CheckPlugin,
)


def parse_netbotz_vibration(string_table):
    map_state = {
        "-1": (State.UNKNOWN, "undefined"),
        "0": (State.OK, "noVibration"),
        "1": (State.CRIT, "vibrationDetected"),
    }

    parsed = {}

    for item, value, label in string_table:
        parsed[item] = {
            "label": label,
            "state": map_state.get(value, (State.UNKNOWN, "unknown state")),
        }

    return parsed


snmp_section_netbotz_vibration = SimpleSNMPSection(
    name = "netbotz_vibration",
    parse_function = parse_netbotz_vibration,
    fetch = SNMPTree(
        base = ".1.3.6.1.4.1.52674.500.4.2.11.1",
        oids = [
            "1",   # NetBotz50-MIB::vibrationSensorId
            "2",   # NetBotz50-MIB::vibrationSensorValue
            "4",   # NetBotz50-MIB::vibrationSensorLabel
        ],
    ),
    detect = startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.52674.500"),
)


def discover_netbotz_vibration(section):
    for item in section.keys():
        yield Service(item=item)


def check_netbotz_vibration(item, section):
    if item not in section.keys():
        yield Result(state=State.UNKNOWN, summary="Item not found")

    else:
        yield Result(state=section[item]["state"][0], summary=f"[{section[item]['label']}], State: {section[item]['state'][1]}")


check_plugin_netbotz_vibration = CheckPlugin(
    name = "netbotz_vibration",
    service_name = "Vibration %s",
    discovery_function = discover_netbotz_vibration,
    check_function = check_netbotz_vibration,
)
