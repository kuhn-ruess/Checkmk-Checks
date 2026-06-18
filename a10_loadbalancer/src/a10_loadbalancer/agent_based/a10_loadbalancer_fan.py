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


def parse_a10_loadbalancer_fan(string_table: StringTable) -> StringTable:
    return string_table


snmp_section_a10_loadbalancer_fan = SimpleSNMPSection(
    name="a10_loadbalancer_fan",
    parse_function=parse_a10_loadbalancer_fan,
    detect=equals(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.22610.1.3.22"),
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.22610.2.4.1.5.9.1",
        oids=[
            "2",  # axFanName
            "3",  # axFanStatus
            "4",  # axFanSpeed
        ],
    ),
)


def discover_a10_loadbalancer_fan(section: StringTable) -> DiscoveryResult:
    for line in section:
        yield Service(item=line[0].replace("Fan ", ""))


def check_a10_loadbalancer_fan(item: str, section: StringTable) -> CheckResult:
    states = {
        "0": "Failed",
        "4": "OK-fixed/high",
        "5": "OK-low/med",
        "6": "OK-med/med",
        "7": "OK-med/high",
        "-2": "not ready",
        "-1": "unknown",
    }
    for line in section:
        device_name, device_state, device_speed = line
        if device_name.replace("Fan ", "") == item:
            yield Result(
                state=State.OK,
                summary="State: {}, Speed: {} RPM".format(
                    states.get(device_state, device_state), device_speed
                ),
            )
            return


check_plugin_a10_loadbalancer_fan = CheckPlugin(
    name="a10_loadbalancer_fan",
    service_name="Fan %s",
    discovery_function=discover_a10_loadbalancer_fan,
    check_function=check_a10_loadbalancer_fan,
)
