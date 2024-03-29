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
<<<dellpmax_symm_alerts:sep(124)>>>
symmAlertSummary|0|0|0|0|0|0
"""


def discover_dellpmax_alerts(section):
    if section != []:
        yield Service()


def check_dellpmax_alerts_array(section):
    if section:
        array_warn_unack = int(section[0][1])
        array_crit_unack = int(section[0][2])
        array_fatal_unack = int(section[0][3])
        array_sum = array_warn_unack + array_crit_unack + array_fatal_unack

        summary = (
            "%s unacknowledged array alerts found; "
            + "Warning: %s, "
            + "Critical: %s, "
            + "Fatal: %s"
        ) % (array_sum, array_warn_unack, array_crit_unack, array_fatal_unack)
        if array_crit_unack > 0 or array_fatal_unack > 0:
            yield Result(state=State.CRIT, summary=summary)
        if array_warn_unack > 0:
            yield Result(state=State.WARN, summary=summary)
        else:
            yield Result(state=State.OK, summary=summary)
    else:
        yield Result(state=State.CRIT, summary="No alert data available")


register.check_plugin(
    name="dellpmax_symm_alerts_arrays",
    sections=["dellpmax_symm_alerts"],
    service_name="Array alerts",
    discovery_function=discover_dellpmax_alerts,
    check_function=check_dellpmax_alerts_array,
)


def check_dellpmax_alerts_perf(section):
    if section:
        perf_warn_unack = int(section[0][4])
        perf_crit_unack = int(section[0][5])
        perf_fatal_unack = int(section[0][6])
        perf_sum = perf_warn_unack + perf_crit_unack + perf_fatal_unack

        summary = (
            "%s unacknowledged performance alerts found; "
            + "Warning: %s, "
            + "Critical: %s, "
            + "Fatal: %s"
        ) % (perf_sum, perf_warn_unack, perf_crit_unack, perf_fatal_unack)

        if perf_crit_unack > 0 or perf_fatal_unack > 0:
            yield Result(state=State.CRIT, summary=summary)
        elif perf_warn_unack > 0:
            yield Result(state=State.WARN, summary=summary)
        else:
            yield Result(state=State.OK, summary=summary)
    else:
        yield Result(state=State.CRIT, summary="No alert data available")


register.check_plugin(
    name="dellpmax_symm_alerts_performance",
    sections=["dellpmax_symm_alerts"],
    service_name="Performance alerts",
    discovery_function=discover_dellpmax_alerts,
    check_function=check_dellpmax_alerts_perf,
)
