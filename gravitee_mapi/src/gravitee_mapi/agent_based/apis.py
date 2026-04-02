#!/usr/bin/env python3

"""
Gravitee MAPI Check Plugins

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


def parse_gravitee_mapi(string_table):
    """
    Parse agent output into dict keyed by API name.
    Each line is a JSON object with id, name, stats, errors, health.
    """
    parsed = {}
    for line in string_table:
        try:
            data = json.loads(line[0])
            parsed[data["name"]] = data
        except (json.JSONDecodeError, KeyError):
            continue
    return parsed


agent_section_gravitee_mapi = AgentSection(
    name="gravitee_mapi",
    parse_function=parse_gravitee_mapi,
)


# ---------------------------------------------------------------------------
# Check: Response time stats
# ---------------------------------------------------------------------------

def discover_gravitee_mapi_stats(section):
    for api_name in section:
        yield Service(item=api_name)


def check_gravitee_mapi_stats(item, section):
    data = section.get(item)
    if not data:
        yield Result(state=State.UNKNOWN, summary=f"No data for API {item}")
        return

    stats = data.get("stats", {})

    if "error" in stats:
        yield Result(state=State.UNKNOWN, summary=f"Stats error: {stats['error']}")
        return

    avg = stats.get("avg")
    minimum = stats.get("min")
    maximum = stats.get("max")
    count = stats.get("count", 0)

    summary_parts = [f"Requests: {count}"]

    if avg is not None:
        yield from check_levels(
            avg,
            metric_name="response_time",
            label="Avg response time",
            render_func=lambda v: f"{v:.1f} ms",
        )
    else:
        summary_parts.append("No response time data")

    if minimum is not None:
        yield Metric("response_time_min", minimum)
        summary_parts.append(f"Min: {minimum:.1f} ms")

    if maximum is not None:
        yield Metric("response_time_max", maximum)
        summary_parts.append(f"Max: {maximum:.1f} ms")

    yield Result(state=State.OK, summary=", ".join(summary_parts))


check_plugin_gravitee_mapi_stats = CheckPlugin(
    name="gravitee_mapi_stats",
    sections=["gravitee_mapi"],
    service_name="API %s Response Time",
    discovery_function=discover_gravitee_mapi_stats,
    check_function=check_gravitee_mapi_stats,
)


# ---------------------------------------------------------------------------
# Check: Response status ranges (error rates)
# ---------------------------------------------------------------------------

def _parse_ranges(ranges_data):
    """
    Flatten the ranges dict from Gravitee into named counters.
    Keys look like '100.0-200.0', '200.0-300.0', etc.
    Returns (2xx, 4xx, 5xx, total).
    """
    count_2xx = 0
    count_4xx = 0
    count_5xx = 0
    count_other = 0

    for key, value in (ranges_data or {}).items():
        try:
            lower = float(key.split("-")[0])
        except (ValueError, IndexError):
            continue
        if 200 <= lower < 300:
            count_2xx += int(value or 0)
        elif 400 <= lower < 500:
            count_4xx += int(value or 0)
        elif 500 <= lower < 600:
            count_5xx += int(value or 0)
        else:
            count_other += int(value or 0)

    total = count_2xx + count_4xx + count_5xx + count_other
    return count_2xx, count_4xx, count_5xx, total


def discover_gravitee_mapi_errors(section):
    for api_name in section:
        yield Service(item=api_name)


def check_gravitee_mapi_errors(item, section):
    data = section.get(item)
    if not data:
        yield Result(state=State.UNKNOWN, summary=f"No data for API {item}")
        return

    errors = data.get("errors", {})

    if "error" in errors:
        yield Result(state=State.UNKNOWN, summary=f"Errors data unavailable: {errors['error']}")
        return

    ranges = errors.get("ranges", errors)
    count_2xx, count_4xx, count_5xx, total = _parse_ranges(ranges)

    yield Metric("requests_2xx", count_2xx)
    yield Metric("requests_4xx", count_4xx)
    yield Metric("requests_5xx", count_5xx)
    yield Metric("requests_total", total)

    state = State.OK
    details = [f"Total: {total}", f"2xx: {count_2xx}"]

    if total > 0:
        rate_4xx = count_4xx / total * 100
        rate_5xx = count_5xx / total * 100
        details.append(f"4xx: {count_4xx} ({rate_4xx:.1f}%)")
        details.append(f"5xx: {count_5xx} ({rate_5xx:.1f}%)")
        if count_5xx > 0:
            state = State.CRIT
        elif count_4xx > 0:
            state = State.WARN
    else:
        details.append("4xx: 0")
        details.append("5xx: 0")

    yield Result(state=state, summary=", ".join(details))


check_plugin_gravitee_mapi_errors = CheckPlugin(
    name="gravitee_mapi_errors",
    sections=["gravitee_mapi"],
    service_name="API %s Error Rates",
    discovery_function=discover_gravitee_mapi_errors,
    check_function=check_gravitee_mapi_errors,
)


# ---------------------------------------------------------------------------
# Check: Health / Availability
# ---------------------------------------------------------------------------

def discover_gravitee_mapi_health(section):
    for api_name in section:
        yield Service(item=api_name)


def check_gravitee_mapi_health(item, section):
    data = section.get(item)
    if not data:
        yield Result(state=State.UNKNOWN, summary=f"No data for API {item}")
        return

    health = data.get("health", {})

    if "error" in health:
        yield Result(state=State.UNKNOWN, summary=f"Health unavailable: {health['error']}")
        return

    # Gravitee health/availability returns a percentage or availability object
    availability = health.get("availability", health.get("global"))

    if availability is None:
        yield Result(state=State.UNKNOWN, summary="No health data returned")
        return

    try:
        pct = float(availability) * 100 if float(availability) <= 1 else float(availability)
    except (TypeError, ValueError):
        yield Result(state=State.UNKNOWN, summary=f"Unexpected health value: {availability}")
        return

    yield Metric("availability", pct)

    state = State.OK if pct >= 99.0 else (State.WARN if pct >= 95.0 else State.CRIT)
    yield Result(state=state, summary=f"Availability: {pct:.1f}%")


check_plugin_gravitee_mapi_health = CheckPlugin(
    name="gravitee_mapi_health",
    sections=["gravitee_mapi"],
    service_name="API %s Health",
    discovery_function=discover_gravitee_mapi_health,
    check_function=check_gravitee_mapi_health,
)
