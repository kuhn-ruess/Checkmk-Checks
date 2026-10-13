#!/usr/bin/env python3

"""
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


def parse_cmdb_syncer_eda(string_table):
    """
    Parse the EDA summary
    """
    try:
        parsed = json.loads(string_table[0][0])
    except (IndexError, ValueError):
        return None
    return parsed if isinstance(parsed, dict) else None


def discover_cmdb_syncer_eda(section):
    """
    One service per Syncer
    """
    yield Service()


def _render_count(value):
    """
    Render a counter
    """
    return str(int(value))


def _offender_text(offender):
    """
    One line per repeating event
    """
    status = offender.get('last_status') or 'unknown'
    if offender.get('last_http_status'):
        status = f"{status} (HTTP {offender['last_http_status']})"
    return (
        f"{offender.get('hostname')}: {offender.get('event')}"
        f" (rule {offender.get('rule')}, account {offender.get('account')}),"
        f" sends {offender.get('sends')}/{offender.get('threshold')},"
        f" failures {offender.get('failures')},"
        f" first sent {offender.get('first_sent')}, last sent {offender.get('last_sent')},"
        f" last status {status}"
    )


def check_cmdb_syncer_eda(params, section):
    """
    Check repeating and failing EDA events
    """
    if section.get('has_error'):
        yield Result(state=State.CRIT, summary=section.get('message', 'API error'))
        return

    yield from check_levels(
        value=section.get('repeating', 0),
        levels_upper=params.get('repeating', ('no_levels', None)),
        metric_name='cmdb_syncer_eda_repeating',
        label="Repeating events",
        render_func=_render_count,
    )
    yield from check_levels(
        value=section.get('repeating_hosts', 0),
        levels_upper=params.get('repeating_hosts', ('no_levels', None)),
        metric_name='cmdb_syncer_eda_repeating_hosts',
        label="Hosts with repeating events",
        render_func=_render_count,
    )

    failing = section.get('failing', 0)
    yield Result(
        state=State(params.get('failing_state', 2)) if failing else State.OK,
        summary=f"Failing: {failing}",
    )
    yield Metric('cmdb_syncer_eda_failing', failing)

    yield from check_levels(
        value=section.get('failed_24h', 0),
        levels_upper=params.get('failed_24h', ('no_levels', None)),
        metric_name='cmdb_syncer_eda_failed_24h',
        label="Rejected in last 24h",
        render_func=_render_count,
        notice_only=True,
    )
    yield from check_levels(
        value=section.get('max_sends', 0),
        levels_upper=params.get('max_sends', ('no_levels', None)),
        metric_name='cmdb_syncer_eda_max_sends',
        label="Most sends of one event",
        render_func=_render_count,
        notice_only=True,
    )
    yield from check_levels(
        value=section.get('events_24h', 0),
        metric_name='cmdb_syncer_eda_events_24h',
        label="Sent in last 24h",
        render_func=_render_count,
        notice_only=True,
    )
    yield from check_levels(
        value=section.get('pending', 0),
        metric_name='cmdb_syncer_eda_pending',
        label="Pending (below threshold)",
        render_func=_render_count,
        notice_only=True,
    )

    for account in section.get('accounts', []):
        yield Result(
            state=State.OK,
            notice=(
                f"Account {account.get('account')}: repeating {account.get('repeating')}"
                f" on {account.get('repeating_hosts')} hosts, failing {account.get('failing')},"
                f" pending {account.get('pending')}, sent 24h {account.get('events_24h')},"
                f" rejected 24h {account.get('failed_24h')}, max sends {account.get('max_sends')}"
            ),
        )

    offenders = section.get('offenders', [])
    if offenders:
        yield Result(state=State.OK, notice="Repeating events (most sends first):")
    for offender in offenders:
        yield Result(state=State.OK, notice=_offender_text(offender))
    if section.get('offenders_truncated'):
        yield Result(state=State.OK, notice="List truncated, see the Syncer GUI for all entries")


agent_section_cmdb_syncer_eda = AgentSection(
    name = "cmdb_syncer_eda",
    parse_function = parse_cmdb_syncer_eda,
)


check_plugin_cmdb_syncer_eda = CheckPlugin(
    name = "cmdb_syncer_eda",
    sections = ["cmdb_syncer_eda"],
    service_name = "EDA Events",
    discovery_function = discover_cmdb_syncer_eda,
    check_function = check_cmdb_syncer_eda,
    check_default_parameters = {
        'repeating': ('fixed', (1, 10)),
        'repeating_hosts': ('no_levels', None),
        'failing_state': 2,
        'failed_24h': ('no_levels', None),
        'max_sends': ('no_levels', None),
    },
    check_ruleset_name = "cmdb_syncer_eda",
)
