#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from time import mktime, strptime

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    Result,
    State,
)

from .utils.exasol import (
    parse_exasol_database,
    discover_exasol_database,
)


agent_section_exasol_database = AgentSection(
    name = "exasol_database_backup",
    parse_function = parse_exasol_database,
)


def check_exasol_database_backup(item, section):
    if item not in section.keys():
        yield Result(state=State.UNKNOWN, summary="Item not fund")

    else:
        data = section[item]

        if "backups" not in data.keys():
            yield Result(state=State.CRIT, summary="No valid Backup found")

        else:
            for last_id, backup in enumerate(data["backups"][1:]):
                if data["backups"][last_id] < backup:
                    yield Result(state=State.WARN, summary="Remote Base Backup expires before its dependency")

            yield Result(state=State.OK, summary="Valid Backup found")


check_plugin_exasol_database_backup = CheckPlugin(
    name= "exasol_database_backup",
    sections = ["exasol_database"],
    service_name = "Database %s backup",
    discovery_function = discover_exasol_database,
    check_function = check_exasol_database_backup,
)
