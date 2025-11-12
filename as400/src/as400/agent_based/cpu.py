#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from .lib import DETECT_AS400, parse_as400

from cmk.plugins.lib.cpu import Section, Load
from cmk.plugins.lib.cpu_load import CPULoadParams, check_cpu_load

from cmk.agent_based.v2 import (
    SimpleSNMPSection,
    CheckPlugin,
    Service,
    SNMPTree,
    State,
    Metric,
    Result,
    get_value_store,
)


snmp_section_as400_cpu = SimpleSNMPSection(
    name="as400_cpu",
    detect=DETECT_AS400,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.2.6.4.5.1",
        oids=["0"],
    ),
    parse_function = parse_as400,
)


def discover_as400_cpu(section):
    """ Discover Function """
    yield Service()

def check_as400_cpu(params, section):
    """ Check Function """
    cpu = section / 100.0

    yield from check_cpu_load(
        params=CPULoadParams(
            {
                "levels1": None,
                "levels5": None,
                "levels15": params["cpu_levels"][1],
            },
        ),
        section=Section(
            load=Load(0.0, 0.0, cpu),
            num_cpus=1,
        ),
    )


check_plugin_as400_cpu = CheckPlugin(
    name="as400_cpu",
    service_name="CPU load",
    discovery_function=discover_as400_cpu,
    check_function=check_as400_cpu,
    check_default_parameters={"cpu_levels": ("fixed", (80, 90))},
    check_ruleset_name="as400_cpu",
)
