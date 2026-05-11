#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.agent_based.v2 import (
    CheckPlugin,
    HostLabel,
    Result,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    State,
    startswith,
)


VERTIV_DETECT = startswith(".1.3.6.1.2.1.1.1.0", "Avocent ACS")


def parse_vertiv_acs8000_info(string_table):
    if not string_table or not string_table[0]:
        return None
    row = string_table[0]
    return {
        "hostname": row[0],
        "model": row[1],
        "part_number": row[2],
        "serial": row[3],
        "bootcode": row[4],
        "firmware": row[5],
    }


def host_label_vertiv_acs8000_info(section):
    yield HostLabel("cmk/vendor", "vertiv")
    yield HostLabel("cmk/device_type", "console_server")
    if section.get("model"):
        yield HostLabel("vertiv/model", section["model"].split()[0])


def discover_vertiv_acs8000_info(section):
    yield Service()


def check_vertiv_acs8000_info(section):
    yield Result(
        state=State.OK,
        summary=f"Model: {section['model']}, Firmware: {section['firmware']}, Serial: {section['serial']}",
        details=(
            f"Hostname: {section['hostname']}\n"
            f"Model: {section['model']}\n"
            f"Part number: {section['part_number']}\n"
            f"Serial: {section['serial']}\n"
            f"Bootcode: {section['bootcode']}\n"
            f"Firmware: {section['firmware']}"
        ),
    )


snmp_section_vertiv_acs8000_info = SimpleSNMPSection(
    name="vertiv_acs8000_info",
    parse_function=parse_vertiv_acs8000_info,
    host_label_function=host_label_vertiv_acs8000_info,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.10418.26.2.1",
        oids=[
            "1.0",  # acsHostName
            "2.0",  # acsProductModel
            "3.0",  # acsPartNumber
            "4.0",  # acsSerialNumber
            "6.0",  # acsBootcodeVersion
            "7.0",  # acsFirmwareVersion
        ],
    ),
    detect=VERTIV_DETECT,
)


check_plugin_vertiv_acs8000_info = CheckPlugin(
    name="vertiv_acs8000_info",
    service_name="Vertiv ACS device info",
    discovery_function=discover_vertiv_acs8000_info,
    check_function=check_vertiv_acs8000_info,
)
