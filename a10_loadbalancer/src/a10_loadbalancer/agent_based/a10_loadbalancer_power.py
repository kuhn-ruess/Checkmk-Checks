#!/usr/bin/env python3
# https://mibs.observium.org/mib/A10-AX-MIB/

from cmk.agent_based.v2 import (
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Result,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    State,
    StringTable,
    equals,
)


def parse_a10_loadbalancer_power(string_table: StringTable) -> StringTable:
    return string_table


snmp_section_a10_loadbalancer_power = SimpleSNMPSection(
    name="a10_loadbalancer_power",
    parse_function=parse_a10_loadbalancer_power,
    detect=equals(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.22610.1.3.22"),
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.22610.2.4.1.5.12.1",
        oids=[
            "2",  # axPowerSupplyName
            "3",  # axPowerSupplyStatus
        ],
    ),
)


def discover_a10_loadbalancer_power(section: StringTable) -> DiscoveryResult:
    for line in section:
        if line[1] == "1":
            yield Service(item=line[0])


def check_a10_loadbalancer_power(item: str, section: StringTable) -> CheckResult:
    states = {
        "0": "off",
        "1": "on",
        "2": "absent",
        "-1": "unknown",
    }
    for line in section:
        supply_state = line[1]
        if line[0] == item:
            if supply_state == "1":
                state = State.OK
            elif supply_state == "2":
                state = State.CRIT
            else:
                state = State.WARN
            yield Result(
                state=state,
                summary="State: {}".format(states.get(supply_state, supply_state)),
            )
            return


check_plugin_a10_loadbalancer_power = CheckPlugin(
    name="a10_loadbalancer_power",
    service_name="Power Supply %s",
    discovery_function=discover_a10_loadbalancer_power,
    check_function=check_a10_loadbalancer_power,
)
