from .utils import detect_era, discover_era_simple, check_era_simple
from cmk.agent_based.v2 import (
    SNMPTree, 
    contains,
    CheckPlugin,
    SNMPSection,
)

def parse_ntp(string_table):
    entry = string_table[0][0]
    keys = [
        ('ntpStatus.0', True),
        ('ntpStatus.1', True),
    ]
    section = {}
    for idx, config in enumerate(keys):
        key, do_mon = config
        if entry[idx]:
            section[key] = {'value': entry[idx], 'mon': do_mon}
    return section

snmp_section_era_ntp = SNMPSection(
    name="era_ntp",
    detect=detect_era,
    parse_function=parse_ntp,
    fetch=[
        SNMPTree(
            base='.1.3.6.1.4.1.11588.1.5.115.4.1.2',
            oids=[
                '0', #ntpStatus.0"
                '1', #ntpStatus.1
            ]
        ),
    ],
)


check_plugin_era_ntp = CheckPlugin(     
    name='era_ntp',
    service_name='ERA NTP',
    discovery_function=discover_era_simple,
    check_function=check_era_simple,
)