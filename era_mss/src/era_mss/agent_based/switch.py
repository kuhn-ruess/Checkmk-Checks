"""
ERA network switch table (OID branch .115.2 = switchTable).
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


def parse_era_switch(string_table):
    section = {}
    for entry in string_table[0]:
        oid_end, status = entry
        if not status:
            continue
        section[oid_end] = status
    return section


def discover_era_switch(section):
    for item in section:
        yield Service(item=item)


def check_era_switch(item, section):
    status = section.get(item)
    if status is None:
        return
    yield Result(state=era_state(status), summary=f"Status: {status}")


snmp_section_era_switch = SNMPSection(
    name="era_switch",
    detect=detect_era,
    parse_function=parse_era_switch,
    fetch=[
        SNMPTree(
            base='.1.3.6.1.4.1.11588.1.5.115.2.1',
            oids=[
                OIDEnd(),
                '2',  # switchStatus
            ],
        ),
    ],
)


check_plugin_era_switch = CheckPlugin(
    name='era_switch',
    service_name='ERA Switch %s',
    discovery_function=discover_era_switch,
    check_function=check_era_switch,
)
