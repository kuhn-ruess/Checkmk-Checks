# 2021 Created by Sven Rueß, sritd.de


from .agent_based_api.v1 import (
    register,
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


register.agent_section(
    name="cohesity_storage_usage",
    parse_function=parse_cohesity_storage,
)


def discovery_cohesity_storage(section):
    yield Service()

def check_cohesity_storage(params, section):
    (warn, crit) = params.get("levels", (None, None))
    used_storage = None
    total_storage = None

    if "localUsageBytes" in section.keys():
        used_storage = section["localUsageBytes"]

    if "totalCapacityBytes" in section.keys():
        total_storage = section["totalCapacityBytes"]

    percent_used = used_storage * 100 / total_storage
    text = f"Disk used: {render.percent(percent_used)} ({render.disksize(used_storage)} of {render.disksize(total_storage)})"

    if None is not crit and used_storage >= crit:
        yield Result(
            state=State.CRIT,
            summary=text,
        )
    elif None is not warn and used_storage >= warn:
        yield Result(
            state=State.WARN,
            summary=text,
        )
    else:
        yield Result(
            state=State.OK,
            summary=text,
        )


register.check_plugin(
    name="cohesity_storage_usage",
    service_name="Storage Status",
    discovery_function=discovery_cohesity_storage,
    check_function=check_cohesity_storage,
    check_default_parameters={},
    check_ruleset_name="cohesity_storage",
)
