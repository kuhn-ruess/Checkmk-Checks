#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#<<<unisphere_powermax_srp:sep(30)>>>
#SYMMETRIX_000297900498_SRP_1{"total_srdf_dse_allocated_cap_gb": 0.0, "srp_efficiency": {"compression_state": "Enabled", "data_reduction_enabled_percent": 100.0, "data_reduction_ratio_to_one": 2.6, "overall_efficiency_ratio_to_one": 8.0, "virtual_provisioning_savings_ratio_to_one": 3.1}, "srp_capacity": {"subscribed_total_tb": 263.96, "effective_used_capacity_percent": 23, "usable_used_tb": 34.32, "usable_total_tb": 171.15, "snapshot_modified_tb": 0.0, "subscribed_allocated_tb": 86.1, "snapshot_total_tb": 0.0}, "srpId": "SRP_1", "num_of_disk_groups": 1, "rdfa_dse": true, "emulation": "FBA", "diskGroupId": ["1"], "reserved_cap_percent": 10}
#SYMMETRIX_000297900497_SRP_1{"total_srdf_dse_allocated_cap_gb": 0.0, "srp_efficiency": {"compression_state": "Enabled", "data_reduction_enabled_percent": 99.0, "data_reduction_ratio_to_one": 2.6, "overall_efficiency_ratio_to_one": 8.0, "virtual_provisioning_savings_ratio_to_one": 3.1}, "srp_capacity": {"subscribed_total_tb": 264.11, "effective_used_capacity_percent": 23, "usable_used_tb": 34.27, "usable_total_tb": 171.15, "snapshot_modified_tb": 0.0, "subscribed_allocated_tb": 85.89, "snapshot_total_tb": 0.0}, "srpId": "SRP_1", "num_of_disk_groups": 1, "rdfa_dse": true, "emulation": "FBA", "diskGroupId": ["1"], "reserved_cap_percent": 10}


import json
from pprint import pprint

from .agent_based_api.v1 import (
    register,
    Service,
    Result,
    State,
    Metric,
)

def discover_srp_effective_used(section):
    for i in section:
        j = json.loads(i[1])
        if j.get('srp_capacity', {}).get('effective_used_capacity_percent', None) is not None:
            yield Service(item=i[0])

def check_srp_effective_used(item, params, section):
    srp_info = list(filter(lambda x: x[0] == item, section))
    if len(srp_info) != 1:
        return

    srp = srp_info[0][0]
    srp_data = json.loads(srp_info[0][1])

    state = State.OK
    info_text = ""
    used = srp_data.get('srp_capacity', {}).get('effective_used_capacity_percent', None)

    if used is None:
       yield Result(state=State.UNKNOWN, summary="got no data from agent")
       return
    
    info_text = "used: %s %% (warn/crit %s/%s)" % ((used,) + params['levels'])
    if used >= params['levels'][1]:
        state = State.CRIT
    elif used >= params['levels'][0]:
        state = State.WARN
    perfdata = [('used', "{}%".format(used), params['levels'][0], params['levels'][1])]

    yield Metric(name="used", value=used, levels=(params['levels'][0], params['levels'][1]), boundaries=(0, 100))
    yield Result(state=state, summary=info_text)

def discover_srp_physical_used(section):
    for i in section:
        j = json.loads(i[1])
        if j.get('srp_capacity', {}).get('usable_used_tb', None) is not None:
            yield Service(item=i[0])

def check_srp_physical_used(item, params, section):
    srp_info = list(filter(lambda x: x[0] == item, section))
    if len(srp_info) != 1:
        return

    srp = srp_info[0][0]
    srp_data = json.loads(srp_info[0][1])

    state = State.OK
    info_text = ""
    used_tb = srp_data.get('srp_capacity', {}).get('usable_used_tb', None)
    total_tb = srp_data.get('srp_capacity', {}).get('usable_total_tb', None)
    

    if used_tb is None or total_tb is None:
       yield Result(state=State.UNKNOWN, summary="got no data from agent")
       return
    
    used = round((used_tb / total_tb)*100, 2)
    
    info_text = "used: %s %% (warn/crit %s/%s)" % ((used,) + params['levels'])
    if used >= params['levels'][1]:
        state = State.CRIT
    elif used >= params['levels'][0]:
        state = State.WARN
    perfdata = [('used', "{}%".format(used), params['levels'][0], params['levels'][1])]

    yield Metric(name="used", value=used, levels=(params['levels'][0], params['levels'][1]), boundaries=(0, 100))
    yield Result(state=state, summary=info_text)

def discover_srp_data_reduction_ratio(section):
    for i in section:
        j = json.loads(i[1])
        if j.get('srp_efficiency', {}).get('data_reduction_ratio_to_one', None) is not None:
            yield Service(item=i[0])

def check_srp_data_reduction_ratio(item, params, section):
    srp_info = list(filter(lambda x: x[0] == item, section))
    if len(srp_info) != 1:
        return

    srp = srp_info[0][0]
    srp_data = json.loads(srp_info[0][1])

    state = State.OK
    info_text = ""
    ratio = srp_data.get('srp_efficiency', {}).get('data_reduction_ratio_to_one', None)
    

    if ratio is None:
       yield Result(state=State.UNKNOWN, summary="got no data from agent")
       return
    
    info_text = "current reduction ratio: %s:1 (warn/crit <=%s/<=%s)" % ((ratio,) + params['levels'])
    if ratio <= params['levels'][1]:
        state = State.CRIT
    elif ratio <= params['levels'][0]:
        state = State.WARN
    perfdata = [('data_reduction_ratio_to_one', "{}".format(ratio), params['levels'][0], params['levels'][1])]

    yield Metric(name="data_reduction_ratio_to_one", value=ratio, levels=(params['levels'][0], params['levels'][1]))
    yield Result(state=state, summary=info_text)

register.check_plugin(
    name = "unisphere_powermax_srp_effective_used",
    sections = ['unisphere_powermax_srp'],
    service_name = 'Effective SRP Capacity %s',
    discovery_function = discover_srp_effective_used,
    check_function = check_srp_effective_used,
    check_ruleset_name="unisphere_powermax_srp_effective_used",
    check_default_parameters = {"levels": (80, 90)}
)

register.check_plugin(
    name = "unisphere_powermax_srp_physical_used",
    sections = ['unisphere_powermax_srp'],
    service_name = 'Physical SRP Capacity %s',
    discovery_function = discover_srp_physical_used,
    check_function = check_srp_physical_used,
    check_ruleset_name = 'unisphere_powermax_srp_physical_used',
    check_default_parameters = {"levels": (80, 90)}
)

register.check_plugin(
    name = "unisphere_powermax_srp_data_reduction_ratio",
    sections = ['unisphere_powermax_srp'],
    service_name = 'SRP Data Reduction Ratio %s',
    discovery_function = discover_srp_data_reduction_ratio,
    check_function = check_srp_data_reduction_ratio,
    check_ruleset_name = 'unisphere_powermax_srp_data_reduction_ratio',
    check_default_parameters = {"levels": (3.0, 2.0)}
)
