#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.agent_based.v2 import (
    CheckPlugin,
    Result,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    State,
)

from .ts4300_lib import DETECT_TS4300

PSU_STATUS = {
    "1": (State.WARN, "not installed"),
    "2": (State.OK, "ok"),
    "3": (State.CRIT, "not ok"),
}


def parse_ibm_ts4300_psu(string_table):
    """One entry per power supply of every chassis."""
    section = {}
    for index, ps1, ps2, serial in string_table:
        for number, status in (("1", ps1), ("2", ps2)):
            section[f"{index}/{number}"] = {
                "status": status,
                "serial": serial,
            }
    return section


def discover_ibm_ts4300_psu(section):
    """Discovery, skips slots without a power supply."""
    for item, psu in section.items():
        if psu["status"] != "1":
            yield Service(item=item)


def check_ibm_ts4300_psu(item, section):
    """Check"""
    if not (psu := section.get(item)):
        return

    state, text = PSU_STATUS.get(psu["status"], (State.UNKNOWN, f"unknown ({psu['status']})"))
    yield Result(state=state, summary=f"Status: {text}")

    if psu["serial"]:
        yield Result(state=State.OK, notice=f"Chassis serial: {psu['serial']}")


snmp_section_ibm_ts4300_psu = SimpleSNMPSection(
    name = "ibm_ts4300_psu",
    parse_function = parse_ibm_ts4300_psu,
    fetch = SNMPTree(
        base = ".1.3.6.1.4.1.2.6.257.1.3.2.1",
        oids = [
            '1',
            '3',
            '4',
            '9',
        ],
    ),
    detect = DETECT_TS4300,
)

check_plugin_ibm_ts4300_psu = CheckPlugin(
    name = "ibm_ts4300_psu",
    service_name = "Power Supply %s",
    discovery_function = discover_ibm_ts4300_psu,
    check_function = check_ibm_ts4300_psu,
)
