# 2021 created by Sven Rueß, sritd.de
# 2023 reworked by Carlo Kleinloog
#/omd/sites/BIS/local/lib/python3/cmk/base/plugins/agent_based

from .agent_based_api.v1 import (
    register,
    Service,
    Result,
    State,
)


def parse_pure_array(string_table):
    section = {}
    for row in string_table:
        (item, version, revision, id)  = row

        section[item] = {
            'version': version,
            'revision': revision,
            'id': id,
        }
    return section


register.agent_section(
    name="pure_array",
    parse_function=parse_pure_array,
)

def discovery_pure_array(section):
    for item in section.keys():
        yield Service(item=item)

def check_pure_array(item, section):
    failed = []

    if item not in section.keys():
        yield Result(
            state=State.UNKNOWN,
            summary=f"Item {item} not found",
        )

    data = section[item]
    if item not in section.keys():
        yield Result(
            state=State.CRIT,
            summary=f"CRIT, Storage OS: Purity, Software version: {data['version']}",
            details=f"Software revision: {data['revision']}, Array ID: {data['id']}",
        )
    else:
        yield Result(
            state=State.OK,
            summary=f"OK, Storage OS: Purity, Software version: {data['version']}",
            details=f"Software revision: {data['revision']}, Array ID: {data['id']}",
        )


register.check_plugin(
    name="pure_array",
    service_name="Array %s",
    discovery_function=discovery_pure_array,
    check_function=check_pure_array,
)
