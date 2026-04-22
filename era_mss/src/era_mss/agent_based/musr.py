"""
ERA MUSR table (OID branch .112 = musrTable).
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


COLS = [
    ('musrCommunication', True),
    ('musrHw',            True),
    ('musrTimeSync',      True),
    ('musrTemp',          True),
]


def parse_era_musr(string_table):
    section = {}
    for entry in string_table[0]:
        oid_end = entry[0]
        values = entry[1:]
        if not any(values):
            continue
        section[oid_end] = dict(zip((c[0] for c in COLS), values))
    return section


def discover_era_musr(section):
    for item in section:
        yield Service(item=item)


def check_era_musr(item, section):
    data = section.get(item)
    if not data:
        return
    for key, mon in COLS:
        value = data.get(key)
        if not value:
            continue
        yield Result(state=era_state(value, mon), summary=f"{key}: {value}")


snmp_section_era_musr = SNMPSection(
    name="era_musr",
    detect=detect_era,
    parse_function=parse_era_musr,
    fetch=[
        SNMPTree(
            base='.1.3.6.1.4.1.11588.1.5.112.1',
            oids=[
                OIDEnd(),
                '2',  # musrCommunication
                '3',  # musrHw
                '4',  # musrTimeSync
                '5',  # musrTemp
            ],
        ),
    ],
)


check_plugin_era_musr = CheckPlugin(
    name='era_musr',
    service_name='ERA MUSR %s',
    discovery_function=discover_era_musr,
    check_function=check_era_musr,
)
