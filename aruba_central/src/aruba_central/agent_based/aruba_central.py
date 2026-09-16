#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

import json

from cmk.agent_based.v2 import (
    AgentSection,
    check_levels,
    CheckPlugin,
    render,
    Result,
    Service,
    State,
)


def parse_aruba_central(string_table):
    """Parse the counts and the API rate limit of the cencli call."""
    if not string_table:
        return None

    try:
        return json.loads("".join(line[0] for line in string_table))
    except ValueError:
        return None


def discover_aruba_central(section):
    """Discovery"""
    yield Service()


def check_aruba_central(params, section):
    """Check"""
    if error := section.get("error"):
        yield Result(state=State.CRIT, summary=f"Error: {error}")

    if (total := section.get("aps_total")) is not None:
        yield Result(state=State.OK, summary=f"Access points: {total}")

    if (down := section.get("aps_down")) is not None:
        yield from check_levels(
            down,
            levels_upper=params["levels_down"],
            metric_name="aruba_aps_down",
            label="Down",
            render_func=lambda v: f"{int(v)}",
        )

    if (up := section.get("aps_up")) is not None:
        yield from check_levels(
            up,
            metric_name="aruba_aps_up",
            label="Up",
            render_func=lambda v: f"{int(v)}",
            notice_only=True,
        )

    if (clients := section.get("clients")) is not None:
        yield from check_levels(
            clients,
            metric_name="aruba_clients",
            label="Clients",
            render_func=lambda v: f"{int(v)}",
        )

    remaining = section.get("rate_remaining")
    limit = section.get("rate_limit")
    if remaining is not None:
        yield from check_levels(
            remaining,
            levels_lower=params["levels_rate_remaining"],
            metric_name="aruba_api_rate_remaining",
            label="API calls left",
            render_func=lambda v: f"{int(v)}" + (f" of {limit}" if limit else ""),
            notice_only=True,
        )
        if limit:
            yield Result(
                state=State.OK,
                notice=f"API rate limit used: {render.percent(100.0 * (limit - remaining) / limit)}",
            )


agent_section_aruba_central = AgentSection(
    name = "aruba_central",
    parse_function = parse_aruba_central,
)

check_plugin_aruba_central = CheckPlugin(
    name = "aruba_central",
    service_name = "Aruba Central",
    discovery_function = discover_aruba_central,
    check_function = check_aruba_central,
    check_default_parameters = {
        "levels_down": ("fixed", (1, 10)),
        "levels_rate_remaining": ("fixed", (1000, 100)),
    },
    check_ruleset_name = "aruba_central",
)
