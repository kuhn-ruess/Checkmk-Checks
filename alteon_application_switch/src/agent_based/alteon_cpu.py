#!/usr/bin/env python3

from .agent_based_api.v1 import (
    register,
    SNMPTree, 
    startswith,
    Service,
    Result,
    State,
    Metric,
)


# [[u'27', u'26', u'25'], [u'25', u'26', u'20']]
def parse_cpu_cores(cpu_values, cpu_desc):
    parsed_cpu_values = {}
    for core_id, core in zip(range(0, len(cpu_values)), cpu_values):
        # core ->  [u'6', u'5', u'6']
        values = {}
        values["1sec"] = int(core[0]) # alternative for decimals float()  
        values["4sec"] = int(core[1])
        values["64sec"] = int(core[2])
        parsed_cpu_values["CPU {} Core {} Utilization".format(cpu_desc, core_id + 1)] = values

    return parsed_cpu_values
    # {'CPU MP 1': {'1sec': 7, '64sec': 9, '4sec': 6}, 'CPU SP 2': {'1sec': 22, '64sec': 23, '4sec': 26}, 'CPU SP 1': {'1sec': 23, '64sec': 21, '4sec': 23}}

# [[[u'6', u'5', u'6'], [u'25', u'26', u'20']], [[u'27', u'26', u'25'], [u'25', u'26', u'20']]]
def parse_alteon_cpu(string_table):
    # 1. Array -> Values for MP
    # 2. Array -> Values for SP
    mp_values = string_table[0] # [[u'6', u'5', u'6'], [u'25', u'26', u'20']]
    sp_values = string_table[1] # [[u'27', u'26', u'25'], [u'25', u'26', u'20']]

    section = parse_cpu_cores(mp_values, "MP")
    section.update(parse_cpu_cores(sp_values, "SP"))

    return section


register.snmp_section(
    name="alteon_cpu",
    detect=startswith('.1.3.6.1.2.1.1.1.0', "Alteon Application Switch"),
    parse_function=parse_alteon_cpu,
    fetch=[
        SNMPTree(
            base='.1.3.6.1.4.1.1872.2.5.1.2.2', # MP CPU Utilization
            oids=[
                '1', # MP CPU utilization over 1 sec
                '2', # MP CPU utilization over 4 sec
                '3', # MP CPU utilization over 64 sec
            ]
        ),
        SNMPTree(
            base='.1.3.6.1.4.1.1872.2.5.1.2.4.1.1', # SP CPU Utilization
            oids=[
                '2', # The utilization of this SP over 1 second.
                '3', # SP CPU utilization over 4 sec
                '4', # SP CPU utilization over 64 sec
            ]
        ),
    ],
)


# Returnes dictionary of Services within this check and additional tresholds
# parsed -> {'CPU MP Core 1 Utilization': {'1sec': 7, '64sec': 9, '4sec': 6}, 'CPU SP 2': {'1sec': 22, '64sec': 23, '4sec': 26}, 'CPU SP 1': {'1sec': 23, '64sec': 21, '4sec': 23}}
def discover_alteon_cpu(section):
    for core_name, values in section.items():
        tresholds = {}
        tresholds["alteon_cpu_utilization_tresholds"] = (80, 90)
        yield Service(item=core_name, parameters=tresholds)



# check function
# item -> Service name
# params -> thresohlds and others if specified
# section -> output of the parse_cpu_cores function
# CPU_SP_Core_2_Utilization
# {'alteon_cpu_utilization_tresholds': (33.0, 44)}
# {'CPU_SP_Core_1_Utilization': {'1sec': 19, '64sec': 19, '4sec': 17}, 'CPU_MP_Core_1_Utilization': {'1sec': 5, '64sec': 6, '4sec': 5}, 'CPU_SP_Core_2_Utilization': {'1sec': 19, '64sec': 21, '4sec': 20}}
def check_alteon_cpu(item, params, section):
    treshold_key = "1sec"
    values = section[item]

    # check for warn/crit
    warn_treshold, crit_treshold = params["alteon_cpu_utilization_tresholds"]
    value = values[treshold_key]
    state = 0
    infotext = "{}: ".format(item)
    yield Result(state=State.OK, summary=f"{item}: ")
    for duration, value in values.items():
        yield Metric(duration, value, levels=(warn_treshold, crit_treshold))
        if value >= crit_treshold:
            yield Result(state=State.CRIT, summary=f"{duration}:{value}")
        elif value >= warn_treshold:
            yield Result(state=State.WARN, summary=f"{duration}:{value}")
        else:
            yield Result(state=State.OK, summary=f"{duration}:{value}")

     
register.check_plugin(
    name='alteon_cpu',
    service_name='%s',
    discovery_function=discover_alteon_cpu,
    check_function=check_alteon_cpu,
    check_ruleset_name='alteon_cpu',
    check_default_parameters={},
)
