#!/usr/bin/python3
"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    check_levels,
    Service,
)

def parse(string_table):
    """
    Parse function
    """
    print("Parsing digital signage section")
    return {x[0]:int(x[1]) for x in string_table} 


def discovery(section):
    """ Discovery """
    yield Service()

def check(params, section):
    """ Check """

    for name, value in section.items():
        metric_name = name.replace(' ', '_')
        yield from check_levels (
            value,
            levels_upper=params[metric_name],
            metric_name=metric_name.lower(),
            label=name,
            render_func=lambda v: "%.1f" % v
        )

agent_section_hci_cluster_resources = AgentSection(
    name="digital_signage",
    parse_function=parse
)

check_plugin_hci_cluster_resources = CheckPlugin(
    name="digital_signage",
    service_name="Digital Signage",
    discovery_function=discovery,
    check_function=check,
    check_default_parameters = {
        'GPU_Load_3D' : ('fixed', (90, 95)),
        'GPU_Load_Copy' : ('fixed', (90, 95)),
        'GPU_Load_VideoProcessing' : ('fixed', (90, 95)),
        'GPU_Load_VideoDecode' : ('fixed', (90, 95)),
    },
    check_ruleset_name="digital_signage",
)
