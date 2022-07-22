#!/usr/bin/env python3

from .agent_based_api.v1 import (
    register,
    Result,
    Service,
    SNMPTree,
    startswith,
    State,
)

import pprint

register.snmp_section(
    name="cisco_distr_stack_port",
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.9.9.500.1.2.4.1",
        oids=[
            "1", # cswDistrStackPhyPort
            "2", # cswDistrStackPhyPortOperStatus
            "3", # cswDistrStackPhyPortNbr
        ],
    ),
    detect=startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.9.1.2871"),
)


def discover_cisco_distr_stack_port(section):
    for line in section:
        if line[0]:
            yield Service(item=line[0])


def check_cisco_distr_stack_port(item, section):
    for line in section:
        if line[0] == item:
            if line[1] == "1":
                yield Result(state=State.OK, summary="Port state: up")
            elif line[1] == "2":
                yield Result(state=State.CRIT, summary="Port state: down")
        if line[2] == item:
            if line[1] == "1":
                yield Result(state=State.OK, summary="Neighbor port state: up")
            elif line[1] == "2":
                yield Result(state=State.CRIT, summary="Neighbor port state: down")



register.check_plugin(
    name="cisco_distr_stack_port",
    sections=["cisco_distr_stack_port"],
    service_name="Distributed stack port status %s",
    discovery_function=discover_cisco_distr_stack_port,
    check_function=check_cisco_distr_stack_port,
)
