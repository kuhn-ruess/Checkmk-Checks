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


def _decode_value(raw: str) -> str:
    """Normalize value string - strip whitespace and collapse internal whitespace."""
    return " ".join(raw.split())


def parse_wago_datacenter(string_table):
    """
    Returns:
        {
          "info": {"asp_name": str, "device_name": str, "company": str},
          "signals": {index: full_value},
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

    index_to_info_key = {"1": "asp_name", "2": "device_name", "3": "company"}

    for index, raw_value in string_table:
        value = _decode_value(raw_value)
        if not value:
            continue

        if index in _DEVICE_INFO_INDICES:
            parsed["info"][index_to_info_key[index]] = value
            continue

        parsed["signals"][index] = value

    return parsed


snmp_section_wago_datacenter = SimpleSNMPSection(
    name="wago_datacenter",
    parse_function=parse_wago_datacenter,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.13576.10.1.100.1.1",
        oids=[
            OIDEnd(),  # table instance (1, 2, 3, 5, 6, ... 19)
            "3",       # wioPlcDataWriteArea (message string)
        ],
    ),
    detect=startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.13576"),
)


def _signal_description(value: str) -> str:
    """Extract description from "<status_word> <description>" payload."""
    parts = value.split(" ", 1)
    if len(parts) == 2:
        return parts[1].strip()
    return value.strip()


def discover_wago_datacenter(section):
    for index, value in section["signals"].items():
        description = _signal_description(value) or f"Signal {index}"
        yield Service(item=f"{index} {description}")


def check_wago_datacenter(item, section):
    index = item.split(" ", 1)[0]
    if index not in section["signals"]:
        yield Result(state=State.UNKNOWN, summary="Signal not found in SNMP data")
        return

    value = section["signals"][index]
    status_word = value.split()[0] if value.split() else ""

    if status_word == "OK":
        state = State.OK
    else:
        state = State.CRIT

    info = section.get("info", {})
    device_info = info.get("asp_name") or info.get("device_name", "")
    details = f"Device: {device_info}" if device_info else ""

    yield Result(
        state=state,
        summary=value,
        details=details if details else None,
    )


check_plugin_wago_datacenter = CheckPlugin(
    name="wago_datacenter",
    service_name="DC Signal %s",
    discovery_function=discover_wago_datacenter,
    check_function=check_wago_datacenter,
)
