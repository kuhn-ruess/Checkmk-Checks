#!/usr/bin/env python3

from .agent_based_api.v1 import (
    register,
    Result,
    Service,
    SNMPTree,
    matches,
    State,
)


register.snmp_section(
    name="cisco_vpc_status",
    fetch=SNMPTree(
            base=".1.3.6.1.4.1.9.9.807.1.1.2.1",
            oids=[
                "2", # cVpcPeerKeepAliveStatus
            ],
        ),
    detect=matches(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.9.12.3.1.3.\d{4}"),
)


def discover_cisco_vpc_status(section):
   if section:
    yield Service()


def check_cisco_vpc_status(section):
    status_names = {
        "1" : "disabled",
        "2" : "alive",
        "3" : "peerUnreachable",
        "4" : "aliveButDomainIdDismatch",
        "5" : "suspendedAsISSU",
        "6" : "suspendedAsDestIPUnreachable",
        "7" : "suspendedAsVRFUnusable",
        "8" : "misconfigured"
    }
    status_name = status_names.get(section[0][0], "Unknown status: " + section[0][0])
    if section[0][0] == "2":
        yield Result(state=State.OK, summary=status_name)
    else:
        yield Result(state=State.CRIT, summary=status_name)


register.check_plugin(
    name="cisco_vpc_status",
    sections=["cisco_vpc_status"],
    service_name="VPC Keepalive Status",
    discovery_function=discover_cisco_vpc_status,
    check_function=check_cisco_vpc_status,
)
