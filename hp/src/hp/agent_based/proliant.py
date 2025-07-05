#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

# .1.3.6.1.4.1.232.11.1.3.0  1
# .1.3.6.1.4.1.232.11.2.14.1.1.5.0  "2009.05.18"
# .1.3.6.1.4.1.232.2.2.2.1.0  "GB8851CPPH


from cmk.agent_based.v2 import (
    Service,
    Result,
    State,
    SimpleSNMPSection,
    all_of,
    any_of,
    contains,
    exists,
    SNMPTree,
    CheckPlugin,
)

def parse_hp_proliant_general(string_table):
    return string_table

snmp_section_hp_proliant = SimpleSNMPSection(
    name = "hp_proliant",
    parse_function = parse_hp_proliant_general,
    fetch = SNMPTree(
        base = ".1.3.6.1.4.1.232",
        oids = [
            "11.1.3.0",
            "11.2.14.1.1.5.0",
            "2.2.2.1.0"
        ],
    ),
    detect = any_of(
        contains(".1.3.6.1.2.1.1.2.0", "8072.3.2.10"),
        contains(".1.3.6.1.2.1.1.2.0", "232.9.4.10"),
        all_of(
            contains(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.311.1.1.3.1.2"),
            exists(".1.3.6.1.4.1.232.11.1.3.0"),
        ),
    ),
)

def discover_hp_proliant_general(section):
    if section and len(section[0]) > 1 and section[0][0]:
        yield Service()


def check_hp_proliant_general(section):
    if not section:
        yield Result(state=State.UNKNOWN, summary="Data missing")

    else:
        map_states = {
            "0": (State.OK, "OK"),
            "1": (State.UNKNOWN, "unknown"),
            "2": (State.OK, "OK"),
            "3": (State.WARN, "degraded"),
            "4": (State.CRIT, "failed"),
        }

        status, firmware, serial_number = section[0]
        state, state_readable = map_states.get(status, (3, "unhandled[%s]" % status))
        yield Result(state=state, summary=f"Status: {state_readable}, Firmware: {firmware}, S/N: {serial_number}")

check_plugin_hp_proliant = CheckPlugin(
    name = "hp_proliant",
    service_name = "General Status",
    discovery_function = discover_hp_proliant_general,
    check_function = check_hp_proliant_general,
)
