#!/usr/bin/env python3

"""
Service Group States Check Plugin

One service per monitored service group. The service alarms when either a
single member, a configurable amount of members or all members of the group
are in a problem state and/or stale.

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
import json

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Metric,
    Result,
    Service,
    State,
    StringTable,
)


STATE_NAMES = {0: "OK", 1: "WARN", 2: "CRIT", 3: "UNKNOWN"}

PROBLEM_STATES = {
    "warn": 1,
    "crit": 2,
    "unknown": 3,
}

MAX_DETAIL_LINES = 25

DEFAULT_PARAMETERS = {
    "problem": {
        "mode": ("any", None),
        "states": ["crit", "unknown"],
        "result": 2,
    },
    "stale": {
        "mode": ("any", None),
        "result": 1,
    },
    "ignore_acknowledged": False,
    "ignore_downtime": True,
    "only_hard_states": True,
    "empty_group": 1,
}


def parse_servicegroup_states(string_table: StringTable) -> dict:
    """
    One json object per line, keyed by the service group name
    """
    parsed = {}
    for line in string_table:
        if not line or not line[0]:
            continue
        try:
            entry = json.loads(line[0])
        except json.JSONDecodeError:
            continue
        name = entry.get("name")
        if name:
            parsed[name] = entry
    return parsed


agent_section_servicegroup_states = AgentSection(
    name="servicegroup_states",
    parse_function=parse_servicegroup_states,
)


def discover_servicegroup_states(section: dict) -> DiscoveryResult:
    """
    One service per service group
    """
    for name in section:
        yield Service(item=name)


def _is_relevant(service: dict, params: dict) -> bool:
    """
    Honour the acknowledgement and downtime filters
    """
    if params.get("ignore_acknowledged") and service.get("ack"):
        return False
    if params.get("ignore_downtime") and service.get("downtime"):
        return False
    return True


def _triggered(mode: tuple, count: int, total: int) -> bool:
    """
    Evaluate the configured trigger mode
    """
    kind, value = mode
    if count == 0:
        return False
    if kind == "all":
        return total > 0 and count >= total
    if kind == "at_least":
        return count >= value
    if kind == "percent":
        return total > 0 and (count / total * 100.0) >= value
    return True


def _mode_text(mode: tuple) -> str:
    """
    Human readable trigger description
    """
    kind, value = mode
    if kind == "all":
        return "all members"
    if kind == "at_least":
        return f"at least {value}"
    if kind == "percent":
        return f"at least {value}% of the members"
    return "at least one member"


def _is_are(count: int) -> str:
    """
    Verb form for the affected count
    """
    return "is" if count == 1 else "are"


def _plural(count: int) -> str:
    """
    Singular or plural for the member count
    """
    return "service" if count == 1 else "services"


def _details(headline: str, services: list) -> str:
    """
    Build the long output for the affected services
    """
    lines = [headline]
    for service in services[:MAX_DETAIL_LINES]:
        site = f"[{service['site']}] " if service.get("site") else ""
        state = STATE_NAMES.get(service.get("state"), "UNKNOWN")
        flags = []
        if service.get("stale"):
            flags.append("stale")
        if service.get("pending"):
            flags.append("pending")
        if service.get("ack"):
            flags.append("acknowledged")
        if service.get("downtime"):
            flags.append("downtime")
        if not service.get("hard"):
            flags.append("soft")
        suffix = f" ({', '.join(flags)})" if flags else ""
        output = service.get("output", "")
        output = f" - {output}" if output else ""
        lines.append(f"{site}{service['host']} / {service['service']}: {state}{suffix}{output}")
    if len(services) > MAX_DETAIL_LINES:
        lines.append(f"... and {len(services) - MAX_DETAIL_LINES} more")
    return "\n".join(lines)


def check_servicegroup_states(item: str, params: dict, section: dict) -> CheckResult:
    """
    Evaluate one service group
    """
    group = section.get(item)
    if group is None:
        return

    total = group.get("total", 0)
    counts = group.get("counts", {})
    services = group.get("services", [])

    alias = group.get("alias") or ""
    headline = f"{total} {_plural(total)}"
    if alias and alias != item:
        headline = f"{alias}: {headline}"
    yield Result(
        state=State.OK,
        summary=headline,
        details=(
            f"OK: {counts.get('ok', 0)}, WARN: {counts.get('warn', 0)}, "
            f"CRIT: {counts.get('crit', 0)}, UNKNOWN: {counts.get('unknown', 0)}, "
            f"PENDING: {counts.get('pending', 0)}"
        ),
    )

    yield Metric("servicegroup_services", total)

    if not total:
        yield Result(
            state=State(params.get("empty_group", 1)),
            summary="Service group is empty",
        )
        return

    candidates = [service for service in services if _is_relevant(service, params)]
    only_hard = params.get("only_hard_states", True)

    problem_config = params.get("problem")
    problem_services = []
    if problem_config:
        wanted = {PROBLEM_STATES[name] for name in problem_config.get("states", [])}
        problem_services = [
            service
            for service in candidates
            if service.get("state") in wanted
            and not service.get("pending")
            and (service.get("hard") or not only_hard)
        ]

    stale_config = params.get("stale")
    stale_services = []
    if stale_config:
        stale_services = [service for service in candidates if service.get("stale")]

    yield Metric("servicegroup_services_problem", len(problem_services))
    yield Metric("servicegroup_services_stale", len(stale_services))

    if problem_config:
        mode = tuple(problem_config.get("mode", ("any", None)))
        count = len(problem_services)
        state_names = ", ".join(
            STATE_NAMES[PROBLEM_STATES[name]] for name in problem_config.get("states", [])
        )
        if _triggered(mode, count, total):
            yield Result(
                state=State(problem_config.get("result", 2)),
                summary=f"{count} of {total} {_plural(total)} in state {state_names}",
                details=_details(
                    f"Services in state {state_names} ({_mode_text(mode)} triggers):",
                    problem_services,
                ),
            )
        elif count:
            yield Result(
                state=State.OK,
                notice=f"{count} of {total} {_plural(total)} in state {state_names} "
                       f"(below trigger: {_mode_text(mode)})",
                details=_details(f"Services in state {state_names}:", problem_services),
            )

    if stale_config:
        mode = tuple(stale_config.get("mode", ("any", None)))
        count = len(stale_services)
        if _triggered(mode, count, total):
            yield Result(
                state=State(stale_config.get("result", 1)),
                summary=f"{count} of {total} {_plural(total)} {_is_are(count)} stale",
                details=_details(f"Stale services ({_mode_text(mode)} triggers):", stale_services),
            )
        elif count:
            yield Result(
                state=State.OK,
                notice=f"{count} of {total} {_plural(total)} {_is_are(count)} stale "
                       f"(below trigger: {_mode_text(mode)})",
                details=_details("Stale services:", stale_services),
            )


check_plugin_servicegroup_states = CheckPlugin(
    name="servicegroup_states",
    service_name="Service Group %s",
    discovery_function=discover_servicegroup_states,
    check_function=check_servicegroup_states,
    check_default_parameters=DEFAULT_PARAMETERS,
    check_ruleset_name="servicegroup_states",
)
