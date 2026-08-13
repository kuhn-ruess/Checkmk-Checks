#!/usr/bin/env python3
"""
Palo Alto XML API - High availability check

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


def parse_palo_alto_api_ha(string_table):
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


agent_section_palo_alto_api_ha = AgentSection(
    name="palo_alto_api_ha",
    parse_function=parse_palo_alto_api_ha,
)


def discover_palo_alto_api_ha(section):
    for item in section:
        if item != "_error":
            yield Service(item=item)


# HA states considered healthy; everything else uses the configured state.
_HEALTHY_STATES = {"active", "passive", "active-primary", "active-secondary"}


def check_palo_alto_api_ha(item, params, section):
    if item not in section:
        if "_error" in section:
            yield Result(state=State.CRIT, summary=f"Agent error: {section['_error']}")
        return

    data = section[item]

    # HA link item
    if "conn_status" in data:
        conn = data["conn_status"].lower()
        state = State.OK if conn == "up" else State(params["state_link_down"])
        yield Result(state=state, summary=f"Connection: {data['conn_status']}")
        return

    # HA summary item
    if data.get("enabled", "").lower() in ("no", ""):
        yield Result(state=State.OK, summary="HA is not enabled")
        return

    local_state = data.get("local_state", "unknown")
    if local_state in _HEALTHY_STATES:
        yield Result(state=State.OK, summary=f"Local state: {local_state}")
    else:
        yield Result(state=State(params["state_local_unhealthy"]),
                     summary=f"Local state: {local_state}")

    if data.get("local_state_reason"):
        yield Result(state=State.OK, notice=f"State reason: {data['local_state_reason']}")

    if data.get("peer_state"):
        yield Result(state=State.OK, summary=f"Peer state: {data['peer_state']}")

    if data.get("mode"):
        yield Result(state=State.OK, summary=f"Mode: {data['mode']}")

    sync = data.get("running_sync")
    if sync:
        state = State.OK if sync.lower() == "synchronized" else State(params["state_not_synced"])
        yield Result(state=state, summary=f"Config sync: {sync}")


check_plugin_palo_alto_api_ha = CheckPlugin(
    name="palo_alto_api_ha",
    service_name="Palo Alto %s",
    discovery_function=discover_palo_alto_api_ha,
    check_function=check_palo_alto_api_ha,
    check_ruleset_name="palo_alto_api_ha",
    check_default_parameters={
        "state_local_unhealthy": 2,
        "state_not_synced": 1,
        "state_link_down": 2,
    },
)
