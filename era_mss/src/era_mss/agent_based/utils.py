"""
Helper Functions
"""
from cmk.agent_based.v2 import (
    contains,
    Service,
    Result,
    State,
    check_levels,
)


STATE_MAP_ERA = {
    'OKA': State.OK,
    'ON':  State.OK,
    'ONN': State.OK,
    'ACTIVE': State.OK,
    'BACKUP': State.OK,
    'WAR': State.WARN,
    'DEG': State.WARN,
    'ERR': State.CRIT,
    'OFF': State.CRIT,
    'NOC': State.CRIT,
    'UNK': State.UNKNOWN,
    'n/a': State.UNKNOWN,
}

NA_INT = '-9999'

detect_era = contains('.1.3.6.1.2.1.1.2.0', ".1.3.6.1.4.1.311.1.1.3.1.2")


def era_state(value, mon=True):
    if not mon:
        return State.OK
    return STATE_MAP_ERA.get(value, State.UNKNOWN)


def is_na(value):
    return value in ('', 'n/a', NA_INT, None)


def parse_int(value):
    if is_na(value):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def parse_float(value):
    if is_na(value):
        return None
    try:
        return float(str(value).replace(',', '.'))
    except (TypeError, ValueError):
        return None


def discover_era(section):
    for entry in section:
        yield Service(item=entry)


def discover_era_simple(section):
    if section:
        yield Service()


def check_era(item, section):
    data = section.get(item)
    if data is None:
        return
    yield from _emit_results(data)


def check_era_simple(section):
    yield from _emit_results(section)


def _emit_results(data):
    for key, mon_data in data.items():
        value = mon_data['value']
        mon = mon_data.get('mon', True)
        yield Result(state=era_state(value, mon), summary=f"{key}: {value}")


def _levels(params, key):
    if not params or key is None:
        return ('no_levels', None)
    return params.get(key, ('no_levels', None))


def check_percent(label, value_str, metric, params=None, param_key=None):
    value = parse_int(value_str)
    if value is None:
        yield Result(state=State.UNKNOWN, summary=f"{label}: n/a")
        return
    yield from check_levels(
        value,
        levels_upper=_levels(params, param_key),
        metric_name=metric,
        render_func=lambda v: f"{v:.0f}%",
        label=label,
        boundaries=(0, 100),
    )


def check_count(label, value_str, metric, params=None, param_key=None):
    value = parse_int(value_str)
    if value is None:
        yield Result(state=State.UNKNOWN, summary=f"{label}: n/a")
        return
    yield from check_levels(
        value,
        levels_upper=_levels(params, param_key),
        metric_name=metric,
        render_func=lambda v: f"{v:.0f}",
        label=label,
    )
