#!/usr/bin/env python3
"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de


Docker Image Monitoring
"""
# Plugin output:
#
# <<<docker_images:sep(59)>>>
# nginx:latest;Running_containers=7;Diskspace_used=107912952;CPU_pct=0.000000;Memory_used=11476992
# ubuntu:latest;Running_containers=2;Diskspace_used=119174159;CPU_pct=0.000000;Memory_used=561152
# hello-world:latest;Running_containers=0;Diskspace_used=1840;CPU_pct=0.000000;Memory_used=0

from contextlib import suppress
from cmk.agent_based.v2 import (
    CheckPlugin,
    Metric,
    Result,
    Service,
    State,
    get_value_store,
    GetRateError,
    AgentSection,
)

from .docker_utils import get_docker_container_cpu

def parse_docker_images(string_table):
    return string_table

def get_running_image_containers(image_id, containers):
    """
    Get running Images or Containers
    """
    return [c for c in containers.values() if c.get("ImageID") == image_id and c.get("State") == "running"]


def get_docker_image_cpu(value_store, image_containers):
    """
    Get Image CPU
    """
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
    """
    Discover Docker Images
    """
    if section_docker_images is not None:
        for line in section_docker_images:
            yield Service(item=line[0])


def check_docker_images(item, section_docker_images, section_docker_containers):
    """
    Check Docker Images
    """
    value_store = get_value_store()

    for line in section_docker_images:

        if line[0] == item:
            image = {}

            for kv in line[1:]:
                (key, value) = kv.split("=", 1)
                image[key] = value

            image_containers = get_running_image_containers(image["ImageID"],
                                                            section_docker_containers)

            image["Running_containers"] = len(image_containers)
            image["Memory_used"] = sum(float(c["Memory_used"]) for c in image_containers)
            with suppress(GetRateError):
                image["CPU_pct"] = get_docker_image_cpu(value_store, image_containers)

            for var, value in image.items():
                if var == 'Stats':
                    yield Result(state=State.WARN, summary=f"Note: {value}")
                elif var == 'ImageID':
                    continue
                else:
                    yield Result(state=State.OK, summary=f"{var} = {float(value):.2f}")

                if var in ['CPU_pct']:
                    yield Metric(var, float(value), boundaries=(0, 100))

                if var in ['Diskspace_used', 'Memory_used', 'Running_containers']:
                    yield Metric(var, float(value))

agent_section_docker_images = AgentSection(
    name="docker_images",
    parse_function=parse_docker_images,
)

check_plugin_docker_images = CheckPlugin(
    name='docker_images',
    sections=['docker_images', 'docker_containers'],
    service_name="Docker Image %s",
    discovery_function=discover_docker_images,
    check_function=check_docker_images,
)
