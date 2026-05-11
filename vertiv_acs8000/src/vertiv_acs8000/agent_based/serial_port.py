#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from time import time

from cmk.agent_based.v2 import (
    CheckPlugin,
    GetRateError,
    Result,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    State,
    check_levels,
    get_rate,
    get_value_store,
    render,
    startswith,
)


VERTIV_DETECT = startswith(".1.3.6.1.2.1.1.1.0", "Avocent ACS")


# acsSerialPortTable column 23 — connection state. Observed in the field:
# 1 = session active, 2 = idle. Override via the ruleset if a different
# firmware exposes other values.
DEFAULT_CONN_STATE_NAMES = {
    "1": "active",
    "2": "idle",
}
DEFAULT_CONN_STATE_MAPPING = {
    "1": int(State.OK),
    "2": int(State.OK),
}


def parse_vertiv_acs8000_serial_port(string_table):
    if not string_table:
        return None
    ports = {}
    for row in string_table:
        port_id, tty_name, alias, baud, tx_bytes, rx_bytes, conn_state = row
        if not port_id:
            continue
        item = alias.strip() if alias and alias.strip() else f"Port {port_id}"
        ports[item] = {
            "port_id": port_id,
            "tty_name": tty_name,
            "alias": alias,
            "baud": baud,
            "tx_bytes": _to_int(tx_bytes),
            "rx_bytes": _to_int(rx_bytes),
            "conn_state": conn_state,
        }
    return ports


def _to_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def _unprefix(mapping):
    return {k.removeprefix("value_"): v for k, v in mapping.items()}


def discover_vertiv_acs8000_serial_port(section):
    for item in section:
        yield Service(item=item)


def check_vertiv_acs8000_serial_port(item, params, section):
    port = section.get(item)
    if port is None:
        return

    state_names = {**DEFAULT_CONN_STATE_NAMES, **_unprefix(params.get("state_names", {}))}
    state_mapping = {**DEFAULT_CONN_STATE_MAPPING, **_unprefix(params.get("state_mapping", {}))}

    conn_label = state_names.get(port["conn_state"], f"unknown({port['conn_state']})")
    cmk_state = State(state_mapping.get(port["conn_state"], int(State.UNKNOWN)))
    yield Result(
        state=cmk_state,
        summary=f"Connection: {conn_label}",
        details=(
            f"Port ID: {port['port_id']}\n"
            f"TTY: {port['tty_name']}\n"
            f"Alias: {port['alias']}\n"
            f"Baud rate: {port['baud']}"
        ),
    )

    now = time()
    value_store = get_value_store()
    for direction, key in (("TX", "tx_bytes"), ("RX", "rx_bytes")):
        absolute = port[key]
        if absolute is None:
            continue
        try:
            rate = get_rate(value_store, f"{item}.{key}", now, absolute, raise_overflow=True)
        except GetRateError:
            continue
        yield from check_levels(
            value=rate,
            levels_upper=params.get(f"{key}_rate"),
            metric_name=f"{key}_rate",
            label=f"{direction} rate",
            render_func=render.iobandwidth,
        )


snmp_section_vertiv_acs8000_serial_port = SimpleSNMPSection(
    name="vertiv_acs8000_serial_port",
    parse_function=parse_vertiv_acs8000_serial_port,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.10418.26.2.3.2.1",
        oids=[
            "1",   # portID
            "2",   # tty name (ttyS1 …)
            "4",   # alias / display name
            "7",   # baud rate
            "16",  # TX byte counter
            "17",  # RX byte counter
            "23",  # connection state
        ],
    ),
    detect=VERTIV_DETECT,
)


check_plugin_vertiv_acs8000_serial_port = CheckPlugin(
    name="vertiv_acs8000_serial_port",
    service_name="Vertiv ACS port %s",
    discovery_function=discover_vertiv_acs8000_serial_port,
    check_function=check_vertiv_acs8000_serial_port,
    check_ruleset_name="vertiv_acs8000_serial_port",
    check_default_parameters={},
)
