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
    name="cisco_vpc_role",
    fetch=SNMPTree(
            base=".1.3.6.1.4.1.9.9.807.1.2.1.1",
            oids=[
                "2", # CISCO-VPC-MIB::cVpcRoleStatus
                "3", # CISCO-VPC-MIB::cVpcDualActiveDetectionStatus
            ],
        ),
    detect=startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.9.12.3.1.3.1955"),
)


def discover_cisco_vpc_role(section):
    yield Service(parameters={"switch_role" : section[0][0]})


def check_cisco_vpc_role(params, section):
    role_names = {
        "1" : "primary, and operational secondary",   # primarySecondary(1),
        "2" : "primary, and operational primary",     # primary(2),
        "3" : "secondary, and operational primary",   # secondaryPrimary(3),
        "4" : "secondary, and operational secondary", # secondary(4),
        "5" : "no peer device",                       # noneEstablished(5),
    }
    role_name = role_names[section[0][0]]
    if params.get("switch_role") and section[0][0] != params["switch_role"]:
        yield Result(state=State.WARN, summary=role_name + " (expected " + role_names[params["switch_role"]] + ")")
    else:
        yield Result(state=State.OK, summary=role_name)
    if section[0][1] == "2":
        yield Result(state=State.OK, summary="no dual active detected")
    else:
        yield Result(state=State.CRIT, summary="dual active detected")


register.check_plugin(
    name="cisco_vpc_role",
    sections=["cisco_vpc_role"],
    service_name="VPC Role",
    discovery_function=discover_cisco_vpc_role,
    check_function=check_cisco_vpc_role,
    check_default_parameters={},
    check_ruleset_name="cisco_vpc_role",
)
