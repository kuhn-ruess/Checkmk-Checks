"""
ERA MSS overall rollup statuses (OID branch .100 = main).
tpTable per-TP rollups plus global scalars for txs, rmtr, rack, networkDevices.
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


TP_COL_NAMES = [
    'tpAsterixStatus',
    'tpServerStatus',
    'rxs',
    'inputData',
]


def parse_era_main(string_table):
    tp_rows, scalars = string_table
    section = {}
    for row in tp_rows:
        tp_idx = row[0]
        values = row[1:]
        section[f"TP {tp_idx}"] = dict(zip(TP_COL_NAMES, values))
    scalar_names = ['txs', 'rmtr', 'rack', 'networkDevices']
    if scalars and scalars[0]:
        section['System'] = dict(zip(scalar_names, scalars[0]))
    return section


def discover_era_main(section):
    for item in section:
        yield Service(item=item)


def check_era_main(item, section):
    data = section.get(item)
    if not data:
        return
    for key, value in data.items():
        if not value:
            continue
        yield Result(state=era_state(value), summary=f"{key}: {value}")


snmp_section_era_main = SNMPSection(
    name="era_main",
    detect=detect_era,
    parse_function=parse_era_main,
    fetch=[
        SNMPTree(
            base='.1.3.6.1.4.1.11588.1.5.100.1.1',
            oids=[
                OIDEnd(),
                '2',  # tpAsterixStatus
                '3',  # tpServerStatus
                '4',  # rxs
                '5',  # inputData
            ],
            # main.1 = tpTable (col 1 is tpIndex, col 2..5 are status)
        ),
        SNMPTree(
            base='.1.3.6.1.4.1.11588.1.5.100',
            oids=[
                '3.0',  # txs
                '4.0',  # rmtr
                '5.0',  # rack
                '6.0',  # networkDevices
            ],
        ),
    ],
)


check_plugin_era_main = CheckPlugin(
    name='era_main',
    service_name='ERA Status %s',
    discovery_function=discover_era_main,
    check_function=check_era_main,
)
