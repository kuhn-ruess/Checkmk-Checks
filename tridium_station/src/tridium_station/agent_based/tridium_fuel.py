#!/usr/bin/env python3
# Written by Bastian Kuhn (mail@bastian-kuhn.de)
# Tridium Niagara Station - fuel tank check

from cmk.agent_based.v2 import (
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Metric,
    Result,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    State,
    StringTable,
    startswith,
)

_MAX_FUEL = 6000.0


def parse_tridium_fuel(string_table: StringTable) -> StringTable:
    return string_table


snmp_section_tridium_fuel = SimpleSNMPSection(
    name="tridium_fuel",
    parse_function=parse_tridium_fuel,
    detect=startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.4131.1"),
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.4131.1.6.15.1.1.3",
        oids=[
            "2",  # left
            "4",  # consumption
        ],
    ),
)


def discover_tridium_fuel(section: StringTable) -> DiscoveryResult:
    if section:
        yield Service()


def check_tridium_fuel(params: dict, section: StringTable) -> CheckResult:
    if not section:
        return

    consumption = float(section[0][0])
    last_consumption = float(section[0][1])

    left = consumption + _MAX_FUEL

    state = State.OK
    levels = params.get("levels")
    if levels and levels[0] == "fixed":
        warn, crit = levels[1]
        if left <= crit:
            state = State.CRIT
        elif left <= warn:
            state = State.WARN

    yield Result(state=state, summary="Fuel left: %s ltrs." % left)
    yield Metric("usage", consumption)
    yield Metric("last_cons", last_consumption)
    yield Metric("level", left)


check_plugin_tridium_fuel = CheckPlugin(
    name="tridium_fuel",
    service_name="TR Fuel",
    discovery_function=discover_tridium_fuel,
    check_function=check_tridium_fuel,
    check_default_parameters={"levels": ("no_levels", None)},
    check_ruleset_name="tridium_fuel",
)
