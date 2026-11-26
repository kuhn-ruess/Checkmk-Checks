#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de

Camera check contributed by Kamil Jablonski (GitHub: Jarowitt)
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

MAP_STATUS = {
    "0": (State.UNKNOWN, "unknown"),
    "1": (State.CRIT, "disconnected"),
    "2": (State.OK, "connected"),
}

MAP_ERROR = {
    "0": (State.OK, "normal"),
    "1": (State.OK, "info"),
    "2": (State.WARN, "warning"),
    "3": (State.CRIT, "error"),
    "4": (State.CRIT, "critical"),
    "5": (State.CRIT, "failure"),
}


def parse_netbotz_camera(string_table):
    """Map the camera table to a dict keyed by camera id."""
    return {
        item: {
            "model": model,
            "label": label,
            "ip": ip_addr,
            "status": MAP_STATUS.get(status, (State.UNKNOWN, f"unknown status ({status})")),
            "error": MAP_ERROR.get(error_status, (State.UNKNOWN, f"unknown error status ({error_status})")),
        }
        for item, model, status, error_status, label, ip_addr in string_table
    }


snmp_section_netbotz_camera = SimpleSNMPSection(
    name="netbotz_camera",
    parse_function=parse_netbotz_camera,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.52674.500.6.1.1",
        oids=[
            "1",  # NetBotz50-MIB::cameraId
            "3",  # NetBotz50-MIB::cameraModel
            "4",  # NetBotz50-MIB::cameraStatus
            "5",  # NetBotz50-MIB::cameraErrorStatus
            "6",  # NetBotz50-MIB::cameraLabel
            "7",  # NetBotz50-MIB::cameraIpAddress
        ],
    ),
    detect=startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.52674.500"),
)


def discover_netbotz_camera(section):
    """One service per camera."""
    for item in section:
        yield Service(item=item)


def check_netbotz_camera(item, section):
    """Report the connection status and a non normal error status."""
    if not (cam := section.get(item)):
        return
    yield Result(
        state=cam["status"][0],
        summary=f"[{cam['label']}] ({cam['model']}, IP: {cam['ip']}), Status: {cam['status'][1]}",
    )
    if cam["error"][0] != State.OK:
        yield Result(state=cam["error"][0], summary=f"Error status: {cam['error'][1]}")


check_plugin_netbotz_camera = CheckPlugin(
    name="netbotz_camera",
    service_name="Camera %s",
    discovery_function=discover_netbotz_camera,
    check_function=check_netbotz_camera,
)
