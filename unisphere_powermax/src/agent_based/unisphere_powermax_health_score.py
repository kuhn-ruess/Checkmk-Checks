#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#<<<unisphere_powermax_health_score:sep(30)>>>
#SYMMETRIX_000297900498-RZ1{"num_failed_disks": 0, "health_score_metric": [{"cached_date": 1615380648222, "metric": "SERVICE_LEVEL_COMPLIANCE", "health_score": 100.0, "data_date": 1615380648222, "instance_metrics": [{"health_score_instance_metric": []}], "expired": false}, {"metric": "OVERALL", "instance_metrics": [{"health_score_instance_metric": []}], "expired": false, "data_date": 0, "cached_date": 0}, {"cached_date": 1615380648219, "metric": "CAPACITY", "health_score": 100.0, "data_date": 1615380648219, "instance_metrics": [{"health_score_instance_metric": []}], "expired": false}]}
#SYMMETRIX_000297900497-RZ2{"num_failed_disks": 0, "health_check": ["1589178461376"], "health_score_metric": [{"cached_date": 1615381805024, "metric": "SERVICE_LEVEL_COMPLIANCE", "health_score": 95.0, "data_date": 1615381805024, "instance_metrics": [{"health_score_instance_metric": [{"instance_name": "Storage Group sg_s23esx48_r2 is out of compliance", "metric_category": "SG", "health_score_reduction": 5.0, "metric_name": "Service Level Health Score", "severity": "Critical"}, {"instance_name": "Storage Group sg_ucs-prod1_r1 is out of compliance", "metric_category": "SG", "health_score_reduction": 5.0, "metric_name": "Service Level Health Score", "severity": "Critical"}, {"instance_name": "Storage Group sg_ucs-prod4_r2 is out of compliance", "metric_category": "SG", "health_score_reduction": 5.0, "metric_name": "Service Level Health Score", "severity": "Critical"}, {"instance_name": "Storage Group pg_sapmast_VBE is out of compliance", "metric_category": "SG", "health_score_reduction": 5.0, "metric_name": "Service Level Health Score", "severity": "Critical"}, {"instance_name": "Storage Group pg_sapmast_VUL is out of compliance", "metric_category": "SG", "health_score_reduction": 5.0, "metric_name": "Service Level Health Score", "severity": "Critical"}, {"instance_name": "Storage Group sg_sapkons_VAK is out of compliance", "metric_category": "SG", "health_score_reduction": 5.0, "metric_name": "Service Level Health Score", "severity": "Critical"}, {"instance_name": "Storage Group sg_vapdb_SAMBA is out of compliance", "metric_category": "SG", "health_score_reduction": 5.0, "metric_name": "Service Level Health Score", "severity": "Critical"}, {"instance_name": "Storage Group sg_mach2_prod_r1 is out of compliance", "metric_category": "SG", "health_score_reduction": 5.0, "metric_name": "Service Level Health Score", "severity": "Critical"}, {"instance_name": "Storage Group sg_mssql_r1 is out of compliance", "metric_category": "SG", "health_score_reduction": 5.0, "metric_name": "Service Level Health Score", "severity": "Critical"}, {"instance_name": "Storage Group sg_d11ovirtnode03_boot is out of compliance", "metric_category": "SG", "health_score_reduction": 5.0, "metric_name": "Service Level Health Score", "severity": "Critical"}, {"instance_name": "Storage Group sg_ovirt_cluster_dev is out of compliance", "metric_category": "SG", "health_score_reduction": 5.0, "metric_name": "Service Level Health Score", "severity": "Critical"}, {"instance_name": "Storage Group sg_d11ovirtnode04_boot is out of compliance", "metric_category": "SG", "health_score_reduction": 5.0, "metric_name": "Service Level Health Score", "severity": "Critical"}, {"instance_name": "Storage Group sg_d11ovirtnode05_boot is out of compliance", "metric_category": "SG", "health_score_reduction": 5.0, "metric_name": "Service Level Health Score", "severity": "Critical"}, {"instance_name": "Storage Group sg_d11ovirtnode06_boot is out of compliance", "metric_category": "SG", "health_score_reduction": 5.0, "metric_name": "Service Level Health Score", "severity": "Critical"}]}], "expired": false}, {"cached_date": 1615381805024, "metric": "OVERALL", "health_score": 95.0, "data_date": 1615381805000, "instance_metrics": [{"health_score_instance_metric": []}], "expired": false}, {"cached_date": 1615381805024, "metric": "CAPACITY", "health_score": 100.0, "data_date": 1615381805024, "instance_metrics": [{"health_score_instance_metric": []}], "expired": false}, {"cached_date": 1615381805024, "metric": "CONFIGURATION", "health_score": 100.0, "data_date": 1615381805024, "instance_metrics": [{"health_score_instance_metric": []}], "expired": false}, {"cached_date": 1615381805024, "metric": "SYSTEM_UTILIZATION", "health_score": 100.0, "data_date": 1615381805000, "instance_metrics": [{"health_score_instance_metric": []}], "expired": false}, {"cached_date": 1615381805024, "metric": "STORAGE_GROUP_RESPONSE_TIME", "health_score": 100.0, "data_date": 1615381805000, "instance_metrics": [{"health_score_instance_metric": []}], "expired": false}]}

import json
from pprint import pprint

from .agent_based_api.v1 import (
    register,
    Service,
    Result,
    State,
    Metric,
)


def discover_health(section):
    for i in section:
        j = json.loads(i[1])
        if j.get('health_score', None) is not None:
            yield Service(item=i[0])

def check_health(item, params, section):
    health_info = list(filter(lambda x: x[0] == item, section))
    if len(health_info) != 1:
        return

    metric = health_info[0][0]
    metric_data = json.loads(health_info[0][1])

    state = State.OK
    info_text = ""
    score = metric_data.get('health_score', None)

    if score is None:
       yield Result(state=State.UNKNOWN, summary="got no data from agent")
       return
    
    info_text = "health score: %s %% (warn/crit <=%s/<=%s)" % ((score,) + params['levels'])
    if score <= params['levels'][1]:
        state = State.CRIT
    elif score <= params['levels'][0]:
        state = State.WARN
    perfdata = [('health_score', "{}%".format(score), params['levels'][0], params['levels'][1])]

    yield Metric(name='health_score', 
                 value=score,
                 levels=(params['levels'][0], params['levels'][1]),
                 boundaries=(0, 100))

    yield Result(state=state, summary=info_text)
    
register.check_plugin(
    name = "unisphere_powermax_health_score",
    service_name = 'Health Score %s',
    discovery_function = discover_health,
    check_function = check_health,
    check_ruleset_name="unisphere_powermax_health_score",
    check_default_parameters = {"levels": (90, 80)}
)
