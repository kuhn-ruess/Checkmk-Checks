#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
# +------------------------------------------------------------+
# |                                                            |
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

# Example Output
"""
<<<dellpmax_systeminfo>>>
sersion|V9.2.2.2

"""


def discover_dellpmax_info(section):
    yield Service()


def check_dellpmax_info(section):
    yield Result(state=State.OK, summary="PowerMax Unisphere version: {}".format(section[0][1]))


register.check_plugin(
    name="dellpmax_systeminfo",
    service_name="Version Info",
    discovery_function=discover_dellpmax_info,
    check_function=check_dellpmax_info,
)
