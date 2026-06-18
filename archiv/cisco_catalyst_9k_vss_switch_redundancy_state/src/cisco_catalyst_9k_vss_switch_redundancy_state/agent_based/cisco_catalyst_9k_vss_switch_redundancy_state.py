#!/usr/bin/env python3

from cmk.agent_based.v2 import (
    CheckPlugin,
    Result,
    Service,
    SNMPSection,
    SNMPTree,
    StringTable,
    startswith,
    State,
)


def parse_cisco_catalyst_9k_vss_switch_redundancy_state(string_table: StringTable):
    parsed = {}
    for line in string_table:
        parsed[line[0]] = {
            "switch_role": line[1],
            "switch_state": line[2],
        }
    return parsed


snmp_section_cisco_catalyst_9k_vss_switch_redundancy_state = SNMPSection(
    name="cisco_catalyst_9k_vss_switch_redundancy_state",
    parse_function=parse_cisco_catalyst_9k_vss_switch_redundancy_state,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.9.9.500.1.2.1.1",
        oids=[
            "1",  # CISCO-STACKWISE-MIB::cswSwitchNumCurrent
            "3",  # CISCO-STACKWISE-MIB::cswSwitchRole
            "6",  # CISCO-STACKWISE-MIB::cswSwitchState
        ],
    ),
    detect=startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.9.1.2871"),
)


def discover_cisco_catalyst_9k_vss_switch_redundancy_state(section):
    for switch_number, info in section.items():
        yield Service(item=switch_number, parameters={"switch_role": info["switch_role"]})


def check_cisco_catalyst_9k_vss_switch_redundancy_state(item, params, section):
    switch_roles = {
        "1": "master",
        "2": "member",
        "3": "not member",
        "4": "standby",
    }

    switch_states = {
        "1": "waiting",
        "2": "progressing",
        "3": "added",
        "4": "ready",
        "5": "SDM mismatch",
        "6": "version mismatch",
        "7": "feature mismatch",
        "8": "new master init",
        "9": "provisioned",
        "10": "invalid",
        "11": "removed",
    }

    if item not in section:
        return

    switch_role = section[item]["switch_role"]
    expected_role = params.get("switch_role")
    # The ruleset stores the role as "role_<n>", the discovery as raw "<n>".
    if expected_role:
        expected_role = expected_role.removeprefix("role_")
    if expected_role and switch_role != expected_role:
        yield Result(
            state=State.CRIT,
            summary="Switch role is " + switch_roles[switch_role]
            + ", expected " + switch_roles[expected_role],
        )
    else:
        yield Result(state=State.OK, summary="Switch role is " + switch_roles[switch_role])

    switch_state = section[item]["switch_state"]
    if switch_state == "4":
        yield Result(state=State.OK, summary="Switch state is " + switch_states[switch_state])
    else:
        yield Result(state=State.CRIT, summary="Switch state is " + switch_states[switch_state])


check_plugin_cisco_catalyst_9k_vss_switch_redundancy_state = CheckPlugin(
    name="cisco_catalyst_9k_vss_switch_redundancy_state",
    sections=["cisco_catalyst_9k_vss_switch_redundancy_state"],
    service_name="State Switch %s",
    discovery_function=discover_cisco_catalyst_9k_vss_switch_redundancy_state,
    check_function=check_cisco_catalyst_9k_vss_switch_redundancy_state,
    check_default_parameters={},
    check_ruleset_name="cisco_catalyst_9k_vss_switch_redundancy_state",
)
