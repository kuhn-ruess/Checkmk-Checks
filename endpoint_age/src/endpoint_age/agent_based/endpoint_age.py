#!/usr/bin/env python3
"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de

Check plugin: endpoint freshness — verifies an HTTP endpoint serves
data that was updated within configurable thresholds. The age is
extracted by the special agent from a response header (e.g. ``Age``,
``Last-Modified``) or from a dotted JSON path.
"""
import json

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    Result,
    Service,
    State,
    check_levels,
    render,
)


def parse_endpoint_age(string_table):
    section = {}
    for row in string_table:
        if not row:
            continue
        try:
            entry = json.loads(row[0])
        except json.JSONDecodeError:
            continue
        name = entry.get("name")
        if not name:
            continue
        section[name] = entry
    return section


def discover_endpoint_age(section):
    for name in section:
        yield Service(item=name)


def check_endpoint_age(item, params, section):
    entry = section.get(item)
    if entry is None:
        return

    if not entry.get("ok"):
        error = entry.get("error") or "unknown error"
        http = entry.get("http_status")
        suffix = f" (HTTP {http})" if http else ""
        yield Result(
            state=State.CRIT,
            summary=f"Cannot determine freshness: {error}{suffix}",
        )
        if entry.get("url"):
            yield Result(state=State.OK, notice=f"URL: {entry['url']}")
        return

    age = entry.get("age_seconds")
    if age is None:
        yield Result(state=State.UNKNOWN, summary="No age value extracted")
        return

    levels = params.get("max_age")
    yield from check_levels(
        value=age,
        levels_upper=levels,
        metric_name="endpoint_age",
        render_func=render.timespan,
        label="Age",
    )
    if entry.get("detail"):
        yield Result(state=State.OK, notice=f"Source: {entry['detail']}")
    if entry.get("url"):
        yield Result(state=State.OK, notice=f"URL: {entry['url']}")


agent_section_endpoint_age = AgentSection(
    name="endpoint_age",
    parse_function=parse_endpoint_age,
)


check_plugin_endpoint_age = CheckPlugin(
    name="endpoint_age",
    service_name="Endpoint age %s",
    discovery_function=discover_endpoint_age,
    check_function=check_endpoint_age,
    check_ruleset_name="endpoint_age",
    check_default_parameters={
        "max_age": ("fixed", (15.0 * 60, 60.0 * 60)),
    },
)
