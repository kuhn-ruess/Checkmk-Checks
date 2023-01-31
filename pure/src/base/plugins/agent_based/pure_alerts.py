# 2021 created by Sven Rueß, sritd.de
# 2023 reworked by Carlo Kleinloog

from .agent_based_api.v1 import (
    register,
    Service,
    Result,
    State,
)


def parse_pure_alerts(string_table):
    section = {
        "crit": 0,
        "warn": 0,
        "info": 0,
        "error": '',
    }

    if not string_table:
        return section

    for row in string_table:
        if row[0].startswith("error"):
            section["error"] += ", ".join(row[1:])
        elif row[0].startswith("critical"):
            section["crit"] = int(row[1])
        elif row[0].startswith("warning"):
            section["warn"] = int(row[1])
        elif row[0].startswith("info"):
            section["info"] = int(row[1])

    return section


register.agent_section(
    name="pure_fa_errors",
    parse_function=parse_pure_alerts,
)


def discovery_pure_alerts(section):
    yield Service()

def check_pure_alerts(section):
    if len(section["error"]) > 0:
        yield Result(
            state=State.UNKNOWN,
            summary=f"UNKN: {section['error']}",
        )
    elif section["crit"] > 0:
        yield Result(
            state=State.CRIT,
            summary=f"CRIT: {section['crit']} critical alerts",
        )
    elif section["warn"] > 0:
        yield Result(
            state=State.WARN,
            summary=f"WARN: {section['warn']} warning alerts",
        )
    else:
        yield Result(
            state=State.OK,
            summary=f"OK: {section['info']} informational alerts",
        )


register.check_plugin(
    name="pure_fa_errors",
    service_name="Alerts",
    discovery_function=discovery_pure_alerts,
    check_function=check_pure_alerts,
)
