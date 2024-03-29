#!/usr/bin/env python3

from .agent_based_api.v1 import (
    register,
    SNMPTree, 
    startswith,
    Service,
    Result,
    State,
)

def parse_alteon_vrrp_status(string_table):
    values = {}
    for state, router_ip in zip(string_table[0], string_table[1]):
        state = int(state[0])
        router_ip = "{}".format(router_ip[0])
        values[router_ip] = state
    return values


register.snmp_section(
    name="alteon_vrrp_status",
    detect=startswith('.1.3.6.1.2.1.1.1.0', "Alteon Application Switch"),
    parse_function=parse_alteon_vrrp_status,
    fetch=[
        SNMPTree(
            # http://oid-info.com/get/1.3.6.1.4.1.1872.2.5.3.3.3.1.1.2
            # init(1),
            # master(2),
            # backup(3),
            # holdoff(4)
            base='.1.3.6.1.4.1.1872.2.5.3.3.3.1.1',
            oids=[
                '2', # VRRP Status
            ],
        ),
        SNMPTree(
            # http://oidref.com/1.3.6.1.4.1.1872.2.5.3.1.6.3.1
            base='.1.3.6.1.4.1.1872.2.5.3.1.6.3.1',
            oids=[
                '3', # vrrpCurCfgVirtRtrAddr The VRRP virtual router IP address.
            ]
        ),
    ],
)


# {'10.247.84.126': 2, '10.247.80.30': 2, '10.247.84.190': 2, '10.112.99.14': 2, '10.247.81.254': 2, '10.247.84.222': 2, '10.247.84.238': 2}
def discover_alteon_vrrp_status(section):
    if len(section) > 0 and all(elem == list(section.values())[0] for elem in section.values()):
        tresholds = {}
        tresholds["inventory_alteon_vrrp_state"] = (list(section.values())[0], None)
        yield Service(item="VRRP Status", parameters=tresholds)


# VRRP Status
# {'inventory_alteon_vrrp_state': 2}
# {'10.247.84.126': 2, '10.247.80.30': 2, '10.247.84.190': 2, '10.112.99.14': 2, '10.247.81.254': 2, '10.247.84.222': 2, '10.247.84.238': 2}
def check_alteon_vrrp_status(item, params, section):
    defined_state = params["inventory_alteon_vrrp_state"][0]
    state = 0
    states = ["nd", "init", "master", "backup", "holdoff"]
    infotext = "VRRP Status: {}\n".format(states[list(section.values())[0]])
    for router_ip, router_state in section.items():
        infotext = "{}{} -> {}\n".format(infotext, router_ip, states[router_state])

    if not all(elem == list(section.values())[0] for elem in section.values()):
        yield Result(state=State.CRIT, summary=infotext)
    elif list(section.values())[0] != defined_state:
        yield Result(state=State.WARN, summary=infotext)
    else:
        yield Result(state=State.OK, summary=infotext)


register.check_plugin(
    name='alteon_vrrp_status',
    service_name='%s',
    discovery_function=discover_alteon_vrrp_status,
    check_function=check_alteon_vrrp_status,
    check_ruleset_name='alteon_global',
    check_default_parameters={},
)
