#!/usr/bin/env python3
"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.agent_based.v2 import (
    Result,
    Service,
    State,
    CheckPlugin,
)

# Example Output
"""
<<<dellpmax_systeminfo>>>
sersion|V9.2.2.2

"""


def discover_dellpmax_info(section):
    yield Service()


def check_dellpmax_info(section):
    yield Result(state=State.OK, summary="PowerMax Unisphere version: {}".format(section[0][1]))


check_plugin_dell_pmax_systeminfo = CheckPlugin(
    name="dellpmax_systeminfo",
    service_name="Version Info",
    discovery_function=discover_dellpmax_info,
    check_function=check_dellpmax_info,
)
