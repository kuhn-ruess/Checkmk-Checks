#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from json import loads
from re import search

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    Result,
    Service,
    State,
    get_value_store,
)
from cmk.plugins.lib.temperature import check_temperature, TempParamDict


def parse_lnx_sensors(string_table):
    """
    Parse lnx_sensors
    """
    data = ""
    for entry in string_table:
        data += "".join(entry)

    json = loads(data)
    sensors = {"cpu": {}}
    for bus, data in json.items():
        for name, levels in data.items():

            if "Core" in name:
                sensors["cpu"][name] = levels
    return sensors


agent_section_lnx_sensors = AgentSection(
    name = "lnx_sensors",
    parse_function = parse_lnx_sensors,
)


def discover_lnx_cpus(params, section):
    """
    Discover CPUs
    """
    searches = []
    if "cpu_filters" in params.keys():
        searches = params["cpu_filters"]

    for name, _levels in section["cpu"].items():
        for string in searches:
            if search(string["name"], name):
                yield Service(item=name)


def check_lnx_cpus(item, params, section):
    """
    Check single CPU
    """
    for _bus, data in section.items():
        if item in data.keys():
            value, warn, crit, _alarm = data[item].values()
            yield from check_temperature(
                reading = value,
                params = params,
                dev_levels = (warn, crit),
                unique_name = item,
                value_store = get_value_store(),
            )


check_plugin_lnx_cpus = CheckPlugin(
    name = "lnx_cpu",
    sections = ["lnx_sensors"],
    service_name = "Temperature CPU %s",
    discovery_function = discover_lnx_cpus,
    discovery_ruleset_name = "discover_lnx_sensors",
    discovery_default_parameters = {},
    check_function = check_lnx_cpus,
    check_ruleset_name="temperature",
    check_default_parameters=TempParamDict(
        levels=(70.0, 80.0),
        device_levels_handling="devdefault",
    ),
)
