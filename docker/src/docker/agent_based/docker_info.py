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
    AgentSection,
)


def parse_docker_info(string_table):
    """
    Parser
    """
    if string_table[0][0] == 'service':
        return dict(string_table)

def discover_docker_info(section):
    """
    Discover Docker Info
    """
    yield Service()


def check_docker_info(section):
    """
    Check Docker Info
    """

    if section['service'] == "up":
        yield Result(state=State.OK, summary="service = up")
    else:
        yield Result(state=State.CRIT, summary=f"service = {service}")

    for key, value in section.items():
        if key in ("version", "images", "go_routines", "file_descriptors", "events_listeners"):
            yield Result(state=State.OK, summary=f"{key} = {value}")

            if isinstance(value, int):
                yield Metric(value, int(key))

agent_section_docker = AgentSection(
    name="docker_info",
    parse_function=parse_docker_info,
)

check_plugin_docker = CheckPlugin(
    name="docker_info",
    sections = ['docker_info'],
    service_name="Docker Info",
    discovery_function=discover_docker_info,
    check_function=check_docker_info,
)
