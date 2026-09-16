#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.agent_based.v2 import (
    check_levels,
    CheckPlugin,
    render,
    Result,
    Service,
    SNMPSection,
    SNMPTree,
    State,
)

from .ts4300_lib import (
    AVAILABILITY,
    DETECT_TS4300,
    device_name,
    OPERATIONAL_STATUS,
    status_result,
)

PORT_STATE = {
    "1": "no light",
    "2": "light detected",
    "3": "unknown",
}

DRIVE_TYPE = {
    "1": "LTO",
    "2": "Jaguar",
}


def _to_int(value):
    """Return the integer value of an SNMP counter or None."""
    try:
        return int(value)
    except ValueError:
        return None


def parse_ibm_ts4300_drives(string_table):
    """Merge the SNIA drive table with the IBM drive configuration table."""
    devices, config = string_table

    config_by_index = {}
    for index, installed, control_path, drive_type, generation, port0, port1, revision, wwn in config:
        if installed != "1":
            continue
        config_by_index[index] = {
            "control_path": control_path,
            "type": DRIVE_TYPE.get(drive_type),
            "generation": generation,
            "ports": [PORT_STATE.get(port0, port0), PORT_STATE.get(port1, port1)],
            "revision": revision,
            "wwn": wwn,
        }

    section = {}
    for index, name, availability, cleaning, mounts, wwn, hours, status in devices:
        drive = {
            "availability": availability,
            "status": status,
            "needs_cleaning": cleaning == "1",
            "mounts": _to_int(mounts),
            "operating_time": _to_int(hours),
        }
        config_entry = config_by_index.get(index, {})
        if config_entry and (not wwn or not config_entry["wwn"] or wwn == config_entry["wwn"]):
            drive.update(config_entry)
        section[device_name(name)] = drive

    return section


def discover_ibm_ts4300_drives(section):
    """Discovery"""
    for name in section:
        yield Service(item=name)


def check_ibm_ts4300_drives(item, params, section):
    """Check"""
    if not (drive := section.get(item)):
        return

    yield from status_result(AVAILABILITY, drive["availability"], "Availability")
    yield from status_result(OPERATIONAL_STATUS, drive["status"], "Status")

    if drive["needs_cleaning"]:
        yield Result(state=State(params["needs_cleaning"]), summary="Needs cleaning")
    else:
        yield Result(state=State.OK, notice="Does not need cleaning")

    if drive["mounts"] is not None:
        yield from check_levels(
            drive["mounts"],
            metric_name="tape_drive_mounts",
            label="Mounts",
            render_func=lambda v: f"{int(v)}",
            notice_only=True,
        )

    if drive["operating_time"] is not None:
        yield from check_levels(
            drive["operating_time"] * 3600,
            levels_upper=params.get("levels_operating_time"),
            metric_name="tape_drive_operating_time",
            label="Operating time",
            render_func=render.timespan,
            notice_only=True,
        )

    if drive.get("type"):
        yield Result(
            state=State.OK,
            notice=f"Type: {drive['type']}-{drive['generation']}, firmware: {drive['revision']}",
        )
        yield Result(
            state=State.OK,
            notice="Control path: {}".format("yes" if drive["control_path"] == "1" else "no"),
        )
        for number, port_state in enumerate(drive["ports"]):
            yield Result(state=State.OK, notice=f"Port {number}: {port_state}")


snmp_section_ibm_ts4300_drives = SNMPSection(
    name = "ibm_ts4300_drives",
    parse_function = parse_ibm_ts4300_drives,
    fetch = [
        SNMPTree(
            base = ".1.3.6.1.4.1.14851.3.1.6.2.1",
            oids = [
                '1',
                '3',
                '5',
                '6',
                '7',
                '8',
                '10',
                '11',
            ],
        ),
        SNMPTree(
            base = ".1.3.6.1.4.1.2.6.257.1.5.2.1",
            oids = [
                '1',
                '7',
                '8',
                '9',
                '10',
                '13',
                '14',
                '23',
                '26',
            ],
        ),
    ],
    detect = DETECT_TS4300,
)

check_plugin_ibm_ts4300_drives = CheckPlugin(
    name = "ibm_ts4300_drives",
    service_name = "Drive %s",
    discovery_function = discover_ibm_ts4300_drives,
    check_function = check_ibm_ts4300_drives,
    check_default_parameters = {
        "needs_cleaning": State.WARN.value,
    },
    check_ruleset_name = "ibm_ts4300_drives",
)
