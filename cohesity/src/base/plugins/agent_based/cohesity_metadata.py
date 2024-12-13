# 2021 created by Sven Rueß, sritd.de

from .agent_based_api.v1 import (
    Metric,
    register,
    Service,
    Result,
    State,
    render,
)


def parse_cohesity_metadata(string_table):
    section = {}
    for row in string_table:
        item = row[0]
        
        try:
            number = float(row[1])
        except ValueError:
            number = 0

        section[item] = number
    return section


register.agent_section(
    name="cohesity_metadata_usage",
    parse_function=parse_cohesity_metadata,
)


def discovery_cohesity_metadata(section):
    yield Service()

def check_cohesity_metadata(params, section):
    (warn_pct, crit_pct) = params.get("levels %", (None, None))
    used_metadata_space_pct = None
    avail_metadata_space = None

    if "usedMetadataSpacePct" in section.keys():
        used_metadata_space_pct = section["usedMetadataSpacePct"]

    if "availableMetadataSpace" in section.keys():
        avail_metadata_space = section["availableMetadataSpace"]

    text = f"Metadata space used: {render.percent(used_metadata_space_pct)} ({render.disksize(avail_metadata_space)} available)"

    if None is not crit_pct and used_metadata_space_pct >= crit_pct:
        yield Result(
            state=State.CRIT,
            summary=text,
        )
    elif None is not warn_pct and used_metadata_space_pct >= warn_pct:
        yield Result(
            state=State.WARN,
            summary=text,
        )
    else:
        yield Result(
            state=State.OK,
            summary=text,
        )

    yield Metric(name="used_metadata_space_pct", value=used_metadata_space_pct, levels=(warn_pct, crit_pct), boundaries=(0, 100))
    yield Metric(name="avail_metadata_space", value=avail_metadata_space)

register.check_plugin(
    name="cohesity_metadata_usage",
    service_name="Metadata Status",
    discovery_function=discovery_cohesity_metadata,
    check_function=check_cohesity_metadata,
    check_default_parameters={},
    check_ruleset_name="cohesity_metadata",
)

