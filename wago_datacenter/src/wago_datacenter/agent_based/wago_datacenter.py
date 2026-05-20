#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.agent_based.v2 import (
    CheckPlugin,
    OIDEnd,
    Result,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    State,
    startswith,
)


# Indices 1-3 are device info (ASP Name, Gerätename, Firmenname).
# Indices 5+ are configurable alarm/status signals.
_DEVICE_INFO_INDICES = {"1", "2", "3"}
_INDEX_TO_INFO_KEY = {"1": "asp_name", "2": "device_name", "3": "company"}

# Sub-OIDs inside a signal row:
#   .X.1 = description string (the controller may prefix it with one byte
#          that snmpwalk renders as a control character — we strip it)
#   .X.2 = numeric status code (1 = OK, anything else = fault)
_FIELD_DESCRIPTION = "1"
_FIELD_STATUS_CODE = "2"
_OK_STATUS_CODE = "1"


def _decode_value(raw: str) -> str:
    """Strip control bytes and collapse whitespace."""
    cleaned = "".join(c for c in raw if c.isprintable() or c == " ")
    return " ".join(cleaned.split())


def parse_wago_datacenter(string_table):
    """
    Returns:
        {
          "info": {"asp_name": str, "device_name": str, "company": str},
          "signals": {index: {"description": str, "status_code": str}},
        }

    Signals are keyed by the SNMP table index (not by description), because
    multiple indices can share the same description in the OK state (e.g.
    .15/.16/.17 all show "Notstrom") and the description changes when the
    device reports a fault. Keying by index keeps each signal as its own
    stable service.
    """
    parsed = {
        "info": {},
        "signals": {},
    }

    for oid_end, raw_value in string_table:
        parts = oid_end.split(".")
        value = _decode_value(raw_value)

        if len(parts) == 1:
            index = parts[0]
            if index in _DEVICE_INFO_INDICES and value:
                parsed["info"][_INDEX_TO_INFO_KEY[index]] = value
            continue

        if len(parts) == 2:
            index, field = parts
            entry = parsed["signals"].setdefault(
                index, {"description": "", "status_code": ""}
            )
            if field == _FIELD_DESCRIPTION:
                entry["description"] = value
            elif field == _FIELD_STATUS_CODE:
                entry["status_code"] = value

    return parsed


snmp_section_wago_datacenter = SimpleSNMPSection(
    name="wago_datacenter",
    parse_function=parse_wago_datacenter,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.13576.10.1.100.1.1",
        oids=[
            OIDEnd(),  # row index, e.g. "1", "2", "3" or "5.1", "5.2", ...
            "3",       # wioPlcDataWriteArea (description and status code)
        ],
    ),
    detect=startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.13576"),
)


def discover_wago_datacenter(section):
    for index, entry in section["signals"].items():
        description = entry["description"] or f"Signal {index}"
        yield Service(item=f"{index} {description}")


def check_wago_datacenter(item, section):
    index = item.split(" ", 1)[0]
    entry = section["signals"].get(index)
    if entry is None:
        yield Result(state=State.UNKNOWN, summary="Signal not found in SNMP data")
        return

    description = entry["description"] or f"Signal {index}"
    status_code = entry["status_code"]

    if status_code == _OK_STATUS_CODE:
        state = State.OK
        summary = f"OK: {description}"
    elif not status_code:
        state = State.UNKNOWN
        summary = f"No status code reported for {description}"
    else:
        state = State.CRIT
        summary = f"Status {status_code}: {description}"

    info = section.get("info", {})
    device_info = info.get("asp_name") or info.get("device_name", "")
    details = f"Device: {device_info}" if device_info else None

    yield Result(
        state=state,
        summary=summary,
        details=details,
    )


check_plugin_wago_datacenter = CheckPlugin(
    name="wago_datacenter",
    service_name="DC Signal %s",
    discovery_function=discover_wago_datacenter,
    check_function=check_wago_datacenter,
)
