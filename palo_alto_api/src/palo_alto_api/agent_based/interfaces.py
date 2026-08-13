#!/usr/bin/env python3
"""
Palo Alto XML API - Interface check

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
import json
import time

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    GetRateError,
    Metric,
    Result,
    Service,
    State,
    check_levels,
    get_rate,
    get_value_store,
    render,
)


def parse_palo_alto_api_interfaces(string_table):
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


agent_section_palo_alto_api_interfaces = AgentSection(
    name="palo_alto_api_interfaces",
    parse_function=parse_palo_alto_api_interfaces,
)


def discover_palo_alto_api_interfaces(section):
    for item in section:
        if item != "_error":
            yield Service(item=item)


def _rate(value_store, key, now, value):
    try:
        return get_rate(value_store, key, now, value, raise_overflow=True)
    except GetRateError:
        return None


def check_palo_alto_api_interfaces(item, params, section):
    if item not in section:
        if "_error" in section:
            yield Result(state=State.CRIT, summary=f"Agent error: {section['_error']}")
        return

    data = section[item]
    state = data.get("state", "unknown")

    if state == "up":
        yield Result(state=State.OK, summary="State: up")
    else:
        yield Result(state=State(params["state_down"]), summary=f"State: {state}")

    if data.get("speed"):
        yield Result(state=State.OK, summary=f"Speed: {data['speed']}")

    value_store = get_value_store()
    now = time.time()

    for label, key, metric in (
        ("In", "rx_bytes", "if_in_octets"),
        ("Out", "tx_bytes", "if_out_octets"),
    ):
        counter = data.get(key)
        if counter is None:
            continue
        rate = _rate(value_store, f"{item}.{key}", now, counter)
        if rate is None:
            continue
        # render.networkbandwidth expects octets/s and renders bits/s itself.
        yield from check_levels(
            rate,
            metric_name=metric,
            label=f"{label} bandwidth",
            render_func=render.networkbandwidth,
        )

    for label, key, metric in (
        ("In errors", "rx_errors", "if_in_errors"),
        ("Out errors", "tx_errors", "if_out_errors"),
        ("In discards", "rx_discards", "if_in_discards"),
        ("Out discards", "tx_discards", "if_out_discards"),
    ):
        counter = data.get(key)
        if counter is None:
            continue
        rate = _rate(value_store, f"{item}.{key}", now, counter)
        if rate is None:
            continue
        yield from check_levels(
            rate,
            metric_name=metric,
            levels_upper=params.get("levels_errors", ("no_levels", None)),
            label=label,
            render_func=lambda v: f"{v:.2f}/s",
            notice_only=True,
        )


check_plugin_palo_alto_api_interfaces = CheckPlugin(
    name="palo_alto_api_interfaces",
    service_name="Palo Alto Interface %s",
    discovery_function=discover_palo_alto_api_interfaces,
    check_function=check_palo_alto_api_interfaces,
    check_ruleset_name="palo_alto_api_interfaces",
    check_default_parameters={"state_down": 2, "levels_errors": ("no_levels", None)},
)
