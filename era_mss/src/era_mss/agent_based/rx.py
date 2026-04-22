"""
ERA RX receivers (OID branch .102 = rxsTp).
One sub-table per TP-server view (up to 8). Services are named
"TP<n> <site>" so the same physical RX can be monitored per TP.
Adds counter metrics and garbled-frame ratio.
"""
from .utils import (
    detect_era,
    era_state,
    parse_int,
    check_count,
)
from cmk.agent_based.v2 import (
    SNMPTree,
    CheckPlugin,
    SNMPSection,
    Service,
    Result,
    State,
    check_levels,
    get_rate,
    get_value_store,
    GetRateError,
    OIDEnd,
)


RX_TP_COUNT = 8
RX_BASE = '.1.3.6.1.4.1.11588.1.5.102'


STATUS_FIELDS = [
    # (key, mon, row-index)
    ('rxStatus',    True,  1),
    ('rxPower',     True,  2),
    ('rxFOAStatus', True,  3),
    ('rxFOBStatus', True,  4),
    ('rxActiveFO',  False, 5),
]

COUNT_FIELDS = [
    # (label, row-index, metric, params-key)
    ('A/C codes',           6, 'era_rx_ac_all',       'ac_all'),
    ('Mode-S messages',     7, 'era_rx_modes_all',    'modes_all'),
    ('Mode-S garbled',      8, 'era_rx_modes_garbled', 'modes_garbled'),
]


def parse_era_rx(string_table):
    section = {}
    for tp_idx, table in enumerate(string_table, start=1):
        for entry in table:
            site = (entry[9] or '').strip()
            status_values = [c for c in entry[1:6] if c]
            if not site or not status_values:
                continue
            item = f"TP{tp_idx} {site}"
            section[item] = {
                'tp': tp_idx,
                'row': entry,
            }
    return section


def discover_era_rx(section):
    for item in section:
        yield Service(item=item)


def check_era_rx(item, params, section):
    data = section.get(item)
    if data is None:
        return
    row = data['row']
    tp = data['tp']

    for key, mon, idx in STATUS_FIELDS:
        value = row[idx]
        if not value:
            continue
        yield Result(state=era_state(value, mon), summary=f"{key}: {value}")

    value_store = get_value_store()
    ac_value = parse_int(row[6])
    modes_all = parse_int(row[7])
    modes_garbled = parse_int(row[8])

    if ac_value is not None:
        yield from check_count('A/C codes', row[6], 'era_rx_ac_all', params, 'ac_all')

    if modes_all is not None:
        try:
            rate = get_rate(
                value_store, f"era_rx_modes_all.{tp}.{item}", 0.0, float(modes_all),
                raise_overflow=True,
            )
            yield from check_levels(
                rate,
                metric_name='era_rx_modes_all_rate',
                render_func=lambda v: f"{v:.2f}/s",
                label='Mode-S rate',
            )
        except GetRateError:
            pass
        yield from check_count('Mode-S total', row[7], 'era_rx_modes_all', params, 'modes_all')

    if modes_all and modes_all > 0 and modes_garbled is not None:
        ratio = 100.0 * modes_garbled / modes_all
        levels = (params or {}).get('garbled_ratio', ('no_levels', None))
        yield from check_levels(
            ratio,
            levels_upper=levels,
            metric_name='era_rx_modes_garbled_ratio',
            render_func=lambda v: f"{v:.2f}%",
            label='Garbled ratio',
            boundaries=(0.0, 100.0),
        )


snmp_section_era_rx = SNMPSection(
    name="era_rx",
    detect=detect_era,
    parse_function=parse_era_rx,
    fetch=[
        SNMPTree(
            base=f'{RX_BASE}.{tp}.1',
            oids=[
                OIDEnd(),  # row[0]
                '2',       # rxStatus         - row[1]
                '3',       # rxPower          - row[2]
                '4',       # rxFOAStatus      - row[3]
                '5',       # rxFOBStatus      - row[4]
                '6',       # rxActiveFO       - row[5]
                '71',      # rxAcAll          - row[6]
                '73',      # rxModesAll       - row[7]
                '74',      # rxModesGarbled   - row[8]
                '81',      # rxSiteName       - row[9]
            ],
        ) for tp in range(1, RX_TP_COUNT + 1)
    ],
)


check_plugin_era_rx = CheckPlugin(
    name='era_rx',
    service_name='ERA %s',
    discovery_function=discover_era_rx,
    check_function=check_era_rx,
    check_ruleset_name='era_rx',
    check_default_parameters={},
)
