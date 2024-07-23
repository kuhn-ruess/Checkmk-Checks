#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#<<<unisphere_powermax_alert:sep(30)>>>
#Server Alert Summary{"warning_acknowledged_count": 0, "minor_acknowledged_count": 0, "all_unacknowledged_count": 0, "normal_unacknowledged_count": 0, "critical_acknowledged_count": 0, "normal_acknowledged_count": 0, "warning_unacknowledged_count": 0, "alert_count": 0, "minor_unacknowledged_count": 0, "all_acknowledged_count": 0, "critical_unacknowledged_count": 0, "info_acknowledged_count": 0, "fatal_acknowledged_count": 0, "fatal_unacknowledged_count": 0, "info_unacknowledged_count": 0}
#SYMMETRIX_000297900497-RZ2_performance_alert_summary{"warning_acknowledged_count": 0, "minor_acknowledged_count": 0, "all_unacknowledged_count": 0, "normal_unacknowledged_count": 0, "critical_acknowledged_count": 0, "normal_acknowledged_count": 0, "warning_unacknowledged_count": 0, "alert_count": 0, "minor_unacknowledged_count": 0, "all_acknowledged_count": 0, "critical_unacknowledged_count": 0, "info_acknowledged_count": 0, "fatal_acknowledged_count": 0, "fatal_unacknowledged_count": 0, "info_unacknowledged_count": 0}
#SYMMETRIX_000297900497-RZ2_array_alert_summary{"warning_acknowledged_count": 0, "minor_acknowledged_count": 0, "all_unacknowledged_count": 26, "normal_unacknowledged_count": 19, "critical_acknowledged_count": 0, "normal_acknowledged_count": 0, "warning_unacknowledged_count": 7, "alert_count": 26, "minor_unacknowledged_count": 0, "all_acknowledged_count": 0, "critical_unacknowledged_count": 0, "info_acknowledged_count": 0, "fatal_acknowledged_count": 0, "fatal_unacknowledged_count": 0, "info_unacknowledged_count": 0}
#SYMMETRIX_000297900498-RZ1_performance_alert_summary{"warning_acknowledged_count": 0, "minor_acknowledged_count": 0, "all_unacknowledged_count": 1, "normal_unacknowledged_count": 0, "critical_acknowledged_count": 0, "normal_acknowledged_count": 0, "warning_unacknowledged_count": 1, "alert_count": 1, "minor_unacknowledged_count": 0, "all_acknowledged_count": 0, "critical_unacknowledged_count": 0, "info_acknowledged_count": 0, "fatal_acknowledged_count": 0, "fatal_unacknowledged_count": 0, "info_unacknowledged_count": 0}
#SYMMETRIX_000297900498-RZ1_array_alert_summary{"warning_acknowledged_count": 0, "minor_acknowledged_count": 0, "all_unacknowledged_count": 4, "normal_unacknowledged_count": 4, "critical_acknowledged_count": 0, "normal_acknowledged_count": 0, "warning_unacknowledged_count": 0, "alert_count": 4, "minor_unacknowledged_count": 0, "all_acknowledged_count": 0, "critical_unacknowledged_count": 0, "info_acknowledged_count": 0, "fatal_acknowledged_count": 0, "fatal_unacknowledged_count": 0, "info_unacknowledged_count": 0}



import json
from pprint import pprint

from .agent_based_api.v1 import (
    register,
    Service,
    Result,
    State,
    Metric,
)


def discover_alerts(section):
    for i in section:
        j = json.loads(i[1])
        if j.get('alert_count', None) is not None:
            yield Service(item=i[0])

def check_alerts(item, params, section):
    alert_info = list(filter(lambda x: x[0] == item, section))
    if len(alert_info) != 1:
        return

    alert_data = json.loads(alert_info[0][1])

    info_text = "unacknowledged alerts: "

    state = State.OK

    for key in filter(lambda x: 'unacknowledged' in x and x.split('_')[0] in params['severity_map'].keys(), alert_data.keys()):
        severity = key.split('_')[0]
        n_alerts = alert_data[key]
        if n_alerts > 0:
            yield Result(state=params['severity_map'].get(severity, State.WARN), summary="{}: {}".format(severity, n_alerts))
        else:
            yield Result(state=State.OK, summary="{}: {}".format(severity, n_alerts))


register.check_plugin(
    name = "unisphere_powermax_alerts",
    service_name = 'Alerts - %s',
    discovery_function = discover_alerts,
    check_function = check_alerts,
    check_default_parameters = {'severity_map': {'fatal': State.CRIT,
                                                 'critical': State.CRIT,
                                                 'minor': State.WARN,
                                                 'warning': State.WARN,
                                                 'info': State.OK
                                                }}
)
