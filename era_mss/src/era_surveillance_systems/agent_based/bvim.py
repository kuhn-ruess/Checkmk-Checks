from .utils import detect_era, discover_era_simple, check_era_simple
from cmk.agent_based.v2 import (
    SNMPTree, 
    contains,
    Service,
    Result,
    State,
    CheckPlugin,
    SNMPSection,
)

def parse_bvim(string_table):
    entry = string_table[0][0]
    keys = [
        ("tp1-bvimPowerY", True),
        ("tp1-bvimDinStatus", True),
        ("tp2-bvimPowerX", True),
        ("tp2-bvimPowerY", True),
        ("tp2-bvimDinStatus", True),
    ]
    section = {}
    for idx, config in enumerate(keys):
        key, do_mon = config
        if entry[idx]:
            section[key] = {'value': entry[idx], 'mon': do_mon}
    return section

snmp_section_era_bvim = SNMPSection(
    name="era_bvim",
    detect=contains('.1.3.6.1.2.1.1.2.0', ".1.3.6.1.4.1.311.1.1.3.1.2"),
    parse_function=parse_bvim,
    fetch=[
        SNMPTree(
            base='.1.3.6.1.4.1.11588.1.5.111',
            oids=[
                '1.1.4.0', #tp1-bvimPowerY.0
                '1.1.5.0', # tp1-bvimDinStatus.0
                '2.1.3.0', # tp2-bvimPowerX.0
                '2.1.4.0', # tp2-bvimPowerY.0
                '2.1.5.0', # tp2-bvimDinStatus.0
            ]
        ),
    ],
)

check_plugin_era_bvim = CheckPlugin(     
    name='era_bvim',
    service_name='ERA BVIM',
    discovery_function=discover_era_simple,
    check_function=check_era_simple,
)