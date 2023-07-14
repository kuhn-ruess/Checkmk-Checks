#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# Check status of docker images
# Service is always OK. Just for collecting data in phase 1
#
# Author: lars.getwan@metrosystems.net
#
# 
# Plugin output:
#
# <<<docker_images:sep(59)>>>
# nginx:latest;Running_containers=7;Diskspace_used=107912952;CPU_pct=0.000000;Memory_used=11476992
# ubuntu:latest;Running_containers=2;Diskspace_used=119174159;CPU_pct=0.000000;Memory_used=561152
# hello-world:latest;Running_containers=0;Diskspace_used=1840;CPU_pct=0.000000;Memory_used=0

from cmk.base.plugins.agent_based.agent_based_api.v1 import (
    Metric,
    register,
    Result,
    Service,
    State,
)

def discover_docker_images(section):
    for line in section:
        yield Service(item=line[0])


def check_docker_images(item, section):
    for line in section:

        if line[0] == item:
            image = {}

            for kv in line[1:]:
                (key, value) = kv.split("=", 1)
                image[key] = value

            for var in image.keys():
                value = image[var]
                if var == 'Stats':
                    yield Result(state=State.WARN, summary="Note: %s" % value)
                elif var == 'ImageID':
                    continue
                else:
                    yield Result(state=State.OK, summary="%s = %.2f" % (var, float(value)))

                if var in ['CPU_pct']:
                    yield Metric(var, float(value), boundaries=(0, 100))

                if var in ['Diskspace_used', 'Memory_used', 'Running_containers']:
                    yield Metric(var, float(value))


register.check_plugin(
    name='docker_images',
    service_name="Docker Image %s",
    discovery_function=discover_docker_images,
    check_function=check_docker_images,
)
