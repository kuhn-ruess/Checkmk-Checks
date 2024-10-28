#!/usr/bin/env python3
"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

# Plugin output:
#
# <<<docker_info:sep(58)>>>
# service:up
# images:3
# go_routines:34
# file_descriptors:29
# events_listeners:0

from cmk.agent_based.v2 import (
    CheckPlugin,
    Metric,
    Result,
    Service,
    State,
)

def discover_docker_info(section):
    """
    Discover Docker Info
    """
    for line in section:
        if line[0] == "service":
            yield Service()
            break


def check_docker_info(section):
    """
    Check Docker Info
    """
    for line in section:
        if  line[0] == "service":
            service = line[1]

            if service == "up":
                yield Result(state=State.OK, summary="service = up")
            else:
                yield Result(state=State.CRIT, summary=f"service = {service}")

        for var in ("version", "images", "go_routines", "file_descriptors", "events_listeners"):
            if line[0] == var:
                yield Result(state=State.OK, summary=f"{line[0]} = {line[1]}")

                if isinstance(line[1], int):
                    yield Metric(line[0], int(line[1]))


docker_info_plugin = CheckPlugin(
    name="docker_info",
    service_name="Docker Info",
    discovery_function=discover_docker_info,
    check_function=check_docker_info,
)
