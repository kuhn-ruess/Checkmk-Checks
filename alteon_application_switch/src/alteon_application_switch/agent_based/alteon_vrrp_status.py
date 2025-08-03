#!/usr/bin/env python3

from cmk.agent_based.v2 import (
    SNMPTree, 
    startswith,
    Service,
    Result,
    State,
    CheckPlugin,
    SNMPSection,
)

def parse_alteon_vrrp_status(string_table):
    values = {}
    for state, router_ip in zip(string_table[0], string_table[1]):
        state = int(state[0])
        router_ip = "{}".format(router_ip[0])
        values[router_ip] = state
    return values


snmp_section_alteon_vrrp_status = SNMPSection(
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
        yield Service(item="VRRP Status")


# VRRP Status
# {'inventory_alteon_vrrp_state': 'master'}
# {'10.247.84.126': 2, '10.247.80.30': 2, '10.247.84.190': 2, '10.112.99.14': 2, '10.247.81.254': 2, '10.247.84.222': 2, '10.247.84.238': 2}
def check_alteon_vrrp_status(item, params, section):
    # Mapping von numerischen Werten zu String-Namen
    states = ["nd", "init", "master", "backup", "holdoff"]
    state_to_name = {0: "nd", 1: "init", 2: "master", 3: "backup", 4: "holdoff"}
    name_to_state = {"nd": 0, "init": 1, "master": 2, "backup": 3, "holdoff": 4}
    
    # Parameter aus Ruleset holen (String-Name)
    expected_state_name = params["inventory_alteon_vrrp_state"]
    expected_state_num = name_to_state.get(expected_state_name, 2)  # Default: master
    
    current_state_num = list(section.values())[0]
    current_state_name = state_to_name.get(current_state_num, "unknown")
    
    infotext = "VRRP Status: {}".format(current_state_name)
    for router_ip, router_state in section.items():
        router_state_name = state_to_name.get(router_state, "unknown")
        infotext = "{}, {} -> {}".format(infotext, router_ip, router_state_name)

    if not all(elem == list(section.values())[0] for elem in section.values()):
        yield Result(state=State.CRIT, summary=infotext + " (inconsistent states)")
    elif current_state_num != expected_state_num:
        yield Result(state=State.WARN, summary=infotext + " (expected: {})".format(expected_state_name))
    else:
        yield Result(state=State.OK, summary=infotext)


check_plugin_alteon_vrrp_status = CheckPlugin(     
    name='alteon_vrrp_status',
    service_name='%s',
    discovery_function=discover_alteon_vrrp_status,
    check_function=check_alteon_vrrp_status,
    check_ruleset_name='alteon_global',
    check_default_parameters={"inventory_alteon_vrrp_state": "master"},
)
