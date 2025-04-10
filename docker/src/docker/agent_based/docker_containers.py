#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de


Monitor Docker Containers

Plugin Output:
 <<<docker_containers:sep(59)>>>
 /nervous_roentgen;Names=/nervous_roentgen;State=running;Status=Up 3 days;Created=1500541269;Command=nginx -g 'daemon off;';Image=nginx;SizeRootFs=107509836;SizeRw=2;CPU_pct=0.000000;Memory_used=1404928;Memory_limit=1040609280
 /nginx;Names=/nginx;State=running;Status=Up 4 days;Created=1499762426;Command=nginx -g 'daemon off;';Image=nginx;SizeRootFs=107912940;SizeRw=403106;CPU_pct=0.000000;Memory_used=2945024;Memory_limit=1040609280
 /hungry_liskov;Names=/hungry_liskov;State=running;Status=Up 3 days;Created=1499760925;Command=nginx -g 'daemon off;';Image=nginx;SizeRootFs=107509836;SizeRw=2;CPU_pct=0.000000;Memory_used=1396736;Memory_limit=1040609280
 /stoic_knuth;Names=/stoic_knuth;State=running;Status=Up 3 days;Created=1499760809;Command=nginx -g 'daemon off;';Image=nginx;SizeRootFs=107509836;SizeRw=2;CPU_pct=0.000000;Memory_used=1433600;Memory_limit=1040609280
"""

import time
from contextlib import suppress

from cmk.agent_based.v2 import (
    Metric,
    Result,
    Service,
    ServiceLabel,
    State,
    get_rate,
    get_value_store,
    GetRateError,
    AgentSection,
    CheckPlugin
)
from cmk.agent_based.v2.render import (
    bytes,
    percent,
)
from cmk.plugins.lib.cpu_util import check_cpu_util

from .docker_utils import get_docker_container_cpu, SectionCpuUtilizationOs


def parse_docker_containers(string_table):
    """
    Parser
    """
    parsed = {}
    for line in string_table:
        item = line[0][1:]
        parsed[item] = dict(map(lambda e: e.split("=", 1), line[1:]))
        if "Labels" in parsed[item]:
            parsed[item]["Labels"] = [
                    ServiceLabel(label_key, label_value) for label_key, label_value in
                    map(lambda e: e.split(":"), parsed[item]["Labels"].split("|"))
                ]
        else:
            parsed[item]['Labels'] = {}

    return parsed


agent_section_docker = AgentSection(
    name="docker_containers",
    parse_function=parse_docker_containers,
)


def discover_docker_containers(section):
    """
    Docker Containers Discovery
    """
    for item in section:
        yield Service(item=item, labels=section[item]["Labels"])


def check_docker_containers(item, section):
    """
    Docker Containers Check
    """
    container = section[item]

    if 'State' in container.keys():
        if container['State'] == 'running':
            yield Result(state=State.OK, summary="State = running")
        else:
            yield Result(state=State.CRIT, summary=f"State = {container['State']}")

        if "CPU_usage" in container and "CPU_system_usage" in container:
            with suppress(GetRateError):
                cpu_usage_percent = get_docker_container_cpu(get_value_store(), container)
                yield Metric("CPU_pct", cpu_usage_percent, boundaries=(0, 100))
                yield Result(state=State.OK, summary=f"CPU_pct = {percent(cpu_usage_percent)}")

        if "cpu_num" in container and "system_ticks" in container and "container_ticks" in container:
            section = SectionCpuUtilizationOs(
                time_base=int(container["system_ticks"]) / int(container["cpu_num"]),
                time_cpu=int(container["container_ticks"]),
                num_cpus=int(container["cpu_num"]),
            )

            util = get_rate(
                value=section.time_cpu,
                time=section.time_base,
                key="util",
                value_store=get_value_store(),
            )

            yield from check_cpu_util(
                util=util * 100,
                params={},
                this_time=section.time_base,
                value_store=get_value_store(),
            )

        for var in container.keys():

            if var not in ['State', 'Labels', 'time', 'CPU_usage', 'CPU_system_usage', 'cpu_num', 'system_ticks', 'container_ticks']:
                value = container[var]
                if var == 'Stats':
                    yield Result(state=State.WARN, summary=f"Note: {value}")
                else:
                    if var == 'Created':
                        value = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(value)))
                    elif var in ['SizeRootFs', 'SizeRw', 'Memory_used', 'Memory_limit']:
                        yield Metric(var, float(value))
                        yield Result(state=State.OK, summary=f"{var} = {bytes(value)}")
                    else:
                        yield Result(state=State.OK, summary=f"{var} = {value}")


check_plugin_docker_containers = CheckPlugin(
    name='docker_containers',
    service_name="Docker Container %s",
    discovery_function=discover_docker_containers,
    check_function=check_docker_containers,
)
