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


def parse_cisco_catalyst_9k_redundancy(string_table: StringTable) -> StringTable:
    return string_table


snmp_section_cisco_catalyst_9k_redundancy = SimpleSNMPSection(
    name="cisco_catalyst_9k_redundancy",
    parse_function=parse_cisco_catalyst_9k_redundancy,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.9.9.500.1.1",
        oids=[
            "3",  # CISCO-STACKWISE-MIB::cswRingRedundant
        ],        # https://datatracker.ietf.org/doc/html/rfc2579
    ),            # TruthValue: 1  INTEGER { true(1), false(2) }
    detect=startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.9.1.2871"),
)


def discover_cisco_catalyst_9k_redundancy(section: StringTable):
    yield Service()


def check_cisco_catalyst_9k_redundancy(section: StringTable):
    if section[0][0] == "1":
        yield Result(state=State.OK, summary="Stackports form a redundant ring")
    elif section[0][0] == "2":
        yield Result(state=State.CRIT, summary="Stackports do not form a redundant ring")


check_plugin_cisco_catalyst_9k_redundancy = CheckPlugin(
    name="cisco_catalyst_9k_redundancy",
    sections=["cisco_catalyst_9k_redundancy"],
    service_name="Stack Ring Redundancy",
    discovery_function=discover_cisco_catalyst_9k_redundancy,
    check_function=check_cisco_catalyst_9k_redundancy,
)
