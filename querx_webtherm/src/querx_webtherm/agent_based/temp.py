#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.agent_based.v2 import (
    Service,
    SimpleSNMPSection,
    SNMPTree,
    contains,
    CheckPlugin,
    get_value_store,
)
from cmk.plugins.lib.temperature import check_temperature


def parse_querx_webtherm_temp(string_table):
    return float(string_table[0][0]) / 10

def discover_querx_webtherm_temp(section):
    yield Service(item="Temperature Sensor")

def check_querx_webtherm_temp(item, params, section):
    yield from check_temperature(section, params, unique_name="temperature", value_store=get_value_store())


snmp_section_querx_webtherm_temp = SimpleSNMPSection(
    name = "querx_webtherm_temp",
    detect = contains(".1.3.6.1.2.1.1.1.0", "Querx"),
    fetch = SNMPTree(
        base = ".1.3.6.1.4.1.3444.1.14.1.2.1.5",
        oids = ["1"],
    ),
    parse_function = parse_querx_webtherm_temp,
)


check_plugin_querx_webtherm_temp = CheckPlugin(
    name = "querx_webtherm_temp",
    service_name = "%s",
    discovery_function = discover_querx_webtherm_temp,
    check_function = check_querx_webtherm_temp,
    check_ruleset_name = "temperature",
    check_default_parameters = {},
)
