#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.agent_based.v2 import (
    all_of,
    contains,
    Metric,
    Result,
    Service,
    SNMPTree,
    State,
    SNMPSection,
    CheckPlugin,
)

def parse_acgateway_users(string_table):
    section = None
    if len(string_table) == 1:
        for tx_trans, rx_trans, users in string_table:
            section = {
                'tx_trans': int(tx_trans),
                'rx_trans': int(rx_trans),
                'users': int(users),
            }
    return section

snmp_section_acgateway_users = SNMPSection(
    name = "acgateway_users",
    parse_function = parse_acgateway_users,
    fetch = [
        SNMPTree(
            base = ".1.3.6.1.4.1.5003.10.8.2",
            oids = [
                "52.41.1.3.0.0", # AC-PM-Control-MIB::acPMSIPActiveSIPTransactionsPerSecondVal.tx.0
                "52.41.1.3.1.0", # AC-PM-Control-MIB::acPMSIPActiveSIPTransactionsPerSecondVal.rx.0
                "54.46.1.2.0",   # AC-PM-Control-MIB::acPMSBCRegisteredUsersVal.0
            ],
        ),
    ],
    detect = all_of(
        contains(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.5003.8.1.1"),
        contains(".1.3.6.1.2.1.1.1.0", "SW Version: 7.20A"),
    ),
)

def discover_acgateway_users(section):
    yield Service()

def check_acgateway_users(section):
    yield Result(state=State.OK,
                 summary="Transactions RX: %d/s" % section['rx_trans'])
    yield Metric('rx_trans', section['rx_trans'])
    yield Result(state=State.OK,
                 summary="Transactions TX: %d/s" % section['tx_trans'])
    yield Metric('tx_trans', section['tx_trans'])
    yield Result(state=State.OK,
                 summary="Registered Users: %d" % section['users'])
    yield Metric('num_user', section['users'])

check_plugin_acgateway_users = CheckPlugin(
    name = "acgateway_users",
    service_name = "SBC Users",
    discovery_function = discover_acgateway_users,
    check_function = check_acgateway_users,
)
