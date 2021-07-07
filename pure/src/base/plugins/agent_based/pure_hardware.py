# 2021 created by Sven Rueß, sritd.de

from .agent_based_api.v1 import (
    register,
    Service,
    Result,
    State,
)


def parse_pure_hardware(string_table):
    section = {}
    for row in string_table:
        (item, status, serial)  = row

        if serial == "None":
            serial = None

        section[item] = {
            'status': status.lower(),
            'serial': serial,
        }
    return section


register.agent_section(
    name="pure_hardware",
    parse_function=parse_pure_hardware,
)


def discovery_pure_hardware(section):
    for item in section.keys():
        yield Service(item=item)

def check_pure_hardware(item, section):
    failed = []

    if item not in section.keys():
        yield Result(
            state=State.UNKN,
            summary=f"Item {item} not found",
        )

    if section[item]['status'].lower() == 'ok':
        yield Result(
            state=State.OK,
            summary=f"OK, Serial: {section[item]['serial']}" if section[item]["serial"] else f"OK",
        )
    else:
        yield Result(
            state=State.CRIT,
            summary=f"CRIT, Serial: {section[item]['serial']}" if section[item]["serial"] else f"CRIT",
        )


register.check_plugin(
    name="pure_hardware",
    service_name="Hardware %s",
    discovery_function=discovery_pure_hardware,
    check_function=check_pure_hardware,
)

