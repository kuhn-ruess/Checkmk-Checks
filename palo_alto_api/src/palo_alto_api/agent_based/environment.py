#!/usr/bin/env python3
"""
Palo Alto XML API - Environment (temperature, fans, power) check

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
import json

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    Metric,
    Result,
    Service,
    State,
    check_levels,
)


def parse_palo_alto_api_environment(string_table):
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


agent_section_palo_alto_api_environment = AgentSection(
    name="palo_alto_api_environment",
    parse_function=parse_palo_alto_api_environment,
)


def discover_palo_alto_api_environment(section):
    for item in section:
        if item != "_error":
            yield Service(item=item)


_METRIC_BY_KIND = {
    "temperature": "temp",
    "fan": "fan",
    "voltage": "voltage",
}


def check_palo_alto_api_environment(item, params, section):
    if item not in section:
        if "_error" in section:
            yield Result(state=State.CRIT, summary=f"Agent error: {section['_error']}")
        return

    data = section[item]

    if data.get("alarm"):
        yield Result(state=State.CRIT, summary="Alarm active")
    else:
        yield Result(state=State.OK, summary="No alarm")

    reading = data.get("reading")
    if reading is None:
        return

    kind = data.get("kind", "")
    unit = data.get("unit", "")
    levels = params.get("levels") if kind == "temperature" else None
    metric_name = _METRIC_BY_KIND.get(kind)

    if metric_name:
        yield from check_levels(
            reading,
            metric_name=metric_name,
            levels_upper=levels or ("no_levels", None),
            label=kind.capitalize() or "Reading",
            render_func=lambda v: f"{v:.1f}{unit}",
        )
    else:
        yield Result(state=State.OK, summary=f"Reading: {reading}{unit}")
        yield Metric("reading", reading)


check_plugin_palo_alto_api_environment = CheckPlugin(
    name="palo_alto_api_environment",
    service_name="Palo Alto Environment %s",
    discovery_function=discover_palo_alto_api_environment,
    check_function=check_palo_alto_api_environment,
    check_ruleset_name="palo_alto_api_environment",
    check_default_parameters={},
)
