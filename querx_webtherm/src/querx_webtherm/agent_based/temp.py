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
from cmk.plugins.lib.temperature import check_temperature


def discover_querx_webtherm_temp(string_table):
    yield Service()

def check_querx_webtherm_temp(params, string_table):
    yield from check_temperature(float(info[0][0]) / 10, params, "temperature")


snmp_section_querx_webtherm_temp = SimpleSNMPSection(
    name = "querx_webtherm_temp",
    fetch = SNMPTree(
        base = ".1.3.6.1.4.1.3444.1.14.1.2.1.5",
        oids = ["1"],
    ),
    detect = contains(".1.3.6.1.2.1.1.1.0", "Querx"),
)


check_plugin_querx_webtherm_temp = CheckPlugin(
    name = "querx_webtherm_temp",
    service_name = "Temperature Sensor",
    discovery_function = discover_querx_webtherm_temp,
    check_function = check_querx_webtherm_temp,
    check_ruleset_name = "temperature",
    check_default_parameters = {},
)
