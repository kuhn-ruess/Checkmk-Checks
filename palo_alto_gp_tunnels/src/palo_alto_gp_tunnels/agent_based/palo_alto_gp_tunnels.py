#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from typing import NamedTuple

from cmk.agent_based.v2 import (
    all_of,
    startswith,
    exists,
    Metric,
    CheckPlugin,
    Result,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    State,
)


class PaloAltoTunnels(NamedTuple):
    active_tunnels: int
    max_tunnels: int


def parse_palo_alto_tunnels(string_table):
    if not string_table:
        return None
    snmp_data = [int(s) for s in string_table[0]]
    return PaloAltoTunnels(*snmp_data)


snmp_section_palo_alto_gp_tunnels = SimpleSNMPSection(
    name="palo_alto_gp_tunnels",
    parse_function=parse_palo_alto_tunnels,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.25461.2.1.2.5.1",
        oids=["3", "2"],
    ),
    detect=all_of(
        startswith(".1.3.6.1.2.1.1.1.0", 'Palo Alto'),
        exists(".1.3.6.1.4.1.25461.2.1.2.5.1.*"),
    ),
)


def discover_palo_alto_tunnels(section):
    yield Service()


def check_palo_alto_tunnels(section):
    yield Metric('active_gp_tunnels',
                 section.active_tunnels,
                 boundaries=(0, section.max_tunnels))

    text = f"Currently {section.active_tunnels} of {section.max_tunnels} Possible GlobalProtect Tunnels used"

    if section.active_tunnels >= section.max_tunnels - 15:
        yield Result(state=State.CRIT, summary=text)
    elif section.active_tunnels >= section.max_tunnels - 50:
        yield Result(state=State.WARN, summary=text)
    else:
        yield Result(state=State.OK, summary=text)


check_plugin_palo_alto_gp_tunnels = CheckPlugin(
    name="palo_alto_gp_tunnels",
    service_name="Palo Alto GlobalProtect Tunnels",
    discovery_function=discover_palo_alto_tunnels,
    check_function=check_palo_alto_tunnels,
)
