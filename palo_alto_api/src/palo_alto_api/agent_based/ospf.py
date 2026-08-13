#!/usr/bin/env python3
"""
Palo Alto XML API - OSPF / OSPFv3 neighbor check

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
)


def parse_palo_alto_api_ospf(string_table):
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


agent_section_palo_alto_api_ospf = AgentSection(
    name="palo_alto_api_ospf",
    parse_function=parse_palo_alto_api_ospf,
)


def discover_palo_alto_api_ospf(section):
    for item in section:
        if item != "_error":
            yield Service(item=item)


# A neighbor is healthy in "full" (adjacency formed) or "2way" (DR/BDR).
_HEALTHY_STATES = {"full", "2way"}


def check_palo_alto_api_ospf(item, params, section):
    if item not in section:
        if "_error" in section:
            yield Result(state=State.CRIT, summary=f"Agent error: {section['_error']}")
        return

    data = section[item]
    state = data.get("state", "unknown")

    if state in _HEALTHY_STATES:
        yield Result(state=State.OK, summary=f"State: {state}")
    else:
        yield Result(state=State(params["state_not_full"]), summary=f"State: {state}")

    if data.get("area"):
        yield Result(state=State.OK, notice=f"Area: {data['area']}")


check_plugin_palo_alto_api_ospf = CheckPlugin(
    name="palo_alto_api_ospf",
    service_name="Palo Alto %s",
    discovery_function=discover_palo_alto_api_ospf,
    check_function=check_palo_alto_api_ospf,
    check_ruleset_name="palo_alto_api_ospf",
    check_default_parameters={"state_not_full": 2},
)
