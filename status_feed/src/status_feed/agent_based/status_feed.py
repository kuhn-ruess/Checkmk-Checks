#!/usr/bin/env python3
"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de

Check plugin: status RSS/Atom feed health.

The special agent emits one JSON object per configured feed. The check
discovers one service per feed and reports:

- CRIT when the feed could not be fetched / parsed (item-less HTML page,
  HTTP error, timeout). This catches the "feed liefert keine Daten" case.
- OK when the feed is valid but contains no items (AWS-style per-service
  feeds publish an entry only while an incident is in flight).
- In incident mode (Statuspage-style history feeds, e.g. Scrivito) the
  state is derived from the lifecycle of the most recent entry: a resolved
  entry is OK regardless of age, an active one alerts.
- Otherwise WARN/CRIT when the most recent entry is younger than a
  configurable age (a fresh event means an incident is in flight).
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
    render,
)


def parse_status_feed(string_table):
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


def discover_status_feed(section):
    for name in section:
        yield Service(item=name)


def _age_state(params, age_seconds):
    crit = params.get("event_age_crit")
    warn = params.get("event_age_warn")
    if crit is not None and age_seconds <= crit:
        return State.CRIT
    if warn is not None and age_seconds <= warn:
        return State.WARN
    return State.OK


def check_status_feed(item, params, section):
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
    state_label = entry.get("latest_state")

    if items == 0:
        yield Result(
            state=State.OK,
            summary="Feed valid, no incidents reported",
        )
        return

    incident_mode = params.get("incident_mode", "age") == "incident"

    if incident_mode and state_label == "resolved":
        # History feeds keep resolved incidents forever; a resolved latest
        # entry means there is nothing going on right now.
        state = State.OK
        summary = "Latest incident resolved"
        if title:
            summary += f" — {title}"
    elif incident_mode and state_label == "active":
        state = State(params.get("active_incident_state", State.CRIT.value))
        summary = "Active incident"
        if title:
            summary += f" — {title}"
    else:
        state = _age_state(params, age) if age is not None else State.OK
        age_text = render.timespan(age) if age is not None else "unknown age"
        summary = f"Latest event {age_text} ago"
        if title:
            summary += f" — {title}"

    yield Result(state=state, summary=summary)
    yield Result(state=State.OK, notice=f"{items} entries in feed")
    if state_label:
        yield Result(state=State.OK, notice=f"Latest entry state: {state_label}")
    if published:
        yield Result(state=State.OK, notice=f"Published: {published}")
    if entry.get("latest_summary"):
        yield Result(state=State.OK, notice=entry["latest_summary"])


agent_section_status_feed = AgentSection(
    name="status_feed",
    parse_function=parse_status_feed,
)


check_plugin_status_feed = CheckPlugin(
    name="status_feed",
    service_name="Status feed %s",
    discovery_function=discover_status_feed,
    check_function=check_status_feed,
    check_ruleset_name="status_feed",
    check_default_parameters={
        "event_age_warn": 7.0 * 24 * 3600,
        "event_age_crit": 24.0 * 3600,
        "incident_mode": "age",
        "active_incident_state": State.CRIT.value,
    },
)
