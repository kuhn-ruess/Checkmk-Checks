#!/usr/bin/env python3
"""
Palo Alto XML API - IKE gateway check

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


def parse_palo_alto_api_ike(string_table):
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


agent_section_palo_alto_api_ike = AgentSection(
    name="palo_alto_api_ike",
    parse_function=parse_palo_alto_api_ike,
)


def discover_palo_alto_api_ike(section):
    for item in section:
        if item != "_error":
            yield Service(item=item)


def check_palo_alto_api_ike(item, params, section):
    if item not in section:
        if "_error" in section:
            yield Result(state=State.CRIT, summary=f"Agent error: {section['_error']}")
        return

    data = section[item]
    state = data.get("state", "unknown")

    # An established IKE SA is healthy; anything else (e.g. no SA present) is
    # reported with the configured, by default less severe, state.
    if state in ("established", "active", "up"):
        yield Result(state=State.OK, summary=f"State: {state}")
    else:
        yield Result(
            state=State(params["state_not_established"]),
            summary=f"State: {state}",
        )

    peer = data.get("peerip")
    if peer:
        yield Result(state=State.OK, summary=f"Peer: {peer}")

    cipher = data.get("cipher")
    if cipher:
        yield Result(state=State.OK, summary=f"Cipher: {cipher}")

    details = []
    for label, key in (("Local IP", "localip"), ("Role", "role")):
        value = data.get(key)
        if value:
            details.append(f"{label}: {value}")
    if details:
        yield Result(state=State.OK, notice="\n".join(details))


check_plugin_palo_alto_api_ike = CheckPlugin(
    name="palo_alto_api_ike",
    service_name="Palo Alto IKE Gateway %s",
    discovery_function=discover_palo_alto_api_ike,
    check_function=check_palo_alto_api_ike,
    check_ruleset_name="palo_alto_api_ike",
    check_default_parameters={"state_not_established": 1},
)
