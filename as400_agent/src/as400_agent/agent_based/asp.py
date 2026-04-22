#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    Service,
    Result,
    Metric,
    State,
    check_levels,
    render,
)


MB = 1_000_000


def parse_function(string_table):
    """
    Parse agent output grouped by ASP number.
    """
    parsed = {}
    current = None
    for line in string_table:
        if not line:
            continue
        first = line[0]
        if first.startswith('[[['):
            current = first[3:-3]
            parsed.setdefault(current, {})
            continue
        if current is None:
            continue
        key = first
        value = " ".join(line[1:]) if len(line) > 1 else ""
        parsed[current][key] = value
    return parsed


def discover_service(section):
    for item in section:
        yield Service(item=item)


def _to_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def check_service(item, params, section):
    data = section.get(item)
    if not data:
        return

    total_mb = _to_int(data.get('TOTAL_CAPACITY'))
    avail_mb = _to_int(data.get('TOTAL_CAPACITY_AVAILABLE'))

    if total_mb is None or avail_mb is None or total_mb <= 0:
        yield Result(state=State.UNKNOWN, summary="ASP capacity not reported")
        return

    used_mb = total_mb - avail_mb
    used_pct = 100.0 * used_mb / total_mb

    total_bytes = total_mb * MB
    used_bytes = used_mb * MB

    summary = (
        f"Used: {render.disksize(used_bytes)} of {render.disksize(total_bytes)}"
    )
    yield Result(state=State.OK, summary=summary)

    yield from check_levels(
        value=used_pct,
        levels_upper=params.get('levels'),
        metric_name='fs_used_percent',
        label='Usage',
        render_func=render.percent,
    )

    yield Metric('fs_used', used_bytes, boundaries=(0, total_bytes))
    yield Metric('fs_size', total_bytes)

    asp_state = data.get('ASP_STATE')
    asp_type = data.get('ASP_TYPE')
    if asp_state:
        yield Result(state=State.OK, notice=f"State: {asp_state}")
    if asp_type:
        yield Result(state=State.OK, notice=f"Type: {asp_type}")


agent_section_as400_agent_asp = AgentSection(
    name="as400_agent_asp",
    parse_function=parse_function,
)


check_plugin_as400_agent_asp = CheckPlugin(
    name="as400_agent_asp",
    sections=["as400_agent_asp"],
    service_name="ASP %s",
    discovery_function=discover_service,
    check_function=check_service,
    check_default_parameters={'levels': ('fixed', (80.0, 90.0))},
)
