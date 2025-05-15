#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    get_value_store,
    Result,
    Service,
    State,
)
from cmk.plugins.lib.temperature import check_temperature

from .utils.pure import (
    parse_pure_hardware,
)


agent_section_pure_hardware_temp = AgentSection(
    name="pure_hardware_temp",
    parse_function=parse_pure_hardware,
)


def discover_pure_hardware_temp(section):
    for item, data in section.items():
        if "temperature" in data:
            yield Service(item=item)

def check_pure_hardware_temp(item, params, section):
    value = int(section[item]["temperature"])

    yield from check_temperature(
        value,
        params,
        unique_name="pure_hardware_temp.%s" % item,
        value_store=get_value_store(),
    )


check_plugin_pure_hardware_temp = CheckPlugin(
    name="pure_hardware_temperature",
    sections=["pure_hardware"],
    service_name="Temperature %s",
    discovery_function=discover_pure_hardware_temp,
    check_function=check_pure_hardware_temp,
    check_default_parameters={},
    check_ruleset_name="temperature",
)
