#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""


from cmk.agent_based.v2 import (
    Service,
    Result,
    State,
    SNMPSection,
    SNMPTree,
    contains,
    CheckPlugin,
)

def parse_gude_ats(string_table):
    return string_table

snmp_section_gude_ats = SNMPSection(
    name = "gude_ats",
    parse_function = parse_gude_ats,
    fetch = [
        SNMPTree(
            base = ".1.3.6.1.4.1.28507.41.1.5.11",
            oids = [
                "1.0", # Primary Power Available
                "2.0", # Secondary Power Available
                "4.0", # Current Channel
            ],
        ),
    ],
    detect = contains(".1.3.6.1.2.1.1.1.0", "UTE ATS"),
)

def discover_gude_ats(section):
    yield Service(
        parameters = {
            "inital" :section[0][2]
        }
    )

def check_gude_ats(params, section):
    mapping = {
        '1': "Primary",
        '2': "Secondary",
    }
    current = section[0][2]
    inital = params['inital']
    state = State.OK
    message = f"Current Input is {mapping[current]}"
    if inital != current:
        state = State.CRIT
        message += f" but should be {mapping[inital]}"
    yield Result(state=state, summary=message)


    inputs = [("Primary", section[0][0]),("Secondary", section[0][1])]

    for input_name, input_state in inputs:
        if input_state == '0':
            yield Result(state=State.CRIT, summary=f"Not redundant, {input_name} Input: Void")


check_plugin_gude_ats = CheckPlugin(
    name = "gude_ats",
    service_name = "Input Status",
    discovery_function = discover_gude_ats,
    check_function = check_gude_ats,
    check_default_parameters={},
)
