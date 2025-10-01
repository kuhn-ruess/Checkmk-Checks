# 2021 created by Sven Rueß, sritd.de

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    Metric,
    Service,
    Result,
    State,
    render,
)


def parse_cohesity_storage(string_table):
    section = {}
    for row in string_table:
        item = row[0]

        try:
            number = int(row[1])
        except ValueError:
            number = 0

        section[item] = number
    return section


agent_section_cohesity_storage_usage = AgentSection(
    name="cohesity_storage_usage",
    parse_function=parse_cohesity_storage,
)


def discovery_cohesity_storage(section):
    yield Service()

def check_cohesity_storage(params, section):
    levels = params.get("levels", ('fixed', (None, None)))
    warn, crit = levels[1]
    levels_pct = params.get("levels_pct", ('fixed', (None, None)))
    warn_pct, crit_pct = levels_pct[1]

    used_storage = None
    total_storage = None

    if "localUsageBytes" in section.keys():
        used_storage = section["localUsageBytes"]

    if "totalCapacityBytes" in section.keys():
        total_storage = section["totalCapacityBytes"]
    
    if used_storage is None or total_storage is None or total_storage == 0:
        yield Result(
            state=State.UNKNOWN,
            summary="No storage space data available",
        )
        return

    percent_used = used_storage * 100 / total_storage
    text = f"Disk used: {render.percent(percent_used)} ({render.disksize(used_storage)} of {render.disksize(total_storage)})"

    if None is not crit and used_storage >= crit:
        yield Result(
            state=State.CRIT,
            summary=text,
        )
    elif None is not crit_pct and percent_used >= crit_pct:
        yield Result(
            state=State.CRIT,
            summary=text,
        )
    elif None is not warn and used_storage >= warn:
        yield Result(
            state=State.WARN,
            summary=text,
        )
    elif None is not warn_pct and percent_used >= warn_pct:
        yield Result(
            state=State.WARN,
            summary=text,
        )
    else:
        yield Result(
            state=State.OK,
            summary=text,
        )

    yield Metric(name="used_storage", value=used_storage, levels=(warn, crit), boundaries=(0, total_storage))
    yield Metric(name="percent_used", value=percent_used, levels=(warn_pct, crit_pct), boundaries=(0, 100))

check_plugin_cohesity_storage_usage = CheckPlugin(
    name="cohesity_storage_usage",
    service_name="Storage Status",
    discovery_function=discovery_cohesity_storage,
    check_function=check_cohesity_storage,
    check_default_parameters={},
    check_ruleset_name="cohesity_storage",
)

