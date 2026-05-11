#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.agent_based.v2 import (
    CheckPlugin,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    check_levels,
    startswith,
)


VERTIV_DETECT = startswith(".1.3.6.1.2.1.1.1.0", "Avocent ACS")


def parse_vertiv_acs8000_cpu_temperature(string_table):
    if not string_table or not string_table[0]:
        return None
    try:
        return int(string_table[0][0])
    except (ValueError, IndexError):
        return None


def discover_vertiv_acs8000_cpu_temperature(section):
    yield Service()


def check_vertiv_acs8000_cpu_temperature(params, section):
    yield from check_levels(
        value=float(section),
        levels_upper=params.get("levels"),
        metric_name="temp",
        label="CPU temperature",
        render_func=lambda v: f"{v:.0f} °C",
    )


snmp_section_vertiv_acs8000_cpu_temperature = SimpleSNMPSection(
    name="vertiv_acs8000_cpu_temperature",
    parse_function=parse_vertiv_acs8000_cpu_temperature,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.10418.26.2.7",
        oids=["1.0"],  # acsSensorsInternalCurrentCPUTemperature
    ),
    detect=VERTIV_DETECT,
)


check_plugin_vertiv_acs8000_cpu_temperature = CheckPlugin(
    name="vertiv_acs8000_cpu_temperature",
    service_name="Vertiv ACS CPU temperature",
    discovery_function=discover_vertiv_acs8000_cpu_temperature,
    check_function=check_vertiv_acs8000_cpu_temperature,
    check_ruleset_name="vertiv_acs8000_cpu_temperature",
    check_default_parameters={"levels": ("fixed", (70.0, 85.0))},
)
