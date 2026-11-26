#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de

Enclosure check contributed by Kamil Jablonski (GitHub: Jarowitt)
"""

from cmk.agent_based.v2 import (
    CheckPlugin,
    Result,
    Service,
    SNMPSection,
    SNMPTree,
    State,
    startswith,
)

MAP_STATUS = {
    "0": (State.CRIT, "disconnected"),
    "1": (State.CRIT, "error"),
    "2": (State.OK, "normal"),
}

MAP_ERROR = {
    "0": (State.OK, "normal"),
    "1": (State.OK, "info"),
    "2": (State.WARN, "warning"),
    "3": (State.CRIT, "error"),
    "4": (State.CRIT, "critical"),
    "5": (State.CRIT, "failure"),
}


def _error(value):
    """Map an error status code to state and text."""
    return MAP_ERROR.get(value, (State.UNKNOWN, f"unknown error status ({value})"))


def parse_netbotz_enclosure(string_table):
    """Join the enclosure table with hardware and firmware data of the appliance."""
    enc_table, hw_table, fw_table, module_fw_table, global_table = string_table

    hw_by_serial = {serial: (model, hw_rev) for model, serial, hw_rev in hw_table}
    fw_by_serial = dict(fw_table)
    module_fw = {model: version for model, version in module_fw_table if model}
    global_error = _error(global_table[0][0]) if global_table else None

    parsed = {}
    for item, status, error_status, label, parent, serial in enc_table:
        model, hw_rev = hw_by_serial.get(serial, (None, None))
        firmware = fw_by_serial.get(serial)
        if label.startswith("Wireless Coordinator") and "NBWC100U" in module_fw:
            model, firmware = "NBWC100U", module_fw["NBWC100U"]

        parsed[item] = {
            "label": label,
            "parent": parent,
            "serial": serial,
            "model": model,
            "hw_rev": hw_rev,
            "firmware": firmware,
            "status": MAP_STATUS.get(status, (State.UNKNOWN, f"unknown status ({status})")),
            "error": _error(error_status),
            "global_error": global_error if label == "Appliance" else None,
        }
    return parsed


snmp_section_netbotz_enclosure = SNMPSection(
    name="netbotz_enclosure",
    parse_function=parse_netbotz_enclosure,
    fetch=[
        SNMPTree(
            base=".1.3.6.1.4.1.52674.500.2.1.1",
            oids=[
                "1",  # NetBotz50-MIB::enclosureId
                "2",  # NetBotz50-MIB::enclosureStatus
                "3",  # NetBotz50-MIB::enclosureErrorStatus
                "4",  # NetBotz50-MIB::enclosureLabel
                "5",  # NetBotz50-MIB::enclosureParentEncId
                "6",  # NetBotz50-MIB::enclosureSerialNumber
            ],
        ),
        SNMPTree(
            base=".1.3.6.1.4.1.318.1.4.2.2.1",
            oids=[
                "2",  # PowerNet-MIB::modelNumber
                "3",  # PowerNet-MIB::serialNumber
                "14",  # PowerNet-MIB::hardwareRevision
            ],
        ),
        SNMPTree(
            base=".1.3.6.1.4.1.318.1.4.2.4.1",
            oids=[
                "2",  # PowerNet-MIB::serialNumber
                "4",  # PowerNet-MIB::firmwareVersion
            ],
        ),
        SNMPTree(
            base=".1.3.6.1.4.1.52674.500.7.1.1",
            oids=[
                "1",  # NetBotz50-MIB::firmwareModel
                "2",  # NetBotz50-MIB::firmwareVersion
            ],
        ),
        SNMPTree(
            base=".1.3.6.1.4.1.52674.500",
            oids=[
                "100",  # NetBotz50-MIB::netBotzErrorStatus
            ],
        ),
    ],
    detect=startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.52674.500"),
)


def discover_netbotz_enclosure(section):
    """One service per enclosure (appliance, pods, probes, wireless coordinator)."""
    for item in section:
        yield Service(item=item)


def check_netbotz_enclosure(item, section):
    """Report enclosure status, error status and hardware details."""
    if not (enc := section.get(item)):
        return

    details = [
        f"Label: {enc['label']}",
        f"Serial number: {enc['serial']}",
        f"Parent enclosure: {enc['parent']}",
    ]
    for title, key in (("Model", "model"), ("Hardware revision", "hw_rev"), ("Firmware", "firmware")):
        if enc[key]:
            details.append(f"{title}: {enc[key]}")

    yield Result(
        state=enc["status"][0],
        summary=f"[{enc['label']}], Status: {enc['status'][1]}",
        details="\n".join(details),
    )
    yield Result(state=enc["error"][0], notice=f"Error status: {enc['error'][1]}")
    if enc["global_error"] is not None:
        yield Result(state=enc["global_error"][0], notice=f"Appliance error status: {enc['global_error'][1]}")


check_plugin_netbotz_enclosure = CheckPlugin(
    name="netbotz_enclosure",
    service_name="Enclosure %s",
    discovery_function=discover_netbotz_enclosure,
    check_function=check_netbotz_enclosure,
)
