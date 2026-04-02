#!/usr/bin/env python3

from cmk.agent_based.v2 import (
    CheckPlugin,
    Result,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    State,
    StringTable,
    matches,
)


def parse_cisco_vpc_role(string_table: StringTable) -> StringTable:
    return string_table


ROLE_VALUE_TO_NAME = {
    "1": "primary_secondary",
    "2": "primary_primary",
    "3": "secondary_primary",
    "4": "secondary_secondary",
    "5": "no_peer_device",
}

ROLE_LABELS = {
    "primary_secondary": "primary, and operational secondary",
    "primary_primary": "primary, and operational primary",
    "secondary_primary": "secondary, and operational primary",
    "secondary_secondary": "secondary, and operational secondary",
    "no_peer_device": "no peer device",
}


snmp_section_cisco_vpc_role = SimpleSNMPSection(
    name="cisco_vpc_role",
    parse_function=parse_cisco_vpc_role,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.9.9.807.1.2.1.1",
        oids=[
            "2",  # CISCO-VPC-MIB::cVpcRoleStatus
            "3",  # CISCO-VPC-MIB::cVpcDualActiveDetectionStatus
        ],
    ),
    detect=matches(".1.3.6.1.2.1.1.2.0", r".1.3.6.1.4.1.9.12.3.1.3.\d{4}"),
)


def discover_cisco_vpc_role(section: StringTable):
    if section and section[0]:
        yield Service(parameters={"switch_role": ROLE_VALUE_TO_NAME.get(section[0][0])})


def check_cisco_vpc_role(params, section: StringTable):
    if not section or not section[0]:
        return

    current_role = ROLE_VALUE_TO_NAME.get(section[0][0])
    role_name = ROLE_LABELS.get(current_role, "Unknown role: " + section[0][0])
    expected_role = params.get("switch_role")
    if expected_role and current_role != expected_role:
        expected_role_name = ROLE_LABELS.get(expected_role, "Unknown role: " + expected_role)
        yield Result(state=State.WARN, summary=role_name + " (expected " + expected_role_name + ")")
    else:
        yield Result(state=State.OK, summary=role_name)
    if len(section[0]) > 1 and section[0][1] == "2":
        yield Result(state=State.OK, summary="no dual active detected")
    else:
        yield Result(state=State.CRIT, summary="dual active detected")


check_plugin_cisco_vpc_role = CheckPlugin(
    name="cisco_vpc_role",
    service_name="VPC Role",
    discovery_function=discover_cisco_vpc_role,
    check_function=check_cisco_vpc_role,
    check_default_parameters={},
    check_ruleset_name="cisco_vpc_role",
)
