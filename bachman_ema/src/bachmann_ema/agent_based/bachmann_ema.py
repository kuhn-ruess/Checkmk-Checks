#!/usr/bin/python
"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
from cmk.agent_based.v2 import (
        SimpleSNMPSection,
        CheckPlugin,
        Service,
        SNMPTree,
        State,
        Metric,
        Result,
        startswith,
)

def parse_ema(string_table):
    """
    Parse function
    """
    out = {}
    for line in string_table:
        in_1, in_2, mode_1, mode_2, switch_1, switch_2 = line
        out[f'{in_1}/1'] = (mode_1, switch_1)
        out[f'{in_2}/2'] = (mode_2, switch_2)
    return out


snmp_section_bluenet_ema = SimpleSNMPSection(
    name="bluenet_ema",
    detect=startswith(".1.3.6.1.2.1.1.1.0", "Linux BLUENET2"),
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.31770.2.2.5.3.1",
        oids=["5.1.4", # First 4 Input/Outputs
              "5.1.5", # Second 4 Input/Outputs
              "8.1.4", # BlueNet2GPIOModes for Frist 
              "8.1.5", # BlueNet2GPIOModes for Second
              "9.1.4", # BlueNet2GPIOSwitch for First
              "9.1.5", # BlueNet2GPIOSwitch for Second
             ],
    ),
    parse_function = parse_ema,
)

def discover_bluenet_ema(section):
    """ Discover Function """
    for sensor, data in section.items():
        if data[0] in ['2', '6']:
            yield Service(item=sensor)

def check_bluenet_ema(item, section):
    state = State.OK
    mode, switch = section[item]
    gpio_mode = {
            '0': 'disabled',
            '2': 'enabled',
            '6': 's0',
            '7': 'undefined',
    }
    yield Result(state=state, summary=f"Mode: {gpio_mode[mode]}")
    gpio_switch = {
            '0': 'undefined',
            '3': 'switchable',
            '5': 'notSwitchable',
            '1': 'on',
            '2': 'off',
    }
    yield Result(state=state, summary=f"Switch: {gpio_switch[switch]}")

check_plugin_bluenet_ema = CheckPlugin(
    name="bluenet_ema",
    service_name="EMA %s",
    discovery_function=discover_bluenet_ema,
    check_function=check_bluenet_ema,
)
