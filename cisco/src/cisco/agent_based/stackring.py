#!/usr/bin/env python3

"""
Cisco StackWise ring redundancy check.

Kuhn & Rueß GmbH
https://kuhn-ruess.de
"""

# .1.3.6.1.4.1.9.9.500.1.2.1.1.1  --> cswSwitchNumCurrent (list of members)
# .1.3.6.1.4.1.9.9.500.1.1.3.0    --> cswRingRedundant (scalar: 1 = redundant, 2 = not)

from cmk.agent_based.v2 import (
    CheckPlugin,
    OIDEnd,
    Result,
    Service,
    SNMPSection,
    SNMPTree,
    State,
    all_of,
    contains,
    exists,
)


def parse_cisco_stackring(string_table):
    members, ring = string_table
    return {
        "members": [row[0] for row in members],
        "ring": ring[0][0] if ring and ring[0] else None,
    }


snmp_section_cisco_stackring = SNMPSection(
    name="cisco_stackring",
    parse_function=parse_cisco_stackring,
    detect=all_of(
        contains(".1.3.6.1.2.1.1.1.0", "cisco"),
        exists(".1.3.6.1.4.1.9.9.500.1.2.1.1.1"),
        exists(".1.3.6.1.4.1.9.9.500.1.1.3"),
    ),
    fetch=[
        SNMPTree(
            base=".1.3.6.1.4.1.9.9.500.1.2.1.1.1",
            oids=[OIDEnd()],
        ),
        SNMPTree(
            base=".1.3.6.1.4.1.9.9.500.1.1",
            oids=["3"],
        ),
    ],
)


def discover_cisco_stackring(section):
    if len(section["members"]) >= 2:
        yield Service()


def check_cisco_stackring(section):
    if section["ring"] is None:
        yield Result(state=State.UNKNOWN, summary="Stackring not found")
        return
    if section["ring"] == "1":
        yield Result(state=State.OK, summary="Stackring is redundant")
    else:
        yield Result(state=State.CRIT, summary="Stackring is NOT redundant")


check_plugin_cisco_stackring = CheckPlugin(
    name="cisco_stackring",
    service_name="Stackring",
    discovery_function=discover_cisco_stackring,
    check_function=check_cisco_stackring,
)
