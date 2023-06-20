#2021 created by Sven Rueß, sritd.de
#/omd/sites/BIS/local/lib/python3/cmk/base/plugins/agent_based/
from .agent_based_api.v1 import (
    register,
    Service,
    Result,
    State,
    render,
)


def parse_pure_drives(string_table):
    section = {}
    for row in string_table:
        (item, status, serial, kind, capacity)  = row

        try:
            capacity = int(capacity)
        except ValueError:
            capacity = 0

        section[item] = {
            'status': status.lower(),
            'type': kind,
            'capacity': capacity,
            'serial': serial,
        }
    return section


register.agent_section(
    name="pure_drives",
    parse_function=parse_pure_drives,
)

def discovery_pure_drives(section):
    for item in section.keys():
        yield Service(item=item)

def check_pure_drives(item, section):
    failed = []

    if item not in section.keys():
        yield Result(
            state=State.UNKNOWN,
            summary=f"Item {item} not found",
        )

    data = section[item]
    txt = f"Storage type: {data['type']}, Serial: {data['serial']}, Capacity: {render.bytes(data['capacity'])}"
    if section[item]['status'].lower() == 'healthy':
        yield Result(
            state=State.OK,
            summary=f"OK, {txt}",
        )
    else:
        yield Result(
            state=State.CRIT,
            summary=f"CRIT, Status: {section[item]['status']}, {txt}",
        )


register.check_plugin(
    name="pure_drives",
    service_name="Drive %s",
    discovery_function=discovery_pure_drives,
    check_function=check_pure_drives,
)
