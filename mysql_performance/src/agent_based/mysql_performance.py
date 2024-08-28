#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
# +-----------------------------------------------------------------+
# |                                                                 |
# |        (  ___ \     | \    /\|\     /||\     /|( (    /|        |
# |        | (   ) )    |  \  / /| )   ( || )   ( ||  \  ( |        |
# |        | (__/ /     |  (_/ / | |   | || (___) ||   \ | |        |
# |        |  __ (      |   _ (  | |   | ||  ___  || (\ \) |        |
# |        | (  \ \     |  ( \ \ | |   | || (   ) || | \   |        |
# |        | )___) )_   |  /  \ \| (___) || )   ( || )  \  |        |
# |        |/ \___/(_)  |_/    \/(_______)|/     \||/    )_)        |
# |                                                                 |
# | Copyright Bastian Kuhn 2018                mail@bastian-kuhn.de |
# +-----------------------------------------------------------------+
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

from .agent_based_api.v1 import Metric, register, Result, Service, State


def discover_mysql_performance(section):
    for instance, data in section.items():
        if 'Threads_created' in data and 'Connections' in data:
            yield Service(item=f"{instance} Thread Cache", parameters={"levels": (80, 90)})


def check_mysql_performance(item, params, section):
    splitted = item.split()
    instance = splitted[0]
    if instance not in section:
        yield Result(state=State.UNKNOWN, summary="Instance Data not found in output")
        return
    data = section[instance]
    what = " ".join(splitted[1:])
    if what == "Thread Cache":
        created = float(data['Threads_created'])
        connections = float(data['Connections'])
        try:
            hitrate = round((created / connections) * 100, 4)
        except ZeroDivisionError:
            hitrate = 0

        # TODO
        warn, crit = 80, 90

        state = State.OK
        if hitrate >= crit:
            state = State.CRIT
        elif hitrate >= warn:
            state = State.WARN
        yield Result(state=state, summary="Thread Cache Hitrate: %s" % hitrate)
        yield Metric("percent", hitrate)


register.check_plugin(
    name = "mysql_performance",
    sections = ["mysql"],
    service_name = "MySQL %s",
    discovery_function = discover_mysql_performance,
    check_function = check_mysql_performance,
    check_default_parameters = {},
    check_ruleset_name = "mysql_tchitrate",
)
