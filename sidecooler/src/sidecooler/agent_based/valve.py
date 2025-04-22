#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from typing import NamedTuple

from cmk.agent_based.v2 import (
    Service,
    Result,
    State,
    Metric,
    SimpleSNMPSection,
    SNMPTree,
    exists,
    CheckPlugin,
)

class SidecoolerValve(NamedTuple):
    valve_set: float
    valve_current: float


def parse_sidecooler_valve(string_table):
    if not string_table:
        return None

    snmp_data = [float(s) / 10 for s in string_table[0]]

    return SidecoolerValve(*snmp_data)


def discover_sidecooler_valve(section):
    yield Service()


def check_sidecooler_valve(section):
    yield Result(state=State.OK, summary=f"Set: {section.valve_set}%")
    yield Metric(name="valve_set", value=section.valve_set, boundaries=(0, 100))

    yield Result(state=State.OK, summary=f"Current: {section.valve_current}%")
    yield Metric(name="valve_current", value=section.valve_current, boundaries=(0, 100))


snmp_section_sidecooler_coldwater = SimpleSNMPSection(
    name = "sidecooler_valve",
    parse_function = parse_sidecooler_valve,
    fetch = SNMPTree(
        base = ".1.3.6.1.4.1.46984.17.3",
        oids = [
            "75",   # SideCoolerMib::valveSet
            "76",   # SideCoolerMib::valveActual
        ],
    ),
    detect = exists(".1.3.6.1.4.1.46984.17.3.*"),
)


check_plugin_sidecooler_valve = CheckPlugin(
    name = "sidecooler_valve",
    service_name = "Sidecooler valve",
    discovery_function = discover_sidecooler_valve,
    check_function = check_sidecooler_valve,
)
