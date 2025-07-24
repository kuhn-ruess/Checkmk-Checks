#!/usr/bin/env python
"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

#<<<unisphere_powermax_alert:sep(30)>>>
# Server Alert Summary
# {"warning_acknowledged_count": 0, "minor_acknowledged_count": 0, "all_unacknowledged_count": 0,
#  "normal_unacknowledged_count": 0, "critical_acknowledged_count": 0,
#  "normal_acknowledged_count": 0,
#  "warning_unacknowledged_count": 0, "alert_count": 0, "minor_unacknowledged_count": 0,
#  "all_acknowledged_count": 0, "critical_unacknowledged_count": 0, "info_acknowledged_count": 0,
#  "fatal_acknowledged_count": 0, "fatal_unacknowledged_count": 0, "info_unacknowledged_count": 0}

# SYMMETRIX_000297900497-RZ2_performance_alert_summary
# {"warning_acknowledged_count": 0, "minor_acknowledged_count": 0, "all_unacknowledged_count": 0,
#  "normal_unacknowledged_count": 0, "critical_acknowledged_count": 0,
#  "normal_acknowledged_count": 0,
#  "warning_unacknowledged_count": 0, "alert_count": 0, "minor_unacknowledged_count": 0,
#  "all_acknowledged_count": 0, "critical_unacknowledged_count": 0, "info_acknowledged_count": 0,
#  "fatal_acknowledged_count": 0, "fatal_unacknowledged_count": 0, "info_unacknowledged_count": 0}

# SYMMETRIX_000297900497-RZ2_array_alert_summary
# {"warning_acknowledged_count": 0, "minor_acknowledged_count": 0, "all_unacknowledged_count": 26,
#  "normal_unacknowledged_count": 19, "critical_acknowledged_count": 0,
#  "normal_acknowledged_count": 0,
#  "warning_unacknowledged_count": 7, "alert_count": 26, "minor_unacknowledged_count": 0,
#  "all_acknowledged_count": 0, "critical_unacknowledged_count": 0, "info_acknowledged_count": 0,
#  "fatal_acknowledged_count": 0, "fatal_unacknowledged_count": 0, "info_unacknowledged_count": 0}

# SYMMETRIX_000297900498-RZ1_performance_alert_summary
# {"warning_acknowledged_count": 0, "minor_acknowledged_count": 0, "all_unacknowledged_count": 1,
#  "normal_unacknowledged_count": 0, "critical_acknowledged_count": 0,
#  "normal_acknowledged_count": 0,
#  "warning_unacknowledged_count": 1, "alert_count": 1, "minor_unacknowledged_count": 0,
#  "all_acknowledged_count": 0, "critical_unacknowledged_count": 0, "info_acknowledged_count": 0,
#  "fatal_acknowledged_count": 0, "fatal_unacknowledged_count": 0, "info_unacknowledged_count": 0}

# SYMMETRIX_000297900498-RZ1_array_alert_summary
# {"warning_acknowledged_count": 0, "minor_acknowledged_count": 0, "all_unacknowledged_count": 4,
#  "normal_unacknowledged_count": 4, "critical_acknowledged_count": 0,
#  "normal_acknowledged_count": 0,
#  "warning_unacknowledged_count": 0, "alert_count": 4, "minor_unacknowledged_count": 0,
#  "all_acknowledged_count": 0, "critical_unacknowledged_count": 0, "info_acknowledged_count": 0,
#  "fatal_acknowledged_count": 0, "fatal_unacknowledged_count": 0, "info_unacknowledged_count": 0}


from cmk.agent_based.v2 import (
    Service,
    Result,
    State,
    CheckPlugin,
    AgentSection,
)

from .utils import parse_section

agent_section_unispere_powermax_alerts = AgentSection(
    name="unisphere_powermax_alerts",
    parse_function=parse_section,
)


def discover_alerts(section):
    """
    Discover alerts for PowerMax systems.
    """
    for item in section:
        yield Service(item=item)

def check_alerts(item, params, section):
    """
    Check alerts for PowerMax systems.
    """
    alert_data = section[item]

    for key, n_alerts in alert_data.items():
        severity = key.split('_')[0]
        if n_alerts > 0:
            yield Result(state=params['severity_map'].get(severity, State.WARN),
                         summary=f"{severity}: {n_alerts}")
        else:
            yield Result(state=State.OK, summary=f"{severity}: {n_alerts}")

check_plugin_unisphere_powermax_alerts = CheckPlugin(
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
