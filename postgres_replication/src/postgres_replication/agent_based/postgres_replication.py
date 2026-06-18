#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from collections.abc import Mapping

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Result,
    Service,
    State,
    StringTable,
    check_levels,
    render,
)


Section = Mapping[str, list]


def parse_postgres_replication(string_table: StringTable) -> Section:
    """
    Parse the agent output of the postgres_replication plugin.

    One line per replication slot:
        slot_name slot_type slot_lsn delta active [delta_pretty] [unit]
    """
    section: dict[str, list] = {}
    for line in string_table:
        if not line:
            continue
        section[line[0]] = line
    return section


def discover_postgres_replication(section: Section) -> DiscoveryResult:
    """One service per replication slot."""
    for slot_name in section:
        yield Service(item=slot_name)


def check_postgres_replication(item: str, params: Mapping, section: Section) -> CheckResult:
    line = section.get(item)
    if line is None:
        return

    # Pad the line so optional trailing columns (delta_pretty, unit) are safe.
    fields = list(line) + [""] * (7 - len(line))
    slot_name, slot_type, slot_lsn, delta, active, delta_pretty, unit = fields[:7]

    yield Result(state=State.OK, summary="Slot Type: " + slot_type)
    yield Result(state=State.OK, summary="LSN " + slot_lsn)

    if active != "t":
        yield Result(state=State.CRIT, summary="Status inactive")

    if unit == "bytes":
        yield from check_levels(
            int(delta_pretty),
            levels_upper=params["levels"],
            metric_name="bytes",
            label="Usage",
            render_func=render.bytes,
        )


agent_section_postgres_replication = AgentSection(
    name="postgres_replication",
    parse_function=parse_postgres_replication,
)


check_plugin_postgres_replication = CheckPlugin(
    name="postgres_replication",
    service_name="PostgreSQL Replication %s",
    discovery_function=discover_postgres_replication,
    check_function=check_postgres_replication,
    check_ruleset_name="postgres_replication",
    check_default_parameters={"levels": ("fixed", (31457280, 62914560))},
)
