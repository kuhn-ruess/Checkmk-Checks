#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from typing import NamedTuple

from cmk.agent_based.v2 import (
    CheckPlugin,
    Metric,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    all_of,
    check_levels,
    exists,
    startswith,
)


class PaloAltoTunnels(NamedTuple):
    active_tunnels: int
    max_tunnels: int


def parse_palo_alto_gp_tunnels(string_table):
    if not string_table:
        return None
    return PaloAltoTunnels(*(int(s) for s in string_table[0]))


snmp_section_palo_alto_gp_tunnels = SimpleSNMPSection(
    name="palo_alto_gp_tunnels",
    parse_function=parse_palo_alto_gp_tunnels,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.25461.2.1.2.5.1",
        oids=["3", "2"],
    ),
    detect=all_of(
        startswith(".1.3.6.1.2.1.1.1.0", "Palo Alto"),
        exists(".1.3.6.1.4.1.25461.2.1.2.5.1.*"),
    ),
)


def discover_palo_alto_gp_tunnels(section):
    yield Service()


def check_palo_alto_gp_tunnels(params, section):
    yield Metric(
        "active_gp_tunnels",
        section.active_tunnels,
        boundaries=(0, section.max_tunnels),
    )
    remaining = section.max_tunnels - section.active_tunnels
    yield from check_levels(
        value=remaining,
        levels_lower=params["levels_remaining"],
        render_func=lambda v: (
            f"{remaining} free slot(s), {section.active_tunnels} of "
            f"{section.max_tunnels} possible GlobalProtect Tunnels used"
        ),
        label="Remaining",
    )


check_plugin_palo_alto_gp_tunnels = CheckPlugin(
    name="palo_alto_gp_tunnels",
    service_name="Palo Alto GlobalProtect Tunnels",
    discovery_function=discover_palo_alto_gp_tunnels,
    check_function=check_palo_alto_gp_tunnels,
    check_ruleset_name="palo_alto_gp_tunnels",
    check_default_parameters={"levels_remaining": ("fixed", (50, 15))},
)
