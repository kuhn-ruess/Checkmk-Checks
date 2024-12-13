# 2021 created by Sven Rueß, sritd.de

from .agent_based_api.v1 import (
    Metric,
    register,
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


register.agent_section(
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

register.check_plugin(
    name="cohesity_unprotected",
    service_name="Unproteced Status",
    discovery_function=discovery_cohesity_unprotected,
    check_function=check_cohesity_unprotected,
)

