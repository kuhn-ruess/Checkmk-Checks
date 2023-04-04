# 2021 created by Sven Rueß, sritd.de
#/omd/sites/BIS/local/lib/python3/cmk/base/plugins/agent_based/
from .agent_based_api.v1 import (
    register,
    Service,
    Result,
    State,
    get_value_store,
)

from .utils.temperature import (
    check_temperature,
    TempParamType,
    to_celsius,
)

def parse_pure_hardware(string_table):
    section = {}
    for row in string_table:
        (item, status, serial, speed, temp, voltage, slot)  = row

        if serial == "None":
            serial = None

        section[item] = {
            'status': status.lower(),
            'voltage': voltage,
            'slot': slot,
        }
        if temp != "None":
            section[item]['temperature'] = int(temp)
        elif 'ETH' in item:
            # is Network
            section[item]['nw_speed'] = int(speed)
        elif "FAN" in item:
            section[item]['FAN'] = True
        else:
            section[item]['default'] = True
    return section


register.agent_section(
    name="pure_hardware",
    parse_function=parse_pure_hardware,
)


def discovery_pure_hardware(section):
    for item, data in section.items():
        if 'default' in data:
            yield Service(item=item)

def check_pure_hardware(item, section):

    if item not in section.keys():
        yield Result(
            state=State.UNKNOWN,
            summary=f"Item {item} not found",
        )

    data = section[item]
    if data['status'].lower() == 'ok':
        state = State.OK
    else:
        state = State.CRIT

    yield Result(
        state=state,
        summary=f"Device State: {data['status']}"
    )


register.check_plugin(
    name="pure_hardware",
    service_name="Hardware %s",
    discovery_function=discovery_pure_hardware,
    check_function=check_pure_hardware,
)

def discovery_pure_hardware_temp(section):
    for item, data in section.items():
        if 'temperature' in data:
            yield Service(item=item)

def check_pure_hardware_temp(item, params, section):
    value = int(section[item]['temperature'])

    yield from check_temperature(
        value,
        params,
        unique_name="pure_hardware_temp.%s" % item,
        value_store=get_value_store(),
    )

register.check_plugin(
    name="pure_hardware_temperature",
    sections=['pure_hardware'],
    service_name="Temperature %s",
    discovery_function=discovery_pure_hardware_temp,
    check_function=check_pure_hardware_temp,
    check_default_parameters={},
    check_ruleset_name='temperature',
)

def discovery_pure_hardware_fan(section):
    for item, data in section.items():
        if 'FAN' in data:
            yield Service(item=item)

def check_pure_hardware_fan(item, section):
    data = section[item]

    if data['status'].lower() == 'ok':
        state = State.OK
    else:
        state = State.CRIT
    yield Result(
        state=state,
        summary=f"FAN State: {data['status']}"
    )


register.check_plugin(
    name="pure_hardware_fan",
    sections=['pure_hardware'],
    service_name="FAN %s",
    discovery_function=discovery_pure_hardware_fan,
    check_function=check_pure_hardware_fan,
)
def discovery_pure_hardware_nw(section):
    for item, data in section.items():
        if 'nw_speed' in data:
            yield Service(item=item)

def check_pure_hardware_nw(item, section):
    data = section[item]

    if data['status'].lower() == 'ok':
        state = State.OK
    else:
        state = State.CRIT
    yield Result(
        state=state,
        summary=f"Interface State: {data['status']}"
    )


register.check_plugin(
    name="pure_hardware_nw",
    sections=['pure_hardware'],
    service_name="Interface %s",
    discovery_function=discovery_pure_hardware_nw,
    check_function=check_pure_hardware_nw,
)
