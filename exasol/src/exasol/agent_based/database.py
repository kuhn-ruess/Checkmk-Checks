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
    check_levels,
    Result,
    State,
)
from cmk.agent_based.v2.render import (
    bytes,
    percent,
)

from .utils.exasol import (
    parse_exasol_database,
    discover_exasol_database,
)


agent_section_exasol_database = AgentSection(
    name = "exasol_database",
    parse_function = parse_exasol_database,
)


def check_exasol_database(item, params, section):
    if item not in section.keys():
        yield Result(state=State.UNKNOWN, summary="Item not fund")

    else:
        data = section[item]
        usage = float(data['usage']) * 1024 * 1024 * 1024
        free = float(data['free']) * 1024 * 1024 * 1024
        total = free + usage
        usage_perc = round((usage/total) * 100.0, 2)

        if "absolute" == params["levels"][0]:
            yield from check_levels(
                value = usage,
                levels_upper = params["levels"][1],
                metric_name = "exasol_db_size",
                render_func = lambda v: bytes(v),
                label = "Exasol database size",
            )

        elif "percentage" == params["levels"][0]:
            yield from check_levels(
                value = usage_perc,
                levels_upper = params["levels"][1],
                metric_name = "exasol_db_size_perc",
                render_func = lambda v: percent(v),
                label = "Exasol database size percentage",
                boundaries = (0, 100),
            )


check_plugin_exasol_database = CheckPlugin(
    name= "exasol_database",
    sections = ["exasol_database"],
    service_name = "Database %s usage",
    discovery_function = discover_exasol_database,
    check_function = check_exasol_database,
    check_ruleset_name = "exasol_database",
    check_default_parameters = {
        "levels": ('absolute', ('fixed', (1024 * 1024 * 1024, 2 * 1024 * 1024 * 1024)))
    },
)
