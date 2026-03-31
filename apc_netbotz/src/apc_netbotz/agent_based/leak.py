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


def parse_netbotz_leak(string_table):
    map_state = {
        "-1": (State.UNKNOWN, "undefined"),
        "0": (State.OK, "noLeak"),
        "1": (State.CRIT, "leakDetected"),
    }

    parsed = {}

    for item, value, label in string_table:
        parsed[item] = {
            "label": label,
            "state": map_state.get(value, (State.UNKNOWN, "unknown state")),
        }

    return parsed


snmp_section_netbotz_leak = SimpleSNMPSection(
    name = "netbotz_leak",
    parse_function = parse_netbotz_leak,
    fetch = SNMPTree(
        base = ".1.3.6.1.4.1.52674.500.4.2.13.1",
        oids = [
            "1",   # NetBotz50-MIB::leakSensorId
            "2",   # NetBotz50-MIB::leakSensorValue
            "4",   # NetBotz50-MIB::leakSensorLabel
        ],
    ),
    detect = startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.52674.500"),
)


def discover_netbotz_leak(section):
    for item in section.keys():
        yield Service(item=item)


def check_netbotz_leak(item, section):
    if item not in section.keys():
        yield Result(state=State.UNKNOWN, summary="Item not found")

    else:
        yield Result(state=section[item]["state"][0], summary=f"[{section[item]['label']}], State: {section[item]['state'][1]}")


check_plugin_netbotz_leak = CheckPlugin(
    name = "netbotz_leak",
    service_name = "Leak %s",
    discovery_function = discover_netbotz_leak,
    check_function = check_netbotz_leak,
)
