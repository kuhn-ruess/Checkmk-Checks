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

from cmk.base.plugins.agent_based.agent_based_api.v1 import (
    Metric,
    register,
    Result,
    Service,
    ServiceLabel,
    State,
)

def discover_docker_containers(section):
    for line in section:
        service_labels = []
        for kv in line[1:]:
            (key, value) = kv.split("=", 1)
            if key == "Labels":
                for label in value.split("|"):
                    label_key, label_value = label.split(":")
                    service_labels.append(ServiceLabel(
                            "whitelist/" + label_key,
                            label_value
                        ))
        yield Service(item=line[0][1:], labels=service_labels)


def check_docker_containers(item, section):
    for line in section:
        if line[0][1:] == item:
            container = {}

            for kv in line[1:]:
                (key, value) = kv.split("=", 1)
                container[key] = value

            if 'State' in container.keys():
                if container['State'] == 'running':
                    yield Result(state=State.OK, summary="State = running")
                else:
                    yield Result(state=State.CRIT, summary="State = %s" % container['State'])

                for var in container.keys():

                    if var != 'State' and var != 'Labels':
                        value = container[var]
                        if var == 'Stats':
                            yield Result(state=State.WARN, summary="Note: %s" % value)
                        else:
                            if var == 'Created':
                                value = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(value)))


                            if var in ['CPU_pct']:
                                yield Metric(var, float(value), boundaries=(0, 100))

                            if var in ['SizeRootFs', 'SizeRw', 'Memory_used', 'Memory_limit']:
                                yield Metric(var, float(value))

                            yield Result(state=State.OK, summary="%s = %s" % (var, value))


register.check_plugin(
    name='docker_containers',
    service_name="Docker Container %s",
    discovery_function=discover_docker_containers,
    check_function=check_docker_containers,
)
