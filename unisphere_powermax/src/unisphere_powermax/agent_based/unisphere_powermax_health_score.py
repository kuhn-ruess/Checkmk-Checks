#!/usr/bin/env python3
"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#<<<unisphere_powermax_health_score:sep(30)>>>
#SYMMETRIX_000297900498-RZ1{"num_failed_disks": 0, "health_score_metric": [{"cached_date": 1615380648222, "metric": "SERVICE_LEVEL_COMPLIANCE", "health_score": 100.0, "data_date": 1615380648222, "instance_metrics": [{"health_score_instance_metric": []}], "expired": false}, {"metric": "OVERALL", "instance_metrics": [{"health_score_instance_metric": []}], "expired": false, "data_date": 0, "cached_date": 0}, {"cached_date": 1615380648219, "metric": "CAPACITY", "health_score": 100.0, "data_date": 1615380648219, "instance_metrics": [{"health_score_instance_metric": []}], "expired": false}]}
#SYMMETRIX_000297900497-RZ2{"num_failed_disks": 0, "health_check": ["1589178461376"], "health_score_metric": [{"cached_date": 1615381805024, "metric": "SERVICE_LEVEL_COMPLIANCE", "health_score": 95.0, "data_date": 1615381805024, "instance_metrics": [{"health_score_instance_metric": [{"instance_name": "Storage Group sg_s23esx48_r2 is out of compliance", "metric_category": "SG", "health_score_reduction": 5.0, "metric_name": "Service Level Health Score", "severity": "Critical"}, {"instance_name": "Storage Group sg_ucs-prod1_r1 is out of compliance", "metric_category": "SG", "health_score_reduction": 5.0, "metric_name": "Service Level Health Score", "severity": "Critical"}, {"instance_name": "Storage Group sg_ucs-prod4_r2 is out of compliance", "metric_category": "SG", "health_score_reduction": 5.0, "metric_name": "Service Level Health Score", "severity": "Critical"}, {"instance_name": "Storage Group pg_sapmast_VBE is out of compliance", "metric_category": "SG", "health_score_reduction": 5.0, "metric_name": "Service Level Health Score", "severity": "Critical"}, {"instance_name": "Storage Group pg_sapmast_VUL is out of compliance", "metric_category": "SG", "health_score_reduction": 5.0, "metric_name": "Service Level Health Score", "severity": "Critical"}, {"instance_name": "Storage Group sg_sapkons_VAK is out of compliance", "metric_category": "SG", "health_score_reduction": 5.0, "metric_name": "Service Level Health Score", "severity": "Critical"}, {"instance_name": "Storage Group sg_vapdb_SAMBA is out of compliance", "metric_category": "SG", "health_score_reduction": 5.0, "metric_name": "Service Level Health Score", "severity": "Critical"}, {"instance_name": "Storage Group sg_mach2_prod_r1 is out of compliance", "metric_category": "SG", "health_score_reduction": 5.0, "metric_name": "Service Level Health Score", "severity": "Critical"}, {"instance_name": "Storage Group sg_mssql_r1 is out of compliance", "metric_category": "SG", "health_score_reduction": 5.0, "metric_name": "Service Level Health Score", "severity": "Critical"}, {"instance_name": "Storage Group sg_d11ovirtnode03_boot is out of compliance", "metric_category": "SG", "health_score_reduction": 5.0, "metric_name": "Service Level Health Score", "severity": "Critical"}, {"instance_name": "Storage Group sg_ovirt_cluster_dev is out of compliance", "metric_category": "SG", "health_score_reduction": 5.0, "metric_name": "Service Level Health Score", "severity": "Critical"}, {"instance_name": "Storage Group sg_d11ovirtnode04_boot is out of compliance", "metric_category": "SG", "health_score_reduction": 5.0, "metric_name": "Service Level Health Score", "severity": "Critical"}, {"instance_name": "Storage Group sg_d11ovirtnode05_boot is out of compliance", "metric_category": "SG", "health_score_reduction": 5.0, "metric_name": "Service Level Health Score", "severity": "Critical"}, {"instance_name": "Storage Group sg_d11ovirtnode06_boot is out of compliance", "metric_category": "SG", "health_score_reduction": 5.0, "metric_name": "Service Level Health Score", "severity": "Critical"}]}], "expired": false}, {"cached_date": 1615381805024, "metric": "OVERALL", "health_score": 95.0, "data_date": 1615381805000, "instance_metrics": [{"health_score_instance_metric": []}], "expired": false}, {"cached_date": 1615381805024, "metric": "CAPACITY", "health_score": 100.0, "data_date": 1615381805024, "instance_metrics": [{"health_score_instance_metric": []}], "expired": false}, {"cached_date": 1615381805024, "metric": "CONFIGURATION", "health_score": 100.0, "data_date": 1615381805024, "instance_metrics": [{"health_score_instance_metric": []}], "expired": false}, {"cached_date": 1615381805024, "metric": "SYSTEM_UTILIZATION", "health_score": 100.0, "data_date": 1615381805000, "instance_metrics": [{"health_score_instance_metric": []}], "expired": false}, {"cached_date": 1615381805024, "metric": "STORAGE_GROUP_RESPONSE_TIME", "health_score": 100.0, "data_date": 1615381805000, "instance_metrics": [{"health_score_instance_metric": []}], "expired": false}]}


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

agent_section_unispere_powermax_health_score = AgentSection(
    name="unisphere_powermax_health_score",
    parse_function=parse_section,
)

def discover_health(section):
    """
    Discover health scores for PowerMax systems.
    """
    for item in section:
        yield Service(item=item)


def check_health(item, params, section):
    """
    Check health scores for PowerMax systems.
    """
    score = section[item].get('health_score')

    if not score:
        yield Result(state=State.UNKNOWN, summary="got no data from agent")
        return

    yield from check_levels(
        score,
        levels_lower=params['levels'],
        # metric_name="health_score",
        label="Health Score",
        render_func=lambda v: f"{v}",
    )
    yield Metric(
        name="health_score",
        value=score,
        levels=params['levels'][1],
        boundaries=(0, 100),
    )


check_plugin_unisphere_powermax_health_score = CheckPlugin(
    name = "unisphere_powermax_health_score",
    service_name = 'Health Score %s',
    discovery_function = discover_health,
    check_function = check_health,
    check_ruleset_name="unisphere_powermax_health_score",
    check_default_parameters = {"levels": ('fixed',(90, 80))}
)
