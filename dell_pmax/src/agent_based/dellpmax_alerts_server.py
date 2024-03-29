#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
# +------------------------------------------------------------+
# |              _               _              _              |
# |             | |             | |            | |             |
# |          ___| |__   ___  ___| | ___ __ ___ | | __          |
# |         / __| '_ \ / _ \/ __| |/ / '_ ` _ \| |/ /          |
# |        | (__| | | |  __/ (__|   <| | | | | |   <           |
# |         \___|_| |_|\___|\___|_|\_\_| |_| |_|_|\_\          |
# |                                   custom code by Nagarro   |
# |                                                            |
# +------------------------------------------------------------+
#
# Copyright (C)  2022  DevOps InfrastructureServices@nagarro-es.com
# for Nagarro ES GmbH


from .agent_based_api.v1 import (
    register,
    Result,
    Service,
    State
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


register.check_plugin(
    name="dellpmax_server_alerts",
    discovery_function=discover_dellpmax_server_alerts,
    check_function=check_dellpmax_server_alerts,
    service_name="Server alerts",
)
