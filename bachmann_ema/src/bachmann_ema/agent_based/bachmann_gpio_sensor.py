#!/usr/bin/python
"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
from cmk.agent_based.v2 import (
        SNMPSection,
        CheckPlugin,
        OIDEnd,
        Service,
        ServiceLabel,
        SNMPTree,
        State,
        Result,
        startswith,
)

# BlueNet2 sensor types (bluenet2SensorType)
GPIO_TYPES = {
    ".1.3.6.1.4.1.31770.2.1.8.3": "external",
    ".1.3.6.1.4.1.31770.2.1.8.16": "internal",
}

ENTITY_STATES = {
    '0': ('expected', State.OK),
    '1': ('undefined', State.UNKNOWN),
    '2': ('ok', State.OK),
    '3': ('errorHigh', State.CRIT),
    '4': ('errorLow', State.CRIT),
    '5': ('warningHigh', State.WARN),
    '6': ('warningLow', State.WARN),
    '7': ('lost', State.CRIT),
    '8': ('deactivate', State.WARN),
    '11': ('onAlarm', State.CRIT),
    '12': ('offAlarm', State.CRIT),
    '15': ('onWarning', State.WARN),
    '16': ('offWarning', State.WARN),
    '19': ('on', State.OK),
    '20': ('off', State.CRIT),
    '21': ('onChildAlarm', State.CRIT),
    '22': ('offChildAlarm', State.CRIT),
    '23': ('onChildWarning', State.WARN),
    '24': ('offChildWarning', State.WARN),
    '25': ('childAlarm', State.CRIT),
    '26': ('childWarning', State.WARN),
    '27': ('lostChild', State.CRIT),
    '36': ('updateInProgress', State.WARN),
    '37': ('updateError', State.CRIT),
    '41': ('alarm', State.CRIT),
    '42': ('warning', State.WARN),
    '43': ('ok', State.OK),
    '44': ('disabled', State.WARN),
    '45': ('fwVersionTooNew', State.WARN),
}


def parse_gpio_sensor(string_table):
    """
    Parse function

    Joins the BlueNet2 device table (Master/Slave PDUs) with the sensor table
    and keeps the GPIO sensors only.
    """
    devices, sensors = string_table
    device_names = {}
    for index, name, friendly_name in devices:
        device_names[index] = (name or f"Device {index}", friendly_name)

    out = {}
    for index, name, friendly_name, type_oid, state in sensors:
        sensor_type = GPIO_TYPES.get(type_oid)
        if not sensor_type:
            if not name.startswith("GPIO"):
                continue
            sensor_type = "internal" if "Internal" in name else "external"

        device_index = index.split(".")[0]
        device_name, device_friendly_name = device_names.get(device_index,
                                                             (f"Device {device_index}", ""))
        out[f"{device_name} {name}"] = {
            'type': sensor_type,
            'friendly_name': friendly_name,
            'device_friendly_name': device_friendly_name,
            'state': state,
        }
    return out


snmp_section_bluenet_gpio_sensor = SNMPSection(
    name="bluenet_gpio_sensor",
    detect=startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.31770"),
    fetch=[
        SNMPTree(
            base=".1.3.6.1.4.1.31770.2.2.4.2.1", # bluenet2DeviceTable
            oids=[OIDEnd(),
                  "3", # Name (Master, Slave-1, ...)
                  "4", # FriendlyName (Stellplatz)
                 ],
        ),
        SNMPTree(
            base=".1.3.6.1.4.1.31770.2.2.5.2.1", # bluenet2SensorTable
            oids=[OIDEnd(),
                  "4", # Name (GPIO S1, GPIO Internal, ...)
                  "5", # FriendlyName
                  "7", # Sensor type OID
                  "8", # State
                 ],
        ),
    ],
    parse_function=parse_gpio_sensor,
)


def discover_bluenet_gpio_sensor(section):
    """ Discover Function """
    for sensor, data in section.items():
        labels = []
        if data['device_friendly_name']:
            labels.append(ServiceLabel("device_friendly_name", data['device_friendly_name']))
        yield Service(item=sensor, labels=labels)


def check_bluenet_gpio_sensor(item, section):
    """ Check Function """
    if not (data := section.get(item)):
        return

    state_name, state = ENTITY_STATES.get(data['state'], (f"unknown ({data['state']})",
                                                          State.UNKNOWN))
    yield Result(state=state, summary=f"Status: {state_name}")
    yield Result(state=State.OK, summary=f"Type: {data['type']}")
    if data['friendly_name']:
        yield Result(state=State.OK, summary=f"Name: {data['friendly_name']}")
    if data['device_friendly_name']:
        yield Result(state=State.OK, notice=f"Device: {data['device_friendly_name']}")


check_plugin_bluenet_gpio_sensor = CheckPlugin(
    name="bluenet_gpio_sensor",
    service_name="GPIO Sensor %s",
    discovery_function=discover_bluenet_gpio_sensor,
    check_function=check_bluenet_gpio_sensor,
)
