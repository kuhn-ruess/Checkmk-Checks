#!/usr/bin/env python3

"""
Per-switch role and state for Cisco Catalyst stacks whose sysObjectID
is not covered by the built-in cisco_stack check
(.1.3.6.1.4.1.9.1.2871 / Catalyst 9500X).

Kuhn & Rueß GmbH
https://kuhn-ruess.de
"""

# .1.3.6.1.4.1.9.9.500.1.2.1.1.1  --> cswSwitchNumCurrent
# .1.3.6.1.4.1.9.9.500.1.2.1.1.3  --> cswSwitchRole
# .1.3.6.1.4.1.9.9.500.1.2.1.1.6  --> cswSwitchState

from cmk.agent_based.v2 import (
    CheckPlugin,
    Result,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    State,
    startswith,
)


ROLE = {
    "1": "master",
    "2": "member",
    "3": "not_member",
    "4": "standby",
}

ROLE_LABEL = {
    "master": "master",
    "member": "member",
    "not_member": "not member",
    "standby": "standby",
}

SWITCH_STATE = {
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


def parse_catalyst_switch_state(string_table):
    return {
        row[0]: {"switch_role": row[1], "switch_state": row[2]}
        for row in string_table
    }


snmp_section_catalyst_switch_state = SimpleSNMPSection(
    name="catalyst_switch_state",
    parse_function=parse_catalyst_switch_state,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.9.9.500.1.2.1.1",
        oids=["1", "3", "6"],
    ),
    detect=startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.9.1.2871"),
)


def discover_catalyst_switch_state(section):
    for switch_number, info in section.items():
        yield Service(
            item=switch_number,
            parameters={"switch_role": ROLE.get(info["switch_role"], info["switch_role"])},
        )


def check_catalyst_switch_state(item, params, section):
    data = section.get(item)
    if data is None:
        return

    switch_role = ROLE.get(data["switch_role"], data["switch_role"])
    expected_role = params.get("switch_role")
    if expected_role and switch_role != expected_role:
        yield Result(
            state=State.CRIT,
            summary=(
                f"Switch role is {ROLE_LABEL.get(switch_role, switch_role)}, "
                f"expected {ROLE_LABEL.get(expected_role, expected_role)}"
            ),
        )
    else:
        yield Result(
            state=State.OK,
            summary=f"Switch role is {ROLE_LABEL.get(switch_role, switch_role)}",
        )

    switch_state = data["switch_state"]
    if switch_state == "4":
        yield Result(
            state=State.OK,
            summary=f"Switch state is {SWITCH_STATE.get(switch_state, switch_state)}",
        )
    else:
        yield Result(
            state=State.CRIT,
            summary=f"Switch state is {SWITCH_STATE.get(switch_state, switch_state)}",
        )


check_plugin_catalyst_switch_state = CheckPlugin(
    name="catalyst_switch_state",
    service_name="State Switch %s",
    discovery_function=discover_catalyst_switch_state,
    check_function=check_catalyst_switch_state,
    check_default_parameters={},
    check_ruleset_name="catalyst_switch_state",
)
