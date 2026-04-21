#!/usr/bin/env python3

"""
Operational status for Cisco Distributed Stack ports.

Kuhn & Rueß GmbH
https://kuhn-ruess.de
"""

# .1.3.6.1.4.1.9.9.500.1.2.4.1.1  --> cswDistrStackPhyPort
# .1.3.6.1.4.1.9.9.500.1.2.4.1.2  --> cswDistrStackPhyPortOperStatus
# .1.3.6.1.4.1.9.9.500.1.2.4.1.3  --> cswDistrStackPhyPortNbr

from cmk.agent_based.v2 import (
    CheckPlugin,
    Result,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    State,
    startswith,
)


def parse_cisco_distr_stack_port(string_table):
    return string_table or None


snmp_section_cisco_distr_stack_port = SimpleSNMPSection(
    name="cisco_distr_stack_port",
    parse_function=parse_cisco_distr_stack_port,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.9.9.500.1.2.4.1",
        oids=["1", "2", "3"],
    ),
    detect=startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.9.1.2871"),
)


def discover_cisco_distr_stack_port(section):
    seen = set()
    for port, _status, _nbr in section:
        if port and port not in seen:
            seen.add(port)
            yield Service(item=port)


def check_cisco_distr_stack_port(item, section):
    for port, status, nbr in section:
        if port == item:
            if status == "1":
                yield Result(state=State.OK, summary="Port state: up")
            elif status == "2":
                yield Result(state=State.CRIT, summary="Port state: down")
        if nbr == item:
            if status == "1":
                yield Result(state=State.OK, summary="Neighbor port state: up")
            elif status == "2":
                yield Result(state=State.CRIT, summary="Neighbor port state: down")


check_plugin_cisco_distr_stack_port = CheckPlugin(
    name="cisco_distr_stack_port",
    service_name="Distributed stack port status %s",
    discovery_function=discover_cisco_distr_stack_port,
    check_function=check_cisco_distr_stack_port,
)
