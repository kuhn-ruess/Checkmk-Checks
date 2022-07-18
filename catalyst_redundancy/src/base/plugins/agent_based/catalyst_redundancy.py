#!/usr/bin/env python3

from .agent_based_api.v1 import (
    register,
    Result,
    Service,
    SNMPTree,
    startswith,
    State,
)


register.snmp_section(
    name="catalyst_redundancy",
    fetch=SNMPTree(
            base=".1.3.6.1.4.1.9.9.500.1.1",
            oids=[
                "3",  # CISCO-STACKWISE-MIB::cswRingRedundant
            ],        # https://datatracker.ietf.org/doc/html/rfc2579
        ),            # TruthValue: 1  INTEGER { true(1), false(2) }
    detect=startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.9.1.2871"),
)

def discover_catalyst_redundancy(section):
    yield Service()


def check_catalyst_redundancy(section):
    if section[0][0] == "1":
        yield Result(state=State.OK, summary="Stackports form a redundant ring")
    elif section[0][0] == "2":
        yield Result(state=State.CRIT, summary="Stackports do not form a redundant ring")


register.check_plugin(
    name="catalyst_redundancy",
    sections=["catalyst_redundancy"],
    service_name="Stack Ring Redundancy",
    discovery_function=discover_catalyst_redundancy,
    check_function=check_catalyst_redundancy,
)
