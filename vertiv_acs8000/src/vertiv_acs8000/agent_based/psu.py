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
    startswith,
)


VERTIV_DETECT = startswith(".1.3.6.1.2.1.1.1.0", "Avocent ACS")


# PowerSupplyState enum from ACS8000-MIB.
# .1.3.6.1.4.1.10418.26.2.1.8.1.0 = acsPowerSupplyNumber  (count, not a state)
# .1.3.6.1.4.1.10418.26.2.1.8.2.0 = acsPowerSupplyStatePw1
# .1.3.6.1.4.1.10418.26.2.1.8.3.0 = acsPowerSupplyStatePw2
DEFAULT_STATE_NAMES = {
    "1": "powerOn",
    "2": "powerOff",
    "9999": "notInstalled",
}
DEFAULT_STATE_MAPPING = {
    "1": int(State.OK),
    "2": int(State.CRIT),
    "9999": int(State.WARN),
}


def parse_vertiv_acs8000_psu(string_table):
    if not string_table or not string_table[0]:
        return None
    row = string_table[0]
    try:
        count = int(row[0])
    except (ValueError, IndexError):
        count = None
    return {
        "count": count,
        "psus": {
            "PSU 1": row[1] if len(row) > 1 else "",
            "PSU 2": row[2] if len(row) > 2 else "",
        },
    }


def _unprefix(mapping):
    return {k.removeprefix("value_"): v for k, v in mapping.items()}


def discover_vertiv_acs8000_psu(section):
    if section and section["psus"]:
        yield Service()


def check_vertiv_acs8000_psu(params, section):
    state_names = {**DEFAULT_STATE_NAMES, **_unprefix(params.get("state_names", {}))}
    state_mapping = {**DEFAULT_STATE_MAPPING, **_unprefix(params.get("state_mapping", {}))}

    if section.get("count") is not None:
        yield Result(
            state=State.OK,
            summary=f"{section['count']} power supplies",
        )

    for psu_name, raw_state in section["psus"].items():
        if raw_state == "":
            continue
        label = state_names.get(raw_state, f"unknown({raw_state})")
        cmk_state = State(state_mapping.get(raw_state, int(State.UNKNOWN)))
        yield Result(
            state=cmk_state,
            summary=f"{psu_name}: {label}",
        )


snmp_section_vertiv_acs8000_psu = SimpleSNMPSection(
    name="vertiv_acs8000_psu",
    parse_function=parse_vertiv_acs8000_psu,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.10418.26.2.1.8",
        oids=[
            "1.0",  # acsPowerSupplyNumber
            "2.0",  # acsPowerSupplyStatePw1
            "3.0",  # acsPowerSupplyStatePw2
        ],
    ),
    detect=VERTIV_DETECT,
)


check_plugin_vertiv_acs8000_psu = CheckPlugin(
    name="vertiv_acs8000_psu",
    service_name="Vertiv ACS power supply",
    discovery_function=discover_vertiv_acs8000_psu,
    check_function=check_vertiv_acs8000_psu,
    check_ruleset_name="vertiv_acs8000_psu",
    check_default_parameters={},
)
