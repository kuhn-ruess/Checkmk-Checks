#!/usr/bin/env python
from .agent_based_api.v1 import *

def discover_gude_ats(section):
    yield Service(parameters={
                    "inital" :section[0][2]
                 })

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

register.check_plugin(
    name = "gude_ats",
    service_name = "Input Status",
    discovery_function = discover_gude_ats,
    check_function = check_gude_ats,
    check_default_parameters={},
)

register.snmp_section(
    name = "gude_ats",
    detect = contains(".1.3.6.1.2.1.1.1.0", "UTE ATS"),
    fetch = SNMPTree(
        base = '.1.3.6.1.4.1.28507.41.1.5.11',
        oids = [
            '1.0', # Primary Power Available
            '2.0', # Secondary Power Available
            '4.0', # Current Channel
        ],
    ),
)
