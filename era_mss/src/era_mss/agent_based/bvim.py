"""
ERA BVIM (base-station vim), OID branch .111. One sub-table per TP (1..8).
"""
from .utils import detect_era, era_state
from cmk.agent_based.v2 import (
    SNMPTree,
    CheckPlugin,
    SNMPSection,
    Service,
    Result,
    OIDEnd,
)


BVIM_TP_COUNT = 8
BVIM_BASE = '.1.3.6.1.4.1.11588.1.5.111'

COLS = [
    ('bvimTemp',      True),
    ('bvimPowerX',    True),
    ('bvimPowerY',    True),
    ('bvimDinStatus', True),
]


def parse_era_bvim(string_table):
    section = {}
    for tp_idx, table in enumerate(string_table, start=1):
        for entry in table:
            oid_end = entry[0]
            values = entry[1:]
            if not any(values):
                continue
            item = f"TP{tp_idx} BVIM {oid_end}"
            section[item] = dict(zip((c[0] for c in COLS), values))
    return section


def discover_era_bvim(section):
    for item in section:
        yield Service(item=item)


def check_era_bvim(item, section):
    data = section.get(item)
    if not data:
        return
    for key, mon in COLS:
        value = data.get(key)
        if not value:
            continue
        yield Result(state=era_state(value, mon), summary=f"{key}: {value}")


snmp_section_era_bvim = SNMPSection(
    name="era_bvim",
    detect=detect_era,
    parse_function=parse_era_bvim,
    fetch=[
        SNMPTree(
            base=f'{BVIM_BASE}.{tp}.1',
            oids=[
                OIDEnd(),
                '2',  # tp{n}-bvimTemp
                '3',  # tp{n}-bvimPowerX
                '4',  # tp{n}-bvimPowerY
                '5',  # tp{n}-bvimDinStatus
            ],
        ) for tp in range(1, BVIM_TP_COUNT + 1)
    ],
)


check_plugin_era_bvim = CheckPlugin(
    name='era_bvim',
    service_name='ERA %s',
    discovery_function=discover_era_bvim,
    check_function=check_era_bvim,
)
