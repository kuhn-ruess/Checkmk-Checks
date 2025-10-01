# 2021 created by Sven Rueß, sritd.de

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    Service,
    Result,
    State,
)


def parse_cohesity_alerts(string_table):
    section = {}
    for row in string_table:
        item = row[0][3:4] + ''.join(map(lambda x: x if x.islower() else " "+x, row[0][4:]))

        try:
            alerts = int(row[1])
        except ValueError:
            alerts = 0

        section[item] = alerts
    return section


agent_section_cohesity_alerts = AgentSection(
    name="cohesity_alerts",
    parse_function=parse_cohesity_alerts,
)


def discovery_cohesity_alerts(section):
    yield Service()

def check_cohesity_alerts(section):
    numCriticalAlerts = section['Critical Alerts']
    numWarningAlerts = section['Warning Alerts']
    numInfoAlerts = section['Info Alerts']

    text = f"{numCriticalAlerts} Critical {numWarningAlerts} Warning {numInfoAlerts} Info"

    stats=f"Alert stats:"
    for item in section:
        stats=f"{stats}\n{item} {section[item]}"

    if numCriticalAlerts > 0:
        state=State.CRIT
        text=f"Existing alerts: {text}"
    elif numWarningAlerts > 0:
        state=State.WARN
        text=f"Existing alerts: {text}"
    elif numInfoAlerts > 0:
        state=State.OK
        text=f"Info alerts: {text}"
    else:
        state=State.OK
        text=f"No alert: {text}"
    
    yield Result(
        state=state,
        summary=text,
        details=stats,
        )


check_plugin_cohesity_alerts = CheckPlugin(
    name="cohesity_alerts",
    service_name="Alert Status",
    discovery_function=discovery_cohesity_alerts,
    check_function=check_cohesity_alerts,
)

