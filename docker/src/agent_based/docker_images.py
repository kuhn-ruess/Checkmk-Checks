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
    get_value_store,
    GetRateError,
)
from .docker_utils import get_docker_container_cpu
from contextlib import suppress

def get_running_image_containers(image_id, containers):
    return [c for c in containers if c.get("ImageID") == image_id and c.get("State") == "running"]


def get_docker_image_cpu(value_store, image_containers):
    raise_get_rate_error = False
    cpu_perc = 0
    for container in image_containers:
        try:
            cpu_perc += get_docker_container_cpu(value_store, container)
        except GetRateError:
            raise_get_rate_error = True
            continue
    if raise_get_rate_error:
        raise GetRateError
    return cpu_perc


def discover_docker_images(section_docker_images, section_docker_containers):
    for line in section_docker_images:
        yield Service(item=line[0])


def check_docker_images(item, section_docker_images, section_docker_containers):
    value_store = get_value_store()
    for line in section_docker_images:

        if line[0] == item:
            image = {}

            for kv in line[1:]:
                (key, value) = kv.split("=", 1)
                image[key] = value

            image_containers = get_running_image_containers(image["ImageID"], section_docker_containers.values())
            image["Running_containers"] = len(image_containers)
            image["Memory_used"] = sum(float(c["Memory_used"]) for c in image_containers)
            with suppress(GetRateError):
                image["CPU_pct"] = get_docker_image_cpu(value_store, image_containers)

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
    sections=['docker_images', 'docker_containers'],
    service_name="Docker Image %s",
    discovery_function=discover_docker_images,
    check_function=check_docker_images,
)
