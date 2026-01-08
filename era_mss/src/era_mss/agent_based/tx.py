from .utils import detect_era, discover_era, check_era
from cmk.agent_based.v2 import (
    SNMPTree, 
    contains,
    CheckPlugin,
    SNMPSection,
)

def parse_tx(string_table):
    section = {}
    keys = [
            ('txStatus', True),
            ('txLan1', True),
            ('txLan2', True),
            ('txOutPower', True),
            ('txVSWR', True),
            ('txOutPul', True),
            ('txNtpComm', True),
            ('txDutyCycle', True),
            ('txInputData', True),
            ('txOverheating', True),
            ('txPower', True),
            ('txModesAddr', False),
            ('txLan1Addr', False),
            ('txLan2Addr', False),
            ('txSiteName', True),
    ]
    for entry in string_table[0]:
        entry_data = {}
        for idx, key_data in enumerate(keys):
            key, do_mon = key_data
            if entry[idx]:
                entry_data[key] = {'value': entry[idx], 'mon': do_mon}
        site_name = str(entry_data['txSiteName']['value'])
        del entry_data['txSiteName']
        section[site_name] = entry_data
    return section


snmp_section_era_tx = SNMPSection(
    name="era_tx",
    detect=detect_era,
    parse_function=parse_tx,
    fetch=[
        SNMPTree(
            base='.1.3.6.1.4.1.11588.1.5.103.1',
            oids=[
                '2',  #'txStatus',
                '3',  #'txLan1',
                '4',  #'txLan2',
                '5',  #'txOutPower',
                '6',  #'txVSWR',
                '7',  #'txOutPul',
                '8',  #'txNtpComm',
                '9',  #'txDutyCycle',
                '10', # 'txInputData',
                '11', # 'txOverheating',
                '12', # 'txPower',
                '13', # 'txModesAddr',
                '14', # 'txLan1Addr',
                '15', # 'txLan2Addr',
                '81', # 'txSiteName',
            ]
        ),
    ],
)

check_plugin_era_tx = CheckPlugin(     
    name='era_tx',
    service_name='ERA %s',
    discovery_function=discover_era,
    check_function=check_era,
)