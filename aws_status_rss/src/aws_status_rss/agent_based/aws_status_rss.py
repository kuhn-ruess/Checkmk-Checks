#!/usr/bin/env python3
"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de

Check plugin: AWS service status RSS feed health.

The special agent emits one JSON object per configured feed. The check
discovers one service per feed and reports:

- CRIT when the feed could not be fetched / parsed (item-less HTML page,
  HTTP error, timeout). This catches the "RSS Antwort liefert keine Daten"
  case from the original ticket.
- WARN/CRIT when the most recent feed entry is younger than a configurable
  age (an AWS service that just emitted a status event has an incident in
  flight).
- OK otherwise — including the common case of a feed without any items,
  which means AWS reports no incidents for that service.
"""
import json

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Result,
    Service,
    State,
    check_levels,
    render,
)


def parse_aws_status_rss(string_table):
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


def discover_aws_status_rss(section):
    for name in section:
        yield Service(item=name)


def _event_state(params, age_seconds):
    crit = params.get("event_age_crit")
    warn = params.get("event_age_warn")
    if crit is not None and age_seconds <= crit:
        return State.CRIT
    if warn is not None and age_seconds <= warn:
        return State.WARN
    return State.OK


def check_aws_status_rss(item, params, section):
    entry = section.get(item)
    if entry is None:
        return

    if not entry.get("ok"):
        error = entry.get("error") or "feed unreachable"
        http = entry.get("http_status")
        suffix = f" (HTTP {http})" if http else ""
        yield Result(
            state=State.CRIT,
            summary=f"Feed not delivering data: {error}{suffix}",
        )
        if entry.get("url"):
            yield Result(state=State.OK, notice=f"URL: {entry['url']}")
        return

    items = entry.get("items", 0)
    age = entry.get("latest_age_seconds")
    title = entry.get("latest_title")
    published = entry.get("latest_published")

    if items == 0:
        yield Result(
            state=State.OK,
            summary="Feed valid, no incidents reported",
        )
        return

    state = _event_state(params, age) if age is not None else State.OK
    age_text = render.timespan(age) if age is not None else "unknown age"
    summary_bits = [f"Latest event {age_text} ago"]
    if title:
        summary_bits.append(title)
    yield Result(state=state, summary=" — ".join(summary_bits))
    yield Result(state=State.OK, notice=f"{items} entries in feed")
    if published:
        yield Result(state=State.OK, notice=f"Published: {published}")
    if entry.get("latest_summary"):
        yield Result(state=State.OK, notice=entry["latest_summary"])


agent_section_aws_status_rss = AgentSection(
    name="aws_status_rss",
    parse_function=parse_aws_status_rss,
)


check_plugin_aws_status_rss = CheckPlugin(
    name="aws_status_rss",
    service_name="AWS Status %s",
    discovery_function=discover_aws_status_rss,
    check_function=check_aws_status_rss,
    check_ruleset_name="aws_status_rss",
    check_default_parameters={
        "event_age_warn": 7.0 * 24 * 3600,
        "event_age_crit": 24.0 * 3600,
    },
)
