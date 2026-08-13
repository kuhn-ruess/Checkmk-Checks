#!/usr/bin/env python3
"""
Palo Alto XML API - BGP peer check

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


def parse_palo_alto_api_bgp(string_table):
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


agent_section_palo_alto_api_bgp = AgentSection(
    name="palo_alto_api_bgp",
    parse_function=parse_palo_alto_api_bgp,
)


def discover_palo_alto_api_bgp(section):
    for item in section:
        if item != "_error":
            yield Service(item=item)


def check_palo_alto_api_bgp(item, params, section):
    if item not in section:
        if "_error" in section:
            yield Result(state=State.CRIT, summary=f"Agent error: {section['_error']}")
        return

    data = section[item]
    state = data.get("state", "unknown")

    if state == "established":
        yield Result(state=State.OK, summary="State: established")
    else:
        yield Result(state=State(params["state_not_established"]), summary=f"State: {state}")

    for label, key in (
        ("Peer", "peer_address"),
        ("Peer group", "peer_group"),
        ("Remote AS", "remote_as"),
    ):
        value = data.get(key)
        if value:
            yield Result(state=State.OK, notice=f"{label}: {value}")


check_plugin_palo_alto_api_bgp = CheckPlugin(
    name="palo_alto_api_bgp",
    service_name="Palo Alto BGP Peer %s",
    discovery_function=discover_palo_alto_api_bgp,
    check_function=check_palo_alto_api_bgp,
    check_ruleset_name="palo_alto_api_bgp",
    check_default_parameters={"state_not_established": 2},
)
