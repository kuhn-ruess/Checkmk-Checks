# 2021 Created by Sven Rueß, sritd.de


from .agent_based_api.v1 import (
    register,
    Service,
    Result,
    State,
)


def parse_cohesity_alerts(string_table):
    section = {}
    for row in string_table:
        item = ''.join(map(lambda x: x if x.islower() else " "+x, row[0][3:]))

        try:
            alerts = int(row[1])
        except ValueError:
            alerts = 0

        section[item] = alerts
    return section


register.agent_section(
    name="cohesity_alerts",
    parse_function=parse_cohesity_alerts,
)


def discovery_cohesity_alerts(section):
    yield Service()

def check_cohesity_alerts(section):
    failed = []

    for item in section:
        if section[item] > 0:
            failed.append(item)

    if len(failed) > 0:
        yield Result(
            state=State.CRIT,
            summary=f"{len(failed)} existing alerts",
            details=f"Existing alerts: {', '.join(failed)}"
        )
    else:
        yield Result(
            state=State.OK,
            summary=f"There are no alarms"
        )


register.check_plugin(
    name="cohesity_alerts",
    service_name="Alert Status",
    discovery_function=discovery_cohesity_alerts,
    check_function=check_cohesity_alerts,
)
