#!/usr/bin/env python3

from cmk.agent_based.v2 import (
    CheckPlugin,
    Result,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    StringTable,
    startswith,
    State,
)


def parse_cisco_distr_stack_port(string_table: StringTable) -> StringTable:
    return string_table


snmp_section_cisco_distr_stack_port = SimpleSNMPSection(
    name="cisco_distr_stack_port",
    parse_function=parse_cisco_distr_stack_port,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.9.9.500.1.2.4.1",
        oids=[
            "1",  # cswDistrStackPhyPort
            "2",  # cswDistrStackPhyPortOperStatus
            "3",  # cswDistrStackPhyPortNbr
        ],
    ),
    detect=startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.9.1.2871"),
)


def discover_cisco_distr_stack_port(section: StringTable):
    for line in section:
        if line[0]:
            yield Service(item=line[0])


def check_cisco_distr_stack_port(item, section: StringTable):
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


check_plugin_cisco_distr_stack_port = CheckPlugin(
    name="cisco_distr_stack_port",
    sections=["cisco_distr_stack_port"],
    service_name="Distributed stack port status %s",
    discovery_function=discover_cisco_distr_stack_port,
    check_function=check_cisco_distr_stack_port,
)
