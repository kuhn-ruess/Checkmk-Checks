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
    # Remember the neighbor state at discovery as the target state; the check
    # then only alerts when the state changes (e.g. full/2way is fine either way).
    for item, data in section.items():
        if item == "_error":
            continue
        yield Service(item=item, parameters={"discovered_state": data.get("state", "unknown")})


# A neighbor is healthy in "full" (adjacency formed) or "2way" (DR/BDR).
_HEALTHY_STATES = {"full", "2way"}


def check_palo_alto_api_ospf(item, params, section):
    if item not in section:
        if "_error" in section:
            yield Result(state=State.CRIT, summary=f"Agent error: {section['_error']}")
        return

    data = section[item]
    state = data.get("state", "unknown")
    target = params.get("discovered_state")

    if target is None:
        # Service discovered before target-state tracking: fall back to fixed states.
        result_state = State.OK if state in _HEALTHY_STATES else State(params["state_changed"])
        yield Result(state=result_state, summary=f"State: {state}")
    elif state == target:
        yield Result(state=State.OK, summary=f"State: {state} (unchanged since discovery)")
    else:
        yield Result(
            state=State(params["state_changed"]),
            summary=f"State: {state} (changed from {target} since discovery)",
        )

    if data.get("area"):
        yield Result(state=State.OK, notice=f"Area: {data['area']}")


check_plugin_palo_alto_api_ospf = CheckPlugin(
    name="palo_alto_api_ospf",
    service_name="Palo Alto %s",
    discovery_function=discover_palo_alto_api_ospf,
    check_function=check_palo_alto_api_ospf,
    check_ruleset_name="palo_alto_api_ospf",
    check_default_parameters={"state_changed": 2},
)
