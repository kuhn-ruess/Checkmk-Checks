"""
ERA Target Processor server status (OID branch .101 = tpServerTable).
Monitors status cells and emits perfdata for CPU/Memory/Disk/LAN utilisation.
"""
from .utils import (
    detect_era,
    era_state,
    check_percent,
    check_count,
)
from cmk.agent_based.v2 import (
    SNMPTree,
    CheckPlugin,
    SNMPSection,
    Service,
    Result,
    OIDEnd,
)


STATUS_FIELDS = [
    # (key, mon, index_in_row_after_oidend)
    ('tpSwVer',       False, 0),
    ('tpSwProcesses', True,  1),
    ('tpTimeSync',    True,  2),
    ('tpIrrMode',     False, 3),
    ('tpCpu',         False, 4),
    ('tpMemory',      True,  6),
    ('tpDriveC',      False, 8),
    ('tpDriveD',      False, 10),
    ('tpLan1',        False, 12),
    ('tpLan2',        False, 14),
]

USAGE_FIELDS = [
    # (label, row-index-after-oidend, metric-name, params-key)
    ('CPU load',      5,  'era_cpu_load',      'cpu_load'),
    ('Memory usage',  7,  'era_memory_usage',  'memory'),
    ('Drive C usage', 9,  'era_drive_c_usage', 'drive_c'),
    ('Drive D usage', 11, 'era_drive_d_usage', 'drive_d'),
    ('LAN1 usage',    13, 'era_lan1_usage',    'lan1'),
    ('LAN2 usage',    15, 'era_lan2_usage',    'lan2'),
]

COUNT_FIELDS = [
    ('MLAT targets', 16, 'era_mlat_targets', 'mlat'),
    ('ADS-B targets', 17, 'era_adsb_targets', 'adsb'),
]


def parse_era_vserver(string_table):
    section = {}
    for entry in string_table[0]:
        oid_end = entry[0]
        section[oid_end] = entry[1:]
    return section


def discover_era_vserver(section):
    for item in section:
        yield Service(item=item)


def check_era_vserver(item, params, section):
    row = section.get(item)
    if row is None:
        return

    for key, mon, idx in STATUS_FIELDS:
        value = row[idx]
        if not value:
            continue
        yield Result(state=era_state(value, mon), summary=f"{key}: {value}")

    for label, idx, metric, pkey in USAGE_FIELDS:
        if idx >= len(row):
            continue
        yield from check_percent(label, row[idx], metric, params, pkey)

    for label, idx, metric, pkey in COUNT_FIELDS:
        if idx >= len(row):
            continue
        yield from check_count(label, row[idx], metric, params, pkey)


snmp_section_era_vserver = SNMPSection(
    name="era_vserver",
    detect=detect_era,
    parse_function=parse_era_vserver,
    fetch=[
        SNMPTree(
            base='.1.3.6.1.4.1.11588.1.5.101.1',
            oids=[
                OIDEnd(),  # row[0]
                '2',   # tpSwVer (status)        - row[1]
                '3',   # tpSwProcesses           - row[2]
                '4',   # tpTimeSync              - row[3]
                '5',   # tpIrrMode               - row[4]
                '6',   # tpCpu (status)          - row[5]
                '7',   # tpCpuLoad (int %)       - row[6]
                '8',   # tpMemory (status)       - row[7]
                '9',   # tpMemoryUsage (int %)   - row[8]
                '10',  # tpDriveC (status)       - row[9]
                '11',  # tpDriveCUsage (int %)   - row[10]
                '12',  # tpDriveD (status)       - row[11]
                '13',  # tpDriveDUsage (int %)   - row[12]
                '14',  # tpLan1 (status)         - row[13]
                '15',  # tpLan1Usage (int %)     - row[14]
                '16',  # tpLan2 (status)         - row[15]
                '17',  # tpLan2Usage (int %)     - row[16]
                '71',  # tpMlatCnt (int)         - row[17]
                '72',  # tpAdsbCnt (int)         - row[18]
            ],
        ),
    ],
)


check_plugin_era_vserver = CheckPlugin(
    name='era_vserver',
    service_name='ERA vServer %s',
    discovery_function=discover_era_vserver,
    check_function=check_era_vserver,
    check_ruleset_name='era_vserver',
    check_default_parameters={},
)
