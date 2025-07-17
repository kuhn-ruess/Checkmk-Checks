#!/usr/bin/env python3
"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
#<<<unisphere_powermax_array_performance:sep(30)>>>
#SYMMETRIX_000297900498-RZ1{"Average":
# {"FEReqs": 17565.527, "FEWriteMissReqs": 333.76, "SystemMaxWPLimit": 11847405.0,
#  "WriteResponseTime": 1.3820363, "FEHitReqs": 16194.116, "PercentCacheWP": 1.3488692,
#  "DeviceWPEvents": 0.0, "ReadResponseTime": 0.42482662, "FEWriteHitReqs": 5894.95,
#  "BEReqs": 12193.817, "HostIOs": 12869.486, "SystemWPEvents": 0.0,
#  "timestamp": 1615458300000, "HostMBs": 684.82007, "FEReadMissReqs": 1037.6501,
#  "BEIOs": 22252.123, "FEReadHitReqs": 10299.166, "FEWriteReqs": 6228.71,
#  "BEReadReqs": 5830.823, "BEWriteReqs": 6362.993, "WPCount": 159806.0, "FEReadReqs": 11336.817},
#  "Maximum": {"FEReqs": 36209.227, "FEWriteMissReqs": 1147.6667, "SystemMaxWPLimit": 11847405.0,
#  "WriteResponseTime": 2.5043576, "FEHitReqs": 33233.87, "PercentCacheWP": 1.3886416,
#  "DeviceWPEvents": 0.0, "ReadResponseTime": 0.61653674, "FEWriteHitReqs": 11954.507,
#  "BEReqs": 20315.166, "HostIOs": 30688.465, "SystemWPEvents": 0.0, "timestamp": 1615458300000,
#  "HostMBs": 1389.8188, "FEReadMissReqs": 3889.6648, "BEIOs": 31872.55, "FEReadHitReqs": 27527.486,
#  "FEWriteReqs": 12991.903, "BEReadReqs": 11549.166, "BEWriteReqs": 10000.0, "WPCount": 164518.0,
#  "FEReadReqs": 28857.14}}


import re

from cmk.agent_based.v2 import (
    Service,
    Result,
    State,
    Metric,
    CheckPlugin,
    AgentSection,
    check_levels,
) 

from .utils import parse_section

agent_section_unispere_array_performance = AgentSection(
    name="unisphere_powermax_array_performance",
    parse_function=parse_section,
)


def camel_to_snake(name):
    """
    Convert CamelCase to snake_case.
    """
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

def discover_wp_cache(section):
    """
    Discover WP Cache usage for PowerMax systems.
    """
    for item, data  in section.items():
        if data.get('Average', {}).get('PercentCacheWP')\
                and data.get('Maximum', {}).get('PercentCacheWP'):
            yield Service(item=item)

def check_wp_cache(item, params, section):
    """
    Check WP Cache usage for PowerMax systems.
    """
    perf_data = section[item]

    average_wp_cache = perf_data.get('Average', {}).get('PercentCacheWP')
    maximum_wp_cache = perf_data.get('Maximum', {}).get('PercentCacheWP')

    if not average_wp_cache or not maximum_wp_cache:
        yield Result(state=State.UNKNOWN, summary="got no data from agent")
        return

    yield from check_levels(
            average_wp_cache,
            levels_upper=params['average_levels'],
            metric_name='average_wp_cache',
            label='Cache',
            render_func=lambda v: f"Average WP Cache Usage: {v}%"
    )
    yield from check_levels(
            maximum_wp_cache,
            levels_upper=params['maximum_levels'],
            metric_name='maximum_wp_cache',
            label='Cache',
            render_func=lambda v: f"Maximum WP Cache Usage: {v}%"
    )


def discover_perf_info(section):
    """
    Discover performance info for PowerMax systems.
    """
    for item, j in section.items():
        if j.get('Average', None) is not None and j.get('Maximum', None) is not None:
            yield Service(item=item)

def check_perf_info(item, section):
    """
    Check performance info for PowerMax systems.
    """
    perf_data = section[item]

    state = State.OK
    info_text = "Performance info check for gathering performance graphs"

    for x in perf_data.get('Average').keys():
        yield Metric(name=f"average_{camel_to_snake(x)}_5min",
                     value=perf_data.get('Average')[x])

    yield Result(state=state, summary=info_text)


check_plugin_unisphere_powermax_arrayperformance_wp_cache = CheckPlugin(
    name = "unisphere_powermax_array_performance_wp_cache",
    sections = ['unisphere_powermax_array_performance'],
    service_name = 'Array WP Cache %s',
    discovery_function = discover_wp_cache,
    check_function = check_wp_cache,
    check_ruleset_name="unisphere_powermax_powermax_array_performance_wp_cache",
    check_default_parameters =  {"average_levels": ('fixed', (70, 90)),
                                 "maximum_levels": ('fixed', (70, 90))}
)

check_plugin_unisphere_powermax_arrayperformance_perf_info = CheckPlugin(
    name = "unisphere_powermax_array_performance_perf_info",
    sections = ['unisphere_powermax_array_performance'],
    service_name = 'Array Performance Info %s',
    discovery_function = discover_perf_info,
    check_function = check_perf_info,
)
