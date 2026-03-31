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


def parse_netbotz_beacon(string_table):
    map_state = {
        "-1": (State.UNKNOWN, "undefined"),
        "0": (State.OK, "off"),
        "1": (State.CRIT, "on"),
    }

    parsed = {}

    for item, value, label in string_table:
        parsed[item] = {
            "label": label,
            "state": map_state.get(value, (State.UNKNOWN, "unknown state")),
        }

    return parsed


snmp_section_netbotz_beacon = SimpleSNMPSection(
    name = "netbotz_beacon",
    parse_function = parse_netbotz_beacon,
    fetch = SNMPTree(
        base = ".1.3.6.1.4.1.52674.500.4.2.14.1",
        oids = [
            "1",   # NetBotz50-MIB::beaconSensorId
            "2",   # NetBotz50-MIB::beaconSensorValue
            "4",   # NetBotz50-MIB::beaconSensorLabel
        ],
    ),
    detect = startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.52674.500"),
)


def discover_netbotz_beacon(section):
    for item in section.keys():
        yield Service(item=item)


def check_netbotz_beacon(item, section):
    if item not in section.keys():
        yield Result(state=State.UNKNOWN, summary="Item not found")

    else:
        yield Result(state=section[item]["state"][0], summary=f"[{section[item]['label']}], State: {section[item]['state'][1]}")


check_plugin_netbotz_beacon = CheckPlugin(
    name = "netbotz_beacon",
    service_name = "Beacon %s",
    discovery_function = discover_netbotz_beacon,
    check_function = check_netbotz_beacon,
)
