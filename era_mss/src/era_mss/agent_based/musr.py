from .utils import detect_era, discover_era_simple, check_era_simple
from cmk.agent_based.v2 import (
    SNMPTree, 
    contains,
    CheckPlugin,
    SNMPSection,
)

def parse_musr(string_table):
    entry = string_table[0][0]
    keys = [
        ('musrCommunication.0', True),
        ('musrCommunication.1', True),
        ('musrHw.0', True),
        ('musrHw.1', True),
        ('musrTimeSync.0', True),
        ('musrTimeSync.1', True),
        ('musrTemp.0', True),
        ('musrTemp.1', True),
    ]
    section = {}
    for idx, config in enumerate(keys):
        key, do_mon = config
        if entry[idx]:
            section[key] = {'value': entry[idx], 'mon': do_mon}
    return section

snmp_section_era_musr = SNMPSection(
    name="era_musr",
    detect=detect_era,
    parse_function=parse_musr,
    fetch=[
        SNMPTree(
            base='.1.3.6.1.4.1.11588.1.5.112.1',
            oids=[
                '2.0', #musrCommunication.0
                '2.1', #musrCommunication.1
                '3.0', #musrHw.0
                '3.1', #musrHw.1
                '4.0', #musrTimeSync.0
                '4.1', #musrTimeSync.1
                '5.0', #musrTemp.0
                '5.1', #musrTemp.1
            ]
        ),
    ],
)


check_plugin_era_musr = CheckPlugin(     
    name='era_musr',
    service_name='ERA MUSR',
    discovery_function=discover_era_simple,
    check_function=check_era_simple,
)