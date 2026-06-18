#!/usr/bin/env python3
# https://mibs.observium.org/mib/A10-AX-MIB/

from cmk.agent_based.v2 import (
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    get_value_store,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    StringTable,
    equals,
)
from cmk.plugins.lib.temperature import check_temperature, TempParamDict


def parse_a10_loadbalancer_temp(string_table: StringTable) -> StringTable:
    return string_table


snmp_section_a10_loadbalancer_temp = SimpleSNMPSection(
    name="a10_loadbalancer_temp",
    parse_function=parse_a10_loadbalancer_temp,
    detect=equals(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.22610.1.3.22"),
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.22610.2.4.1.5",
        oids=[
            "1",  # AxSyshwPhySystemTemp
        ],
    ),
)


def discover_a10_loadbalancer_temp(section: StringTable) -> DiscoveryResult:
    if section and section[0]:
        yield Service(item="System")


def check_a10_loadbalancer_temp(
    item: str, params: TempParamDict, section: StringTable
) -> CheckResult:
    if not section or not section[0]:
        return
    temp = int(section[0][0])
    yield from check_temperature(
        temp,
        params,
        unique_name="a10_loadbalancer_temp_%s" % item,
        value_store=get_value_store(),
    )


check_plugin_a10_loadbalancer_temp = CheckPlugin(
    name="a10_loadbalancer_temp",
    service_name="Temperature %s",
    discovery_function=discover_a10_loadbalancer_temp,
    check_function=check_a10_loadbalancer_temp,
    check_default_parameters={},
    check_ruleset_name="temperature",
)
