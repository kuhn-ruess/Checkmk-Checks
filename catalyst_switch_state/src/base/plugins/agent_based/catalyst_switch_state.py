#!/usr/bin/env python3

from .agent_based_api.v1 import (
    register,
    Result,
    Service,
    SNMPTree,
    startswith,
    State,
)

def parse_catalyst_switch_state(string_table):
    parsed = {}
    for line in string_table:
        parsed[line[0]] = {
            "switch_role" : line[1],
            "switch_state" : line[2],
        }
    return parsed


register.snmp_section(
    name="catalyst_switch_state",
    parse_function=parse_catalyst_switch_state,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.9.9.500.1.2.1.1",
        oids=[
            "1", # CISCO-STACKWISE-MIB::cswSwitchNumCurrent
            "3", # CISCO-STACKWISE-MIB::cswSwitchRole
            "6", # CISCO-STACKWISE-MIB::cswSwitchState
        ],
    ),
    detect=startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.9.1.2871"),
)


def discover_catalyst_switch_state(section):
    for switch_number, info in section.items():
        yield Service(item=switch_number, parameters={"switch_role" : info["switch_role"]})


def check_catalyst_switch_state(item, params, section):
    switch_roles = {
        "1" : "master",
        "2" : "member",
        "3" : "not member",
        "4" : "standby",
    }

    switch_states = {
        "1" : "waiting",
        "2" : "progressing",
        "3" : "added",
        "4" : "ready",
        "5" : "SDM mismatch",
        "6" : "version mismatch",
        "7" : "feature mismatch",
        "8" : "new master init",
        "9" : "provisioned",
        "10" : "invalid",
        "11" : "removed",
    }

    switch_role = section[item]["switch_role"]
    if params.get("switch_role") and switch_role != params["switch_role"]:
        yield Result(state=State.CRIT, summary="Switch role is " + switch_roles[switch_role] + ", expected " + switch_roles[params["switch_role"]])
    else:
        yield Result(state=State.OK, summary="Switch role is " + switch_roles[switch_role])

    switch_state = section[item]["switch_state"]
    if switch_state == "4":
        yield Result(state=State.OK, summary="Switch state is " + switch_states[switch_state])
    else:
        yield Result(state=State.CRIT, summary="Switch state is " + switch_states[switch_state])


register.check_plugin(
    name="catalyst_switch_state",
    sections=["catalyst_switch_state"],
    service_name="State Switch %s",
    discovery_function=discover_catalyst_switch_state,
    check_function=check_catalyst_switch_state,
    check_default_parameters={},
    check_ruleset_name="catalyst_switch_state",
)
