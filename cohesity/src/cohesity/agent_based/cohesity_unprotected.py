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


def parse_cohesity_unprotected(string_table):
    section = {}

    for row in string_table:
        item = row[0]

        try:
            number = int(row[1])
        except ValueError:
            number = 0

        section[item] = number
    return section


agent_section_cohesity_unprotected = AgentSection(
    name="cohesity_unprotected",
    parse_function=parse_cohesity_unprotected,
)


def discovery_cohesity_unprotected(section):
    yield Service()

def check_cohesity_unprotected(section):
    failed = []

    if section["numObjectsUnprotected"] > 0:
        yield Result(
            state=State.CRIT,
            summary=f"Number of unprotected objects: {section['numObjectsUnprotected']}",
            details=f"Size of protected objects: {render.bytes(section['protectedSizeBytes'])}"
        )
    else:
        yield Result(
            state=State.OK,
            summary=f"There are no unprotected objects",
            details=f"Size of protected objects: {render.bytes(section['protectedSizeBytes'])}"
        )

    yield Metric(name="unprotected_objects", value=section["numObjectsUnprotected"])

check_plugin_cohesity_unprotected = CheckPlugin(
    name="cohesity_unprotected",
    service_name="Unproteced Status",
    discovery_function=discovery_cohesity_unprotected,
    check_function=check_cohesity_unprotected,
)

