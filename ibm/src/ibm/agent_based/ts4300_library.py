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
    SNMPSection,
    SNMPTree,
    State,
)

from .ts4300_lib import (
    DETECT_TS4300,
    OPERATIONAL_STATUS,
    status_result,
)


def parse_ibm_ts4300_library(string_table):
    """Build the library status from computerSystem and subChassis data."""
    system, chassis = string_table
    if not system:
        return None

    name, status = system[0]
    return {
        "name": name,
        "status": status,
        "chassis": [
            {
                "index": index,
                "name": chassis_name,
                "status": chassis_status,
            }
            for index, chassis_name, chassis_status in chassis
        ],
    }


def discover_ibm_ts4300_library(section):
    """Discovery"""
    yield Service()


def check_ibm_ts4300_library(section):
    """Check"""
    yield from status_result(OPERATIONAL_STATUS, section["status"], "Status")

    for chassis in section["chassis"]:
        state, text = OPERATIONAL_STATUS.get(
            chassis["status"], (State.UNKNOWN, f"unknown ({chassis['status']})")
        )
        yield Result(
            state=state,
            notice=f"Chassis {chassis['index']}: {text}",
            details=f"Chassis {chassis['index']} ({chassis['name']}): {text}",
        )

    yield Result(state=State.OK, notice=f"Name: {section['name']}")


snmp_section_ibm_ts4300_library = SNMPSection(
    name = "ibm_ts4300_library",
    parse_function = parse_ibm_ts4300_library,
    fetch = [
        SNMPTree(
            base = ".1.3.6.1.4.1.14851.3.1.10",
            oids = [
                '1.0',
                '2.0',
            ],
        ),
        SNMPTree(
            base = ".1.3.6.1.4.1.14851.3.1.4.10.1",
            oids = [
                '1',
                '9',
                '10',
            ],
        ),
    ],
    detect = DETECT_TS4300,
)

check_plugin_ibm_ts4300_library = CheckPlugin(
    name = "ibm_ts4300_library",
    service_name = "Library Status",
    discovery_function = discover_ibm_ts4300_library,
    check_function = check_ibm_ts4300_library,
)
