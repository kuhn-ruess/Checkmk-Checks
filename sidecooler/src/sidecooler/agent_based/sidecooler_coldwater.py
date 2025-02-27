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

class SidecoolerColdwater(NamedTuple):
    water_supply: int
    water_return: int


def parse_sidecooler_coldwater(string_table):
    if not string_table:
        return None

    snmp_data = [int(s) / 10 for s in string_table[0]]

    return SidecoolerColdwater(*snmp_data)


def discover_sidecooler_coldwater(section):
    yield Service()


def check_sidecooler_coldwater(section):
    yield Result(state=State.OK, summary=f"Coldwater supply: {section.water_supply}°C")
    yield Metric(name="coldwater_supply", value=section.water_supply)

    yield Result(state=State.OK, summary=f"Coldwater return: {section.water_return}°C")
    yield Metric(name="coldwater_return", value=section.water_return)


snmp_section_sidecooler_coldwater = SimpleSNMPSection(
    name = "sidecooler_coldwater",
    parse_function = parse_sidecooler_coldwater,
    fetch = SNMPTree(
        base = ".1.3.6.1.4.1.46984.17.3",
        oids = [
            "10",   # SideCoolerMib::tempColdwaterSupply
            "11",   # SideCoolerMib::tempColdwaterReturn
        ],
    ),
    detect = exists(".1.3.6.1.4.1.46984.17.3.*"),
)


check_plugin_sidecooler_coldwater = CheckPlugin(
    name = "sidecooler_coldwater",
    service_name = "Sidecooler coldwater",
    discovery_function = discover_sidecooler_coldwater,
    check_function = check_sidecooler_coldwater,
)
