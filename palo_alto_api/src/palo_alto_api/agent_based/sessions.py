#!/usr/bin/env python3
"""
Palo Alto XML API - Sessions check

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


def parse_palo_alto_api_sessions(string_table):
    for line in string_table:
        try:
            data = json.loads(line[0])
        except (json.JSONDecodeError, IndexError):
            continue
        if "error" in data:
            return {"_error": data["error"]}
        if "item" in data:
            return {"data": data}
    return {}


agent_section_palo_alto_api_sessions = AgentSection(
    name="palo_alto_api_sessions",
    parse_function=parse_palo_alto_api_sessions,
)


def discover_palo_alto_api_sessions(section):
    if section.get("data"):
        yield Service()


def check_palo_alto_api_sessions(params, section):
    if "_error" in section:
        yield Result(state=State.CRIT, summary=f"Agent error: {section['_error']}")
        return
    data = section.get("data")
    if not data:
        return

    active = data.get("num_active")
    maximum = data.get("num_max")

    if active is not None and maximum:
        utilization = active / maximum * 100.0
        yield from check_levels(
            utilization,
            metric_name="session_utilization",
            levels_upper=params.get("levels_util", ("no_levels", None)),
            label="Utilization",
            render_func=lambda v: f"{v:.1f}%",
            boundaries=(0, 100),
        )

    if active is not None:
        yield Result(state=State.OK, summary=f"Active: {active}")
        yield Metric("num_active_sessions", active, boundaries=(0, maximum or None))

    for label, key, metric in (
        ("TCP", "num_tcp", "tcp_active_sessions"),
        ("UDP", "num_udp", "udp_active_sessions"),
        ("ICMP", "num_icmp", "icmp_active_sessions"),
    ):
        value = data.get(key)
        if value is not None:
            yield Result(state=State.OK, notice=f"{label}: {value}")
            yield Metric(metric, value)

    if data.get("cps") is not None:
        yield Metric("connections_rate", data["cps"])


check_plugin_palo_alto_api_sessions = CheckPlugin(
    name="palo_alto_api_sessions",
    service_name="Palo Alto Sessions",
    discovery_function=discover_palo_alto_api_sessions,
    check_function=check_palo_alto_api_sessions,
    check_ruleset_name="palo_alto_api_sessions",
    check_default_parameters={"levels_util": ("fixed", (80.0, 90.0))},
)
