#!/usr/bin/env python3
"""
NetBotz Camera Sensor Check Plugin for CheckMK (Agent Based API v2)
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


def parse_netbotz_camera(string_table):
    map_status = {
        "0": (State.UNKNOWN, "unknown"),
        "1": (State.CRIT, "disconnected"),
        "2": (State.OK, "connected"),
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

    for item, model, status, error_status, label, ip_addr in string_table:
        parsed[item] = {
            "model": model,
            "status": map_status.get(status, (State.WARN, f"status code {status}")),
            "error": map_error.get(error_status, (State.UNKNOWN, f"error code {error_status}")),
            "label": label,
            "ip": ip_addr,
        }

    return parsed


snmp_section_netbotz_camera = SimpleSNMPSection(
    name="netbotz_camera",
    parse_function=parse_netbotz_camera,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.52674.500.6.1.1",
        oids=[
            "1",  # cameraId (np. camera-52)
            "3",  # cameraModel (np. NBPD0165)
            "4",  # cameraStatus (2 = normal/connected)
            "5",  # cameraErrorStatus (0 = normal)
            "6",  # cameraLabel (np. APC by Schneider Electric-9A2606Y01334)
            "7",  # cameraIpAddress (np. 172.16.0.100)
        ],
    ),
    detect=startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.52674.500"),
)


def discover_netbotz_camera(section):
    for item in section:
        yield Service(item=item)


def check_netbotz_camera(item, section):
    if item not in section:
        yield Result(state=State.UNKNOWN, summary="Item not found")
        return

    cam = section[item]
    yield Result(
        state=cam["status"][0],
        summary=f"[{cam['label']}] ({cam['model']}, IP: {cam['ip']}), Status: {cam['status'][1]}",
    )

    if cam["error"][0] != State.OK:
        yield Result(
            state=cam["error"][0],
            summary=f"Error status: {cam['error'][1]}",
        )


check_plugin_netbotz_camera = CheckPlugin(
    name="netbotz_camera",
    service_name="Camera %s",
    discovery_function=discover_netbotz_camera,
    check_function=check_netbotz_camera,
)