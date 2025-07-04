#!/usr/bin/env python3
"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.agent_based.v2 import (
    Result,
    Service,
    State,
    CheckPlugin,
)

"""
Example output:
<<<dellpmax_server_alerts:sep(124)>>>
serverAlertSummary|0|0|0
"""


def discover_dellpmax_server_alerts(section):
    if section != []:
        yield Service()


def check_dellpmax_server_alerts(section):
    if section:
        warn_unack = section[0][1]
        crit_unack = section[0][2]
        fatal_unack = section[0][3]
        sum_unack = int(warn_unack) + int(crit_unack) + int(fatal_unack)

        summary = f"{sum_unack} unacknowledged alerts found; " + \
                f"Warning: {warn_unack}, Critical: {crit_unack}, Fatal: {fatal_unack}"
        if sum_unack > 0:
            yield Result(state=State.CRIT, summary=summary)
        elif sum_unack == 0:
            yield Result(state=State.OK, summary=summary)

    else:
        yield Result(state=State.CRIT, summary="No server alerts available")


check_plugin_dell_pmax_server_alerts = CheckPlugin(
    name="dellpmax_server_alerts",
    discovery_function=discover_dellpmax_server_alerts,
    check_function=check_dellpmax_server_alerts,
    service_name="Server alerts",
)
