#!/usr/bin/env python3
"""
Palo Alto XML API - License expiry check

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


def parse_palo_alto_api_licenses(string_table):
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


agent_section_palo_alto_api_licenses = AgentSection(
    name="palo_alto_api_licenses",
    parse_function=parse_palo_alto_api_licenses,
)


def discover_palo_alto_api_licenses(section):
    for item in section:
        if item != "_error":
            yield Service(item=item)


def check_palo_alto_api_licenses(item, params, section):
    if item not in section:
        if "_error" in section:
            yield Result(state=State.CRIT, summary=f"Agent error: {section['_error']}")
        return

    data = section[item]

    if data.get("expired"):
        yield Result(state=State.CRIT, summary="License has expired")

    days = data.get("days_remaining")
    if days is None:
        if not data.get("expired"):
            yield Result(state=State.OK, summary="Does not expire")
    else:
        yield from check_levels(
            days,
            metric_name="license_validity_days",
            levels_lower=("fixed", (params["warn_days"], params["crit_days"])),
            label="Days remaining",
            render_func=lambda v: f"{int(v)} days",
        )

    if data.get("description"):
        yield Result(state=State.OK, notice=f"Description: {data['description']}")


check_plugin_palo_alto_api_licenses = CheckPlugin(
    name="palo_alto_api_licenses",
    service_name="Palo Alto License %s",
    discovery_function=discover_palo_alto_api_licenses,
    check_function=check_palo_alto_api_licenses,
    check_ruleset_name="palo_alto_api_licenses",
    check_default_parameters={"warn_days": 30, "crit_days": 14},
)
