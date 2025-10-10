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

# NEW/ALTERNATIVE FORMAT
#SYMMETRIX_000220009898_SRP_1{
#  "srpId": "SRP_1",
#  "num_of_disk_groups": 1,
#  "emulation": "FBA",
#  "reserved_cap_percent": 10,
#  "total_srdf_dse_allocated_cap_gb": 0.0,
#  "rdfa_dse": true,
#  "reliability_state": "Optimal",
#  "diskGroupId": ["1"],
#  "fba_srp_capacity": {
#    "provisioned": {
#      "provisioned_tb": 41.22,
#      "effective_capacity_tb": 294.49,
#      "provisioned_percent": 14.0
#    },
#    "effective": {
#      "used_tb": 1.47,
#      "total_tb": 294.49,
#      "free_tb": 293.02,
#      "effective_used_percent": 1.0,
#      "target_tb": 294.49,
#      "physical_capacity": {
#        "used_tb": 0.49,
#        "total_tb": 108.95,
#        "free_tb": 108.46,
#        "target_tb": 108.95
#      },
#      "effective_capacity_resources": {
#        "used_tb": 1.47,
#        "total_tb": 840.62,
#        "free_tb": 839.15
#      },
#      "effective_capacity_usage": {
#        "snapshot_used_tb": 0.0,
#        "user_used_tb": 1.47,
#        "free_tb": 293.02
#      }
#    },
#    "snapshot": {
#      "effective_used_percent": 0.0,
#      "physical_used_percent": 0.0,
#      "resource_used_tb": 0.0,
#      "modified_capacity_tb": 0.0,
#      "total_capacity_tb": 0.0
#    },
#    "data_reduction": {
#      "data_reduction_ratio_to_one": 6.0,
#      "reducing_data_percent": 79.0,
#      "savings_tb": 0.98,
#      "effective_used": {
#        "enabled_and_reducing_tb": 1.17,
#        "enabled_and_unreducible_tb": 0.3,
#        "enabled_and_unevaluated_tb": 0.0,
#        "disabled_and_unreduced_tb": 0.0
#      },
#      "physical_used": {
#        "enabled_and_reducing_tb": 0.19,
#        "enabled_and_unreducible_tb": 0.3,
#        "enabled_and_unevaluated_tb": 0.0,
#        "disabled_and_unreduced_tb": 0.0
#      }
#    }
#  },
#  "srp_efficiency": {
#    "compression_state": "Enabled",
#    "overall_efficiency_ratio_to_one": 83.8,
#    "data_reduction_ratio_to_one": 6.0,
#    "data_reduction_enabled_percent": 100.0,
#    "unreducible_data_tb": 0.3,
#    "reducible_data_tb": 1.17,
#    "deduplication_and_compression_savings_tb": 0.65,
#    "pattern_detection_savings_tb": 0.33,
#    "drr_on_reducible_only_to_one": 6.0
#  },
#  "service_levels": [
#    "Bronze",
#    "Diamond",
#    "Gold",
#    "Optimized",
#    "Platinum",
#    "Silver"
#  ]
#}


from cmk.agent_based.v2 import (
    Service,
    Result,
    State,
    CheckPlugin,
    AgentSection,
    check_levels,
    Metric,
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
        elif data.get('fba_srp_capacity', {}).get('effective', {}).get('effective_used_percent'):
            yield Service(item=item)

def check_srp_effective_used(item, params, section):
    """
    Check effective used capacity for SRP on PowerMax systems.
    """
    srp_info = section[item]
    if srp_info.get('srp_capacity', {}).get('effective_used_capacity_percent'):
        used = srp_info.get('srp_capacity', {}).get('effective_used_capacity_percent')
    elif srp_info.get('fba_srp_capacity', {}).get('effective', {}).get('effective_used_percent'):
        used = srp_info.get('fba_srp_capacity', {}).get('effective', {}).get('effective_used_percent')

    if not used:
        yield Result(state=State.UNKNOWN, summary="got no data from agent")
        return

    yield from check_levels(
        used,
        metric_name='used',
        levels_upper=params['levels'],
        boundaries=(0, 100),
        label='Used',
        render_func=lambda v: f"{v}%",
    )

def discover_srp_physical_used(section):
    """
    Discover physical used capacity for SRP on PowerMax systems.
    """
    for item, data in section.items():
        if data.get('srp_capacity', {}).get('usable_used_tb'):
            yield Service(item=item)
        elif data.get('fba_srp_capacity', {}).get('effective', {}).get('physical_capacity', {}).get('used_tb'):
            yield Service(item=item)

def check_srp_physical_used(item, params, section):
    """
    Check physical used capacity for SRP on PowerMax systems.
    """
    if section[item].get('srp_capacity'):
        srp_info = section[item].get('srp_capacity')
        used_tb = srp_info.get('usable_used_tb')
        total_tb = srp_info.get('usable_total_tb')
    elif section[item].get('fba_srp_capacity', {}).get('effective', {}).get('physical_capacity'):
        srp_info = section[item].get('fba_srp_capacity', {}).get('effective', {}).get('physical_capacity')
        used_tb = srp_info.get('used_tb')
        total_tb = srp_info.get('total_tb')
    if not srp_info:
        return

    used = round((used_tb / total_tb)*100, 2)

    yield from check_levels(
        used,
        metric_name='used',
        levels_upper=params['levels'],
        boundaries=(0, 100),
        label='Used',
        render_func=lambda v: f"{v}%",
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
        # metric_name="ratio",
        levels_lower=params['levels'],
        label='current reduction ratio',
        render_func=lambda v: f"{v}:1",
    )
    yield Metric(
        name="Data_Reduction_Ratio_To_One",
        value=ratio,
        levels=params['levels'][1],
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
