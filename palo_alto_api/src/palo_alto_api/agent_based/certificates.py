#!/usr/bin/env python3
"""
Palo Alto XML API - Certificate expiry check

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


def parse_palo_alto_api_certificates(string_table):
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


agent_section_palo_alto_api_certificates = AgentSection(
    name="palo_alto_api_certificates",
    parse_function=parse_palo_alto_api_certificates,
)


def discover_palo_alto_api_certificates(section):
    for item in section:
        if item != "_error":
            yield Service(item=item)


def check_palo_alto_api_certificates(item, params, section):
    if item not in section:
        if "_error" in section:
            yield Result(state=State.CRIT, summary=f"Agent error: {section['_error']}")
        return

    data = section[item]
    yield from check_levels(
        data["days_remaining"],
        metric_name="certificate_validity_days",
        levels_lower=("fixed", (params["warn_days"], params["crit_days"])),
        label="Days remaining",
        render_func=lambda v: f"{int(v)} days",
    )
    yield Result(
        state=State.OK,
        notice=f"Subject: {data.get('subject', 'unknown')}, Expires: {data.get('not_after', 'unknown')}",
    )


check_plugin_palo_alto_api_certificates = CheckPlugin(
    name="palo_alto_api_certificates",
    service_name="Palo Alto Certificate %s",
    discovery_function=discover_palo_alto_api_certificates,
    check_function=check_palo_alto_api_certificates,
    check_ruleset_name="palo_alto_api_certificates",
    check_default_parameters={"warn_days": 30, "crit_days": 14},
)
