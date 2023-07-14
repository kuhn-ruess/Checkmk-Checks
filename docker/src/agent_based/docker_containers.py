#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# Check status of docker containers
# Service is CRIT if container state is not "running"
#
# Author: lars.getwan@metrosystems.net
#
# 
# Plugin output:
#
# <<<docker_containers:sep(59)>>>
# /nervous_roentgen;Names=/nervous_roentgen;State=running;Status=Up 3 days;Created=1500541269;Command=nginx -g 'daemon off;';Image=nginx;SizeRootFs=107509836;SizeRw=2;CPU_pct=0.000000;Memory_used=1404928;Memory_limit=1040609280
# /nginx;Names=/nginx;State=running;Status=Up 4 days;Created=1499762426;Command=nginx -g 'daemon off;';Image=nginx;SizeRootFs=107912940;SizeRw=403106;CPU_pct=0.000000;Memory_used=2945024;Memory_limit=1040609280
# /hungry_liskov;Names=/hungry_liskov;State=running;Status=Up 3 days;Created=1499760925;Command=nginx -g 'daemon off;';Image=nginx;SizeRootFs=107509836;SizeRw=2;CPU_pct=0.000000;Memory_used=1396736;Memory_limit=1040609280
# /stoic_knuth;Names=/stoic_knuth;State=running;Status=Up 3 days;Created=1499760809;Command=nginx -g 'daemon off;';Image=nginx;SizeRootFs=107509836;SizeRw=2;CPU_pct=0.000000;Memory_used=1433600;Memory_limit=1040609280

import time

from contextlib import suppress
from cmk.base.plugins.agent_based.agent_based_api.v1 import (
    Metric,
    register,
    Result,
    Service,
    ServiceLabel,
    State,
    get_value_store,
    GetRateError,
)


def parse_docker_containers(string_table):
    parsed = {}
    for line in string_table:
        item = line[0][1:]
        parsed[item] = { key: value for key, value in
                map(lambda e: e.split("="), line[1:]) }
        if "Labels" in parsed[item]:
            parsed[item]["Labels"] = [
                    ServiceLabel(label_key, label_value) for label_key, label_value in
                    map(lambda e: e.split(":"), parsed[item]["Labels"].split("|"))
                ]
    return parsed


register.agent_section(
    name="docker_containers",
    parse_function=parse_docker_containers,
)


def discover_docker_containers(section):
    for item in section:
        yield Service(item=item, labels=section[item]["Labels"])


def get_docker_container_cpu(value_store, container):
    last_state = value_store.get("usage_counters")
    current_state = {
            "cpu_usage" : float(container["CPU_usage"]),
            "cpu_usage_system" : float(container["CPU_system_usage"]),
    }

    value_store["usage_counters"] = current_state
    if not last_state:
        raise GetRateError("Initialized usage counters")

    usage = current_state["cpu_usage"] - last_state["cpu_usage"]
    system_usage = current_state["cpu_usage_system"] - last_state["cpu_usage_system"]

    if usage < 0 or system_usage < 0:
        raise GetRateError("Value overflow")

    if system_usage == 0:
        raise GetRateError("No time difference")

    cpu_usage_percent = 100 * (usage / system_usage)
    return cpu_usage_percent



def check_docker_containers(item, section):
    value_store = get_value_store()
    container = section[item]

    if 'State' in container.keys():
        if container['State'] == 'running':
            yield Result(state=State.OK, summary="State = running")
        else:
            yield Result(state=State.CRIT, summary="State = %s" % container['State'])

        if "CPU_usage" in container and "CPU_system_usage" in container:
            with suppress(GetRateError):
                cpu_usage_percent = get_docker_container_cpu(value_store, container)
                yield Metric("CPU_pct", cpu_usage_percent, boundaries=(0, 100))
                yield Result(state=State.OK, summary="CPU_pct = %.1f" % cpu_usage_percent)

        for var in container.keys():

            if var not in ['State', 'Labels', 'time', 'CPU_usage', 'CPU_system_usage']:
                value = container[var]
                if var == 'Stats':
                    yield Result(state=State.WARN, summary="Note: %s" % value)
                else:
                    if var == 'Created':
                        value = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(value)))
                    elif var in ['SizeRootFs', 'SizeRw', 'Memory_used', 'Memory_limit']:
                        yield Metric(var, float(value))

                    yield Result(state=State.OK, summary="%s = %s" % (var, value))


register.check_plugin(
    name='docker_containers',
    service_name="Docker Container %s",
    discovery_function=discover_docker_containers,
    check_function=check_docker_containers,
)
