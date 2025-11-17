from .utils import detect_era, discover_era, state_map_era
from cmk.agent_based.v2 import (
    SNMPTree, 
    contains,
    Result,
    State,
    CheckPlugin,
    SNMPSection,
)

def parse_rmtr(string_table):
    section = {}
    for entry in string_table[0]:
        entry_data = {
            'status': entry[0],
            'name': entry[1],
        }
        section[entry_data['name']] = entry_data
    return section

snmp_section_era_rmtr = SNMPSection(
    name="era_rmtr",
    detect=detect_era,
    parse_function=parse_rmtr,
    fetch=[
        SNMPTree(
            base='.1.3.6.1.4.1.11588.1.5.104.1',
            oids=[
                '2', #Status
                '81', #rmtrSiteName
            ]
        ),
    ],
)

def check_era_rmtr(item, section):
    data = section[item]
    state = state_map_era.get(data['status'], State.CRIT)
    yield Result(state=state, summary=f"Status: {data['status']}")


check_plugin_era_rmtr = CheckPlugin(     
    name='era_rmtr',
    service_name='ERA %s',
    discovery_function=discover_era,
    check_function=check_era_rmtr,
)