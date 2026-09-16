#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.agent_based.v2 import (
    check_levels,
    CheckPlugin,
    Metric,
    render,
    Result,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    State,
)

from .ts4300_lib import DETECT_TS4300

LOCATION_TYPE = {
    "2": "Storage",
    "3": "Magazine",
    "6": "I/O station",
}


def parse_ibm_ts4300_slots(string_table):
    """Count media locations per type and collect the cleaning cartridges."""
    locations = {}
    cleaning = []

    for location_type, media_present, cleaner, label in string_table:
        group = LOCATION_TYPE.get(location_type)
        if not group:
            continue

        counters = locations.setdefault(group, {"total": 0, "used": 0})
        counters["total"] += 1
        if media_present == "1":
            counters["used"] += 1
            if cleaner == "1":
                cleaning.append((label, group))

    return {
        "locations": locations,
        "cleaning": cleaning,
    }


def discover_ibm_ts4300_slots(section):
    """Discovery, the I/O station is informational by default."""
    for group in section["locations"]:
        if group == "I/O station":
            yield Service(item=group, parameters={"levels_used": ("no_levels", None)})
        else:
            yield Service(item=group)


def check_ibm_ts4300_slots(item, params, section):
    """Check"""
    if not (counters := section["locations"].get(item)):
        return

    total = counters["total"]
    used = counters["used"]

    yield from check_levels(
        100.0 * used / total,
        levels_upper=params["levels_used"],
        metric_name="tape_slots_utilization",
        label="Used",
        render_func=render.percent,
        boundaries=(0.0, 100.0),
    )
    yield Result(state=State.OK, summary=f"{used} of {total} slots, {total - used} free")
    yield Metric("tape_slots_used", used, boundaries=(0, total))
    yield Metric("tape_slots_free", total - used, boundaries=(0, total))


def discover_ibm_ts4300_cleaning(section):
    """Discovery"""
    if section["locations"]:
        yield Service()


def check_ibm_ts4300_cleaning(params, section):
    """Check"""
    cleaning = section["cleaning"]

    yield from check_levels(
        len(cleaning),
        levels_lower=params["levels_cartridges"],
        metric_name="tape_cleaning_cartridges",
        label="Cartridges",
        render_func=lambda v: f"{int(v)}",
    )

    for label, group in cleaning:
        yield Result(state=State.OK, notice=f"{label} in {group}")


snmp_section_ibm_ts4300_slots = SimpleSNMPSection(
    name = "ibm_ts4300_slots",
    parse_function = parse_ibm_ts4300_slots,
    fetch = SNMPTree(
        base = ".1.3.6.1.4.1.14851.3.1.13.3.1",
        oids = [
            '3',
            '10',
            '17',
            '19',
        ],
    ),
    detect = DETECT_TS4300,
)

check_plugin_ibm_ts4300_slots = CheckPlugin(
    name = "ibm_ts4300_slots",
    service_name = "Slots %s",
    discovery_function = discover_ibm_ts4300_slots,
    check_function = check_ibm_ts4300_slots,
    check_default_parameters = {
        "levels_used": ("fixed", (90.0, 95.0)),
    },
    check_ruleset_name = "ibm_ts4300_slots",
)

check_plugin_ibm_ts4300_cleaning = CheckPlugin(
    name = "ibm_ts4300_cleaning",
    sections = ["ibm_ts4300_slots"],
    service_name = "Cleaning Cartridges",
    discovery_function = discover_ibm_ts4300_cleaning,
    check_function = check_ibm_ts4300_cleaning,
    check_default_parameters = {
        "levels_cartridges": ("fixed", (1, 1)),
    },
    check_ruleset_name = "ibm_ts4300_cleaning",
)
