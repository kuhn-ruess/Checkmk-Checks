"""
ERA RMTR (reference and monitoring transponders), OID branch .104.
"""
from .utils import detect_era, era_state
from cmk.agent_based.v2 import (
    SNMPTree,
    CheckPlugin,
    SNMPSection,
    Service,
    Result,
)


def parse_era_rmtr(string_table):
    section = {}
    for entry in string_table[0]:
        status, name = entry
        name = (name or '').strip()
        if not name:
            continue
        section[name] = status
    return section


def discover_era_rmtr(section):
    for item in section:
        yield Service(item=item)


def check_era_rmtr(item, section):
    status = section.get(item)
    if status is None:
        return
    yield Result(state=era_state(status), summary=f"Status: {status}")


snmp_section_era_rmtr = SNMPSection(
    name="era_rmtr",
    detect=detect_era,
    parse_function=parse_era_rmtr,
    fetch=[
        SNMPTree(
            base='.1.3.6.1.4.1.11588.1.5.104.1',
            oids=[
                '2',   # rmtrStatus
                '81',  # rmtrSiteName
            ],
        ),
    ],
)


check_plugin_era_rmtr = CheckPlugin(
    name='era_rmtr',
    service_name='ERA %s',
    discovery_function=discover_era_rmtr,
    check_function=check_era_rmtr,
)
