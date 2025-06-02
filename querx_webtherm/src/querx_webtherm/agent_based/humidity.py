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
)
from cmk.plugins.lib.humidity import check_humidity


def parse_querx_webtherm_humidity(string_table):
    return float(string_table[0][0])

def discover_querx_webtherm_humidity(section):
    yield Service(item="Humidity Sensor")

def check_querx_webtherm_humidity(item, params, section):
    yield from check_humidity(section, params)


snmp_section_querx_webtherm_humidity = SimpleSNMPSection(
    name = "querx_webtherm_humidity",
    detect = contains(".1.3.6.1.2.1.1.1.0", "Querx"),
    fetch = SNMPTree(
        base = ".1.3.6.1.4.1.3444.1.14.1.2.1.5",
        oids = ["2"],
    ),
    parse_function = parse_querx_webtherm_humidity,
)


check_plugin_querx_webtherm_humidity = CheckPlugin(
    name = "querx_webtherm_humidity",
    service_name = "%s",
    discovery_function = discover_querx_webtherm_humidity,
    check_function = check_querx_webtherm_humidity,
    check_ruleset_name = "humidity",
    check_default_parameters = {},
)
