#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    Metric,
    Result,
    Service,
    State,
)

def parse_wp_instances(string_table):
    if not string_table:
        return []
    return json.loads(section[0][0])

def discover_wp_instances(section):
    for wp_instance in section['instances']:
        if wp_instance["name"]:
            instance = wp_instance["name"]
            yield Service(item=instance)

def check_wp_instances(item, section):
    for wp_instance in section['instances']:
        if wp_instance["name"] == item:
            core_version = wp_instance["core_version"]
            core_new_version = wp_instance["core_new_version"]
            yield Metric(
                    "core_status",
                    wp_instance["core_status"]
            )
            if wp_instance["core_status"] == 0:
                yield Result(state=State.OK, summary = "Core Status is OK")
            elif wp_instance["core_status"] == 1:
                yield Result(
                    state=State.WARNING,
                    summary=(
                        f"Check Core Version for Updates: "
                        f"Installed Version: {core_version}, "
                        f"Available Version: {core_new_version}"
                    )
                )
            elif wp_instance["core_status"] == 2:
                yield Result(
                    state=State.CRITICAL,
                    summary=(
                        f"Update Core Version ASAP: "
                        f"Installed Version: {core_version}, "
                        f"Available Version: {core_new_version}"
                    )
                )
            return

agent_section_wordpress_instances = AgentSection(
    name="wordpress_instances", 
    parse_function=parse_wp_instances,
)

check_plugin_wordpress_instances = CheckPlugin(
    name = "wordpress_instances",
    service_name = "Wordpress Core %s",
    sections=["wordpress_instances"],
    discovery_function = discover_wp_instances,
    check_function = check_wp_instances,
)


