from .utils import detect_era, discover_era, check_era
from cmk.agent_based.v2 import (
    SNMPTree, 
    CheckPlugin,
    SNMPSection,
    OIDEnd,
)


def parse_vserver(string_table):
    section = {}
    keys = [
        ('tpSwVer', False),
        ('tpSwProcesses', True),
        ('tpTimeSync', True),
        ('tpIrrMode', True),
        ('tpCpu', False),
        ('tpCpuLoad', True),
        ('tpMemory', False),
        ('tpMemoryUsage', False),
        ('tpDriveC', False),
        ('tpDriveCUsage', False),
        ('tpDriveD', False),
        ('tpDriveDUsage', True),
        ('tpLan1', False),
        ('tpLan1Usage', False),
        ('tpLan2', False),
        ('tpLan2Usage', True),
        ('tpMlatCnt', False),
        ('tpAdsbCnt', False),
    ]
    for srv_idx, entry in enumerate(string_table[0]):
        vserver = {}
        for idx, config in enumerate(keys):
            key, do_mon = config
            if entry[idx]:
                vserver[key] = {'value': entry[idx], 'mon': do_mon}
            section[str(srv_idx)] = vserver
    return section

snmp_section_era_vserver = SNMPSection(
    name="era_vserver",
    detect=detect_era,
    parse_function=parse_vserver,
    fetch=[
        SNMPTree(
            base='.1.3.6.1.4.1.11588.1.5.101.1',
            oids=[
                OIDEnd(),
                '2', #tpSwVer         StatusValueS,
                '3', #tpSwProcesses   StatusValueS,
                '4', #tpTimeSync      StatusValueS,
                '5', #tpIrrMode       OCTET STRING,
                '6', #tpCpu           StatusValueS,
                '7', #tpCpuLoad       INTEGER,
                '8', #tpMemory        StatusValueS,
                '9', #tpMemoryUsage   INTEGER,
                '10', #tpDriveC        StatusValueS,
                '11', #tpDriveCUsage   INTEGER,
                '12', #tpDriveD        StatusValueS,
                '13', #tpDriveDUsage   INTEGER,
                '14', #tpLan1          StatusValueS,
                '15', #tpLan1Usage     INTEGER,
                '16', #tpLan2          StatusValueS,
                '17', #tpLan2Usage     INTEGER,
                '18', #tperaCnt       INTEGER,
                '19', #tpAdsbCnt       INTEGER,
            ]
        ),
    ],
)

check_plugin_era_vserver = CheckPlugin(     
    name='era_vserver',
    service_name='ERA vServer %s',
    discovery_function=discover_era,
    check_function=check_era,
)