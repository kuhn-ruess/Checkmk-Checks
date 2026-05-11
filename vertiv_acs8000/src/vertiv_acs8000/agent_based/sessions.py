#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.agent_based.v2 import (
    CheckPlugin,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    check_levels,
    startswith,
)


VERTIV_DETECT = startswith(".1.3.6.1.2.1.1.1.0", "Avocent ACS")


def parse_vertiv_acs8000_sessions(string_table):
    if not string_table or not string_table[0]:
        return None
    try:
        return int(string_table[0][0])
    except (ValueError, IndexError):
        return None


def discover_vertiv_acs8000_sessions(section):
    yield Service()


def check_vertiv_acs8000_sessions(params, section):
    yield from check_levels(
        value=section,
        levels_upper=params.get("levels"),
        metric_name="sessions",
        label="Active sessions",
        render_func=lambda v: f"{int(v)}",
    )


snmp_section_vertiv_acs8000_sessions = SimpleSNMPSection(
    name="vertiv_acs8000_sessions",
    parse_function=parse_vertiv_acs8000_sessions,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.10418.26.2.2",
        oids=["1.0"],  # acsActiveSessionsNumberOfSession
    ),
    detect=VERTIV_DETECT,
)


check_plugin_vertiv_acs8000_sessions = CheckPlugin(
    name="vertiv_acs8000_sessions",
    service_name="Vertiv ACS active sessions",
    discovery_function=discover_vertiv_acs8000_sessions,
    check_function=check_vertiv_acs8000_sessions,
    check_ruleset_name="vertiv_acs8000_sessions",
    check_default_parameters={"levels": ("no_levels", None)},
)
