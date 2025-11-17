from .utils import detect_era, discover_era, check_era
from cmk.agent_based.v2 import (
    SNMPTree, 
    CheckPlugin,
    SNMPSection,
)

def parse_rx(string_table):
    section = {}
    keys = [
        ('rxStatus', True),
        ('rxPower', True),
        ('rxFOAStatus', True),
        ('rxFOBStatus', True),
        ('rxActiveFO', False),
        ('rxAcAll', True),
        ('rxModesAll', True),
        ('rxModesGarbled', True),
        ('rxSiteName', True),
    ]
    for entry in string_table[0]:
        entry_data = {}
        for idx, config in enumerate(keys):
            key, do_mon = config
            if entry[idx]:
                entry_data[key] = {'value': entry[idx], 'mon': do_mon}
        site_name = str(entry_data['rxSiteName']['value'])
        del entry_data['rxSiteName']
        section[site_name] = entry_data
    return section

snmp_section_era_rx = SNMPSection(
    name="era_rx",
    detect=detect_era,
    parse_function=parse_rx,
    fetch=[
        SNMPTree(
            base='.1.3.6.1.4.1.11588.1.5.102.1.1',
            oids=[
                '2', #'rxStatus'
                '3', #'rxPower'
                '4', #'rxFOAStatus'
                '5', #'rxFOBStatus'
                '6', #'rxActiveFO'
                '7', #'rxAcAll'
                '8', #'rxModesAll'
                '9', #'rxModesGarbled'
                '81', #'rxSiteName'
            ]
        ),
    ],
)

check_plugin_era_rx = CheckPlugin(     
    name='era_rx',
    service_name='ERA %s',
    discovery_function=discover_era,
    check_function=check_era,
)