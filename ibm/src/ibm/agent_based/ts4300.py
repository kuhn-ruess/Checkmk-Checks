#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.agent_based.v2 import (
    Service,
    Result,
    State,
    SNMPSection,
    SNMPTree,
    matches,
    CheckPlugin,
)

def parse_ibm_ts4300(string_table):
    return string_table[0]

snmp_section_ibm_ts4300 = SNMPSection(
    name = "ibm_ts4300",
    parse_function = parse_ibm_ts4300,
    fetch = [
        SNMPTree(
            base = ".1.3.6.1.4.1.14851.3.1.3",
            oids = [
                '1.0',
                '2.0',
                '3.0',
                '4.0',
                '5.0',
            ],
        ),
    ],
    detect = matches(".1.3.6.1.4.1.14851.3.1.3.3.0", "IBM"),
)

def discover_ibm_ts4300(section):
    yield Service()

def check_ibm_ts4300(section):
    # [['3573-TL', '3555L3A7800LH9', 'IBM', '1.2.1.0-A00', 'IBM TS4300 Tape Library']
    model, serial, vendor, version, description = section[0]
    yield Result(state=State.OK,  summary=f"Model: {model}, Serial: {serial}, Version: {version}, Description: {description}")

check_plugin_ibm_ts4300 = CheckPlugin(
    name = "ibm_ts4300",
    service_name = "Library Info",
    discovery_function = discover_ibm_ts4300,
    check_function = check_ibm_ts4300,
)
