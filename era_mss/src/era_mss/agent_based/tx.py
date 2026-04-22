"""
ERA TX transmitters (OID branch .103.1 = txsTp.1).
Single-TP table; emits status results for each column.
"""
from .utils import detect_era, era_state
from cmk.agent_based.v2 import (
    SNMPTree,
    CheckPlugin,
    SNMPSection,
    Service,
    Result,
)


STATUS_FIELDS = [
    # (key, mon, row-index)
    ('txStatus',      True,  0),
    ('txLan1',        True,  1),
    ('txLan2',        True,  2),
    ('txOutPower',    True,  3),
    ('txVSWR',        True,  4),
    ('txOutPul',      True,  5),
    ('txNtpComm',     True,  6),
    ('txDutyCycle',   True,  7),
    ('txInputData',   True,  8),
    ('txOverheating', True,  9),
    ('txPower',       True,  10),
    ('txModesAddr',   False, 11),
    ('txLan1Addr',    False, 12),
    ('txLan2Addr',    False, 13),
]


def parse_era_tx(string_table):
    section = {}
    for entry in string_table[0]:
        site = (entry[14] or '').strip()
        if not site:
            continue
        section[site] = entry[:14]
    return section


def discover_era_tx(section):
    for item in section:
        yield Service(item=item)


def check_era_tx(item, section):
    row = section.get(item)
    if row is None:
        return
    for key, mon, idx in STATUS_FIELDS:
        value = row[idx]
        if not value:
            continue
        yield Result(state=era_state(value, mon), summary=f"{key}: {value}")


snmp_section_era_tx = SNMPSection(
    name="era_tx",
    detect=detect_era,
    parse_function=parse_era_tx,
    fetch=[
        SNMPTree(
            base='.1.3.6.1.4.1.11588.1.5.103.1',
            oids=[
                '2',   # txStatus
                '3',   # txLan1
                '4',   # txLan2
                '5',   # txOutPower
                '6',   # txVSWR
                '7',   # txOutPul
                '8',   # txNtpComm
                '9',   # txDutyCycle
                '10',  # txInputData
                '11',  # txOverheating
                '12',  # txPower
                '13',  # txModesAddr
                '14',  # txLan1Addr
                '15',  # txLan2Addr
                '81',  # txSiteName
            ],
        ),
    ],
)


check_plugin_era_tx = CheckPlugin(
    name='era_tx',
    service_name='ERA %s',
    discovery_function=discover_era_tx,
    check_function=check_era_tx,
)
