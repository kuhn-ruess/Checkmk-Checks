#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.agent_based.v2 import (
    contains,
    Result,
    Service,
    SNMPTree,
    State,
    SNMPSection,
    CheckPlugin,
)

def _item_acgateway_ipgroup(line):
    return "%s %s" % (line[0], line[4])

def parse_acgateway_ipgroup(string_table):
    rowStatus = {
        '1': 'active',
        '2': 'notInService',
        '3': 'notReady',
    }
    ipGroupType = {
        '0': 'server',
        '1': 'user',
        '2': 'gateway',
    }
    section = {}
    for line in string_table[0]:
        item = _item_acgateway_ipgroup(line)
        section[item] = {
            'ipgroupstatus': rowStatus.get(line[1], 'unknown'),
            'ipgrouptype': ipGroupType.get(line[2], 'unknown'),
            'description': line[3],
            'name': line[4]
        }
    return section

snmp_section_acgateway_ipgroup = SNMPSection(
    name = "acgateway_ipgroup",
    parse_function = parse_acgateway_ipgroup,
    fetch = [
        SNMPTree(
            base = ".1.3.6.1.4.1.5003.9.10.3.1.1.23.21.1",
            oids = [
                "1",  # 0  AcGateway::ipGroupIndex
                "2",  # 1  AcGateway::ipGroupRowStatus
                "5",  # 2  AcGateway::ipGroupType
                "6",  # 3  AcGateway::ipGroupDescription
                "31", # 4  AcGateway::ipGroupName
            ],
        ),
    ],
    detect = contains(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.5003.8.1.1"),
)

def discover_acgateway_ipgroup(section):
    for item, data in section.items():
        yield Service(item=item, parameters={'ipgroupstatus': data.get('ipgroupstatus')})

def check_acgateway_ipgroup(item, params, section):
    if item in section:
        data = section[item]
        yield Result(state=State.OK,
                     summary='ip group type: %s' % data['ipgrouptype'])
        if data['description']:
            yield Result(state=State.OK,
                         summary=data['description'])
        for param, value in params.items():
            if value != data.get(param):
                yield Result(state=State.CRIT,
                             summary='%s is %s' % (param, data.get(param)))

check_plugin_acgatgeway_ipgroup = CheckPlugin(
    name = "acgateway_ipgroup",
    service_name = "IP Group %s",
    discovery_function = discover_acgateway_ipgroup,
    check_function = check_acgateway_ipgroup,
    check_default_parameters = {},
)
