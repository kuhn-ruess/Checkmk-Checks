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
        all_of,
)

def parse_ema(string_table):
    """
    Parse function
    """
    out = {}
    for line in string_table:
        in_1, in_2, mode_1, mode_2, state_1, state_2, switch_1, switch_2 = line
        out[f'{in_1}/1'] = (mode_1, switch_1, state_1)
        out[f'{in_2}/2'] = (mode_2, switch_2, state_2)
    return out


snmp_section_bluenet_ema = SimpleSNMPSection(
    name="bluenet_ema",
    detect=all_of(
        startswith(".1.3.6.1.2.1.1.1.0", "Linux"),
        startswith(".1.3.6.1.2.1.1.6.0", "Bachmann"),
    ),
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.31770.2.2.5.3.1",
        oids=["5.1.4", # First 4 Input/Outputs
              "5.1.5", # Second 4 Input/Outputs
              "8.1.4", # BlueNet2GPIOModes for Frist 
              "8.1.5", # BlueNet2GPIOModes for Second
              "10.1.4", #GPIO State
              "10.1.5", #GPIO State
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
    mode, switch, entity_state = section[item]
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

    entity_states = {
       '0': 'expected',
       '1': 'undefined',
       '2': 'ok',
       '3': 'errorHigh',
       '4': 'errorLow',
       '5': 'warningHigh',
       '6': 'warningLow',
       '7': 'lost',
       '8': 'deactivate',
       '9': 'onAlarmIdentidy',
       '10': 'offAlarmIdentify',
       '11': 'onAlarm',
       '12': 'offAlarm',
       '13': 'onWarningIdentify',
       '14': 'offWarningIdentify',
       '15': 'onWarning',
       '16': 'offWarning',
       '17': 'onIdentify',
       '18': 'offIdentify',
       '19': 'on',
       '20': 'off',
       '21': 'onChildAlarm',
       '22': 'offChildAlarm',
       '23': 'onChildWarning',
       '24': 'offChildWarning',
       '25': 'childAlarm',
       '26': 'childWarning',
       '27': 'lostChild',
       '36': 'updateInProgress',
       '37': 'updateError',
       '38': 'onGoingSwitch',
       '39': 'high',
       '40': 'low',
       '41': 'alarm',
       '42': 'warning',
       '43': 'ok',
       '44': 'disabled',
       '45': 'fwVersionTooNew',
    }

    if entity_state == '39':
        state = State.CRIT

    yield Result(state=state, summary=f"Entity Status: {entity_states[entity_state]}")


check_plugin_bluenet_ema = CheckPlugin(
    name="bluenet_ema",
    service_name="EMA %s",
    discovery_function=discover_bluenet_ema,
    check_function=check_bluenet_ema,
)
