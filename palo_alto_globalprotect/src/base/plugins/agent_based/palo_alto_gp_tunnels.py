#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import NamedTuple, Optional
from .agent_based_api.v1.type_defs import (
    CheckResult,
    DiscoveryResult,
    StringTable,
)

from .agent_based_api.v1 import (
    all_of,
    startswith,
    exists,
    Metric,
    register,
    Result,
    Service,
    SNMPTree,
    State,
)


class PaloAtoTunnels(NamedTuple):
    active_tunnels: int
    max_tunnels: int

def parse_palo_alto_tunnels(string_table: StringTable) -> Optional[PaloAtoTunnels]:
    if not string_table:
        return None
    snmp_data = [int(s) for s in string_table[0]]
    return PaloAtoTunnels(*snmp_data)



register.snmp_section(
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


def discover_palo_alto_tunnels(section: PaloAtoTunnels) -> DiscoveryResult:
    yield Service()


def check_palo_alto_tunnels(section: PaloAtoTunnels) -> CheckResult:
    state = State.CRIT
    yield Metric('active_gp_tunnels',
                 section.active_tunnels,
                 boundaries=(0, section.max_tunnels))

    if section.active_tunnels < section.max_tunnels:
        state = State.OK
    yield Result(
        state=state,
        summary=f"Currently {section.active_tunnels} of {section.max_tunnels} Possible GlobalProtect Tunnels used",
    )


register.check_plugin(
    name="palo_alto_gp_tunnels",
    service_name="Palo Alto GlobalProtect Tunnels",
    discovery_function=discover_palo_alto_tunnels,
    check_function=check_palo_alto_tunnels,
)
