#!/usr/bin/env python3
"""
Palo Alto XML API - CPU utilization check

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
import json

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    Result,
    Service,
    State,
    check_levels,
)


def parse_palo_alto_api_cpu(string_table):
    parsed = {}
    for line in string_table:
        try:
            data = json.loads(line[0])
        except (json.JSONDecodeError, IndexError):
            continue
        if "error" in data:
            parsed["_error"] = data["error"]
        elif "item" in data:
            parsed[data["item"]] = data
    return parsed


agent_section_palo_alto_api_cpu = AgentSection(
    name="palo_alto_api_cpu",
    parse_function=parse_palo_alto_api_cpu,
)


def discover_palo_alto_api_cpu(section):
    for item in section:
        if item != "_error":
            yield Service(item=item)


def check_palo_alto_api_cpu(item, params, section):
    if item not in section:
        if "_error" in section:
            yield Result(state=State.CRIT, summary=f"Agent error: {section['_error']}")
        return

    yield from check_levels(
        section[item]["load"],
        metric_name="util",
        levels_upper=params.get("levels", ("no_levels", None)),
        label="Utilization",
        render_func=lambda v: f"{v:.1f}%",
        boundaries=(0, 100),
    )


check_plugin_palo_alto_api_cpu = CheckPlugin(
    name="palo_alto_api_cpu",
    service_name="Palo Alto CPU %s",
    discovery_function=discover_palo_alto_api_cpu,
    check_function=check_palo_alto_api_cpu,
    check_ruleset_name="palo_alto_api_cpu",
    check_default_parameters={"levels": ("fixed", (80.0, 90.0))},
)
