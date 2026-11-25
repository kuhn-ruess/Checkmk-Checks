#!/usr/bin/env python3

"""
NetBotz Enclosure Sensor Check Plugin for CheckMK (Agent Based API v2)
Based on Kuhn & Rueï¿½ GmbH netbotz_leak plugin
by kamil.jablonski@gmail.com
"""

from cmk.agent_based.v2 import (
    CheckPlugin,
    Result,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    State,
    startswith,
)


def parse_netbotz_enclosure(string_table):
    map_status = {
        "0": (State.CRIT, "disconnected"),
        "1": (State.CRIT, "error"),
        "2": (State.OK, "normal"),
    }

    map_error = {
        "0": (State.OK, "normal"),
        "1": (State.OK, "info"),
        "2": (State.WARN, "warning"),
        "3": (State.CRIT, "error"),
        "4": (State.CRIT, "critical"),
        "5": (State.CRIT, "failure"),
    }

    parsed = {}

    for item, status, error_status, label, serial in string_table:
        parsed[item] = {
            "label": label,
            "serial": serial,
            "status": map_status.get(status, (State.UNKNOWN, f"unknown status ({status})")),
            "error": map_error.get(error_status, (State.UNKNOWN, f"error code ({error_status})")),
        }

    return parsed


snmp_section_netbotz_enclosure = SimpleSNMPSection(
    name="netbotz_enclosure",
    parse_function=parse_netbotz_enclosure,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.52674.500.2.1.1",
        oids=[
            "1",  # NetBotz50-MIB::enclosureId
            "2",  # NetBotz50-MIB::enclosureStatus
            "3",  # NetBotz50-MIB::enclosureErrorStatus
            "4",  # NetBotz50-MIB::enclosureLabel
            "6",  # NetBotz50-MIB::enclosureSerialNumber
        ],
    ),
    detect=startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.52674.500"),
)


def discover_netbotz_enclosure(section):
    for item, data in section.items():
        label = data["label"]
        if label == "Appliance" or label.startswith("Wireless Coordinator"):
            yield Service(item=item)


def check_netbotz_enclosure(item, section):
    if item not in section:
        yield Result(state=State.UNKNOWN, summary="Item not found")
        return

    enc = section[item]
    yield Result(
        state=enc["status"][0],
        summary=f"[{enc['label']}] (S/N: {enc['serial']}), Status: {enc['status'][1]}",
    )

    if enc["error"][0] != State.OK:
        yield Result(
            state=enc["error"][0],
            summary=f"Error status: {enc['error'][1]}",
        )


check_plugin_netbotz_enclosure = CheckPlugin(
    name="netbotz_enclosure",
    service_name="Enclosure %s",
    discovery_function=discover_netbotz_enclosure,
    check_function=check_netbotz_enclosure,
)