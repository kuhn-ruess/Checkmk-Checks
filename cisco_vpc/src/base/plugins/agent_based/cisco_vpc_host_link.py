#!/usr/bin/env python3

from .agent_based_api.v1 import (
    register,
    Result,
    Service,
    SNMPTree,
    matches,
    State,
)


def parse_cisco_vpc_host_link(string_table):
    parsed = {}
    for line in string_table:
        parsed[line[0]] = {
            "host_link_status" : line[1],
            "consistency_status" : line[2],
            "consistency_detail": line[3],
        }
    return parsed


register.snmp_section(
    name="cisco_vpc_host_link",
    fetch=SNMPTree(
            base=".1.3.6.1.4.1.9.9.807.1.4.2.1",
            oids=[
                "3", # CISCO-VPC-MIB::cVpcStatusHostLinkIfIndex
                "4", # CISCO-VPC-MIB::cVpcStatusHostLinkStatus
                "5", # CISCO-VPC-MIB::cVpcStatusHostLinkConsistencyStatus
                "6", # CISCO-VPC-MIB::cVpcStatusHostLinkConsistencyDetail
            ],
        ),
    parse_function=parse_cisco_vpc_host_link,
    detect=matches(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.9.12.3.1.3.\d{4}"),
)


def discover_cisco_vpc_host_link(section_cisco_vpc_host_link, section_if64):
    if section_cisco_vpc_host_link and section_if64:
        yield Service()


def _cisco_vpc_host_link_get_if_name(if_idx, section_if64):
    for interface in section_if64:
        if interface.index == if_idx:
            if interface.descr:
                return interface.descr
            elif interface.alias:
                return interface.alias
            else:
                return if_idx


def check_cisco_vpc_host_link(section_cisco_vpc_host_link, section_if64):
    consistency_status_names = {
        "1" : "success",
        "2" : "failed",
        "3" : "not applicable",
    }
    if all(e["consistency_status"] == "1" for e in section_cisco_vpc_host_link.values()):
        yield Result(state=State.OK, summary="All host link configurations consistent")
    else:
        for if_idx, entry in section_cisco_vpc_host_link.items():
            if entry["consistency_status"] != "1":
                if_name = _cisco_vpc_host_link_get_if_name(if_idx, section_if64)
                yield Result(state=State.CRIT, summary="%s: %s (%s)" % (
                        if_name,
                        consistency_status_names[entry["consistency_status"]],
                        entry["consistency_detail"]
                    ))


register.check_plugin(
    name="cisco_vpc_host_link",
    sections=["cisco_vpc_host_link", "if64"],
    service_name="VPC Host Link",
    discovery_function=discover_cisco_vpc_host_link,
    check_function=check_cisco_vpc_host_link,
)
