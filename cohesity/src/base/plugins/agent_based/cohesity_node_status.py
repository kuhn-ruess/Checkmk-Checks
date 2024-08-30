# 2021 created by Sven Rueß, sritd.de

from .agent_based_api.v1 import (
    register,
    Service,
    Result,
    State,
)


def parse_cohesity_node_status(string_table):
    section = {}
    for row in string_table:
        item = row[0]
        section.setdefault(item, {})

        status = row[1]
        services = []
        if row[2:]:
            services = (row[2:][0]).split(',')
        section[item][status] = services
    return section


register.agent_section(
    name="cohesity_node_status",
    parse_function=parse_cohesity_node_status,
)


def discovery_cohesity_node_status(section):
    for node in section.keys():
        yield Service(item=node)

def check_cohesity_node_status(item, params, section):
    services = params.get('services', [])

    if item in section.keys():
        for service in services:
            if service in section[item]['ok']:
                section[item]['ok'].remove(service)

            if service in section[item]['failed']:
                section[item]['failed'].remove(service)

        if "ok" in section[item] and len(section[item]["ok"]):
            yield Result(
                state=State.OK,
                summary=f"{len(section[item]['ok']) } Services are OK",
                details=f"Services OK: {', '.join(section[item]['ok'])}"
            )

        if "failed" in section[item] and len(section[item]["failed"]):
            yield Result(
                state=State.CRIT,
                summary=f"{len(section[item]['failed'])} Services are failed",
                details=f"Services FAILED: {', '.join(section[item]['failed'])}"
            )


register.check_plugin(
    name="cohesity_node_status",
    service_name="Node Status %s",
    discovery_function=discovery_cohesity_node_status,
    check_function=check_cohesity_node_status,
    check_default_parameters={},
    check_ruleset_name="cohesity_node_status",
)

