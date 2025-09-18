#!/usr/bin/env python3
"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
#<<<unisphere_powermax_srp:sep(30)>>>
#SYMMETRIX_000297900498_SRP_1{
#   "total_srdf_dse_allocated_cap_gb": 0.0,
#   "srp_efficiency": {
#       "compression_state": "Enabled",
#       "data_reduction_enabled_percent": 100.0,
#       "data_reduction_ratio_to_one": 2.6,
#       "overall_efficiency_ratio_to_one": 8.0,
#       "virtual_provisioning_savings_ratio_to_one": 3.1
#   },
#   "srp_capacity": {
#       "subscribed_total_tb": 263.96,
#       "effective_used_capacity_percent": 23,
#       "usable_used_tb": 34.32,
#       "usable_total_tb": 171.15,
#       "snapshot_modified_tb": 0.0,
#       "subscribed_allocated_tb": 86.1,
#       "snapshot_total_tb": 0.0
#   },
#   "srpId": "SRP_1",
#   "num_of_disk_groups": 1,
#   "rdfa_dse": true,
#   "emulation": "FBA",
#   "diskGroupId": ["1"],
#   "reserved_cap_percent": 10
#}
#SYMMETRIX_000297900497_SRP_1{
#   "total_srdf_dse_allocated_cap_gb": 0.0,
#   "srp_efficiency": {
#       "compression_state": "Enabled",
#       "data_reduction_enabled_percent": 99.0,
#       "data_reduction_ratio_to_one": 2.6,
#       "overall_efficiency_ratio_to_one": 8.0,
#       "virtual_provisioning_savings_ratio_to_one": 3.1
#   },
#   "srp_capacity": {
#       "subscribed_total_tb": 264.11,
#       "effective_used_capacity_percent": 23,
#       "usable_used_tb": 34.27,
#       "usable_total_tb": 171.15,
#       "snapshot_modified_tb": 0.0,
#       "subscribed_allocated_tb": 85.89,
#       "snapshot_total_tb": 0.0
#   },
#   "srpId": "SRP_1",
#   "num_of_disk_groups": 1,
#   "rdfa_dse": true,
#   "emulation": "FBA",
#   "diskGroupId": ["1"],
#   "reserved_cap_percent": 10
#}


from cmk.agent_based.v2 import (
    Service,
    Result,
    State,
    CheckPlugin,
    AgentSection,
    check_levels,
)

from .utils import parse_section

agent_section_unispere_powermax_srp = AgentSection(
    name="unisphere_powermax_srp",
    parse_function=parse_section,
)

def discover_srp_effective_used(section):
    """
    Discover effective used capacity for SRP on PowerMax systems.
    """
    for item, data in section.items():
        if data.get('srp_capacity', {}).get('effective_used_capacity_percent'):
            yield Service(item=item)

def check_srp_effective_used(item, params, section):
    """
    Check effective used capacity for SRP on PowerMax systems.
    """
    srp_info = section[item]
    used = srp_info.get('srp_capacity', {}).get('effective_used_capacity_percent')

    if not used:
        yield Result(state=State.UNKNOWN, summary="got no data from agent")
        return

    yield from check_levels(
        used,
        metric_name='used',
        levels_upper=params['levels'],
        boundaries=(0, 100),
        render_func=lambda v: f"{v}% used",
    )

def discover_srp_physical_used(section):
    """
    Discover physical used capacity for SRP on PowerMax systems.
    """
    for item, data in section.items():
        if data.get('srp_capacity', {}).get('usable_used_tb'):
            yield Service(item=item)

def check_srp_physical_used(item, params, section):
    """
    Check physical used capacity for SRP on PowerMax systems.
    """
    srp_info = section[item].get('srp_capacity')
    if not srp_info:
        return


    used_tb = srp_info.get('usable_used_tb')
    total_tb = srp_info.get('usable_total_tb')

    used = round((used_tb / total_tb)*100, 2)

    yield from check_levels(
        used,
        metric_name='used',
        levels_upper=params['levels'],
        boundaries=(0, 100),
        render_func=lambda v: f"{v}% used",
    )

def discover_srp_data_reduction_ratio(section):
    """
    Discover data reduction ratio for SRP on PowerMax systems.
    """
    for item, data in section.items():
        if data.get('srp_efficiency', {}).get('data_reduction_ratio_to_one'):
            yield Service(item=item)

def check_srp_data_reduction_ratio(item, params, section):
    """
    Check data reduction ratio for SRP on PowerMax systems.
    """
    srp_info = section[item].get('srp_efficiency')
    if not srp_info:
        return
    ratio = srp_info.get('data_reduction_ratio_to_one')

    yield from check_levels(
        ratio,
        metric_name='ratio',
        levels_lower=params['levels'],
        render_func=lambda v: f"{v}:1",
    )

check_plugin_unisphere_powermax_srp_effective_used = CheckPlugin(
    name = "unisphere_powermax_srp_effective_used",
    sections = ['unisphere_powermax_srp'],
    service_name = 'Effective SRP Capacity %s',
    discovery_function = discover_srp_effective_used,
    check_function = check_srp_effective_used,
    check_ruleset_name="unisphere_powermax_srp_effective_used",
    check_default_parameters = {"levels": ('fixed', (80.0, 90.0))}
)

check_plugin_unisphere_powermax_srp_physical_used = CheckPlugin(
    name = "unisphere_powermax_srp_physical_used",
    sections = ['unisphere_powermax_srp'],
    service_name = 'Physical SRP Capacity %s',
    discovery_function = discover_srp_physical_used,
    check_function = check_srp_physical_used,
    check_ruleset_name = 'unisphere_powermax_srp_physical_used',
    check_default_parameters = {"levels": ('fixed', (80.0, 90.0))}
)

check_plugin_unisphere_powermax_srp_data_reduction_ratio = CheckPlugin(
    name = "unisphere_powermax_srp_data_reduction_ratio",
    sections = ['unisphere_powermax_srp'],
    service_name = 'SRP Data Reduction Ratio %s',
    discovery_function = discover_srp_data_reduction_ratio,
    check_function = check_srp_data_reduction_ratio,
    check_ruleset_name = 'unisphere_powermax_srp_data_reduction_ratio',
    check_default_parameters = {"levels": ('fixed', (3.0, 2.0))}
)
