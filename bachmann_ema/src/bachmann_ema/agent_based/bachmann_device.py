#!/usr/bin/python
"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
from cmk.agent_based.v2 import (
        SimpleSNMPSection,
        CheckPlugin,
        OIDEnd,
        Service,
        ServiceLabel,
        SNMPTree,
        State,
        Result,
        startswith,
)

from cmk_addons.plugins.bachmann_ema.agent_based.bachmann_gpio_sensor import ENTITY_STATES


def parse_bluenet_device(string_table):
    """Parse the BlueNet2 device table (Master and Slave PDUs) by name"""
    out = {}
    for index, name, friendly_name, state, part_number in string_table:
        out[name or f"Device {index}"] = {
            'friendly_name': friendly_name,
            'state': state,
            'part_number': part_number,
        }
    return out


snmp_section_bluenet_device = SimpleSNMPSection(
    name="bluenet_device",
    detect=startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.31770"),
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.31770.2.2.4.2.1", # bluenet2DeviceTable
        oids=[OIDEnd(),
              "3", # Name (Master, Slave-1, ...)
              "4", # FriendlyName
              "7", # State
              "11", # Part number
             ],
    ),
    parse_function=parse_bluenet_device,
)


def discover_bluenet_device(section):
    """Discover one service per PDU of the daisy chain"""
    for name, data in section.items():
        labels = []
        if data['friendly_name']:
            labels.append(ServiceLabel("device_friendly_name", data['friendly_name']))
        yield Service(item=name, labels=labels)


def check_bluenet_device(item, section):
    """Check the state of one PDU as reported by the master"""
    if not (data := section.get(item)):
        yield Result(state=State.CRIT,
                     summary="PDU missing from the device table of the master")
        return

    state_name, state = ENTITY_STATES.get(data['state'], (f"unknown ({data['state']})",
                                                          State.UNKNOWN))
    yield Result(state=state, summary=f"Status: {state_name}")
    if data['friendly_name']:
        yield Result(state=State.OK, summary=f"Name: {data['friendly_name']}")
    if data['part_number']:
        yield Result(state=State.OK, notice=f"Part number: {data['part_number']}")


check_plugin_bluenet_device = CheckPlugin(
    name="bluenet_device",
    service_name="PDU %s",
    discovery_function=discover_bluenet_device,
    check_function=check_bluenet_device,
)
