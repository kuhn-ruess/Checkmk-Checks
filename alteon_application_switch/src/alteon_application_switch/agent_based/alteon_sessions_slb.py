#!/usr/bin/env python3

from cmk.agent_based.v2 import (
    SNMPTree, 
    startswith,
    Service,
    Result,
    State,
    Metric,
    CheckPlugin,
    SNMPSection,
)

#[[[u'2097126', u'35423', u'35386', u'35561']]]
def parse_alteon_slb_sessions(string_table):
    values = {}
    values['max'] = int(string_table[0][0])
    values['current_sessions'] = int(string_table[0][1])
    values['4sec'] = int(string_table[0][2])
    values['64sec'] = int(string_table[0][3])
    return values


snmp_section_alteon_sessions_slb = SNMPSection(
    name="alteon_sessions_slb",
    detect=startswith('.1.3.6.1.2.1.1.1.0', "Alteon Application Switch"),
    parse_function=parse_alteon_slb_sessions,
    fetch=[
        SNMPTree(
            # http://oidref.com/1.3.6.1.4.1.1872.2.5.4.2.5.2
            base='.1.3.6.1.4.1.1872.2.5.4.2.5',
            oids=[
                '1', # slbStatMaintMaximumSessions (1048563)
                '2', # slbStatMaintCurBindings
                '3', # slbStatMaintCurBindings4Seconds
                '4', # slbStatMaintCurBindings64Seconds
            ]
        )],
)

#{
#    '4sec': 34700, 
#    'current sessions': 34656, 
#    'max': 2097126, 
#    '64sec': 35008
#}
def discover_alteon_slb_sessions(section):
    if section['max'] > 0:
        tresholds = {}
        tresholds['alteon_slb_sessions_tresholds'] = (80, 90)
        yield Service(item="SLB Sessions", parameters=tresholds)

#SLB Sessions
#{'alteon_slb_sessions_tresholds': (1677680, 1887390)}
#{
#    '4sec': 34700, 
#    'current sessions': 34656, 
#    'max': 2097126, 
#    '64sec': 35008
#}
def check_alteon_slb_sessions(item, params, section):
    warn_treshold, crit_treshold = params["alteon_slb_sessions_tresholds"] # in precent
    max = section["max"]
    del section["max"]
    warn_treshold = max / 100 * warn_treshold # in sessions
    crit_treshold = max / 100 * crit_treshold # in sessions

    yield Result(state=State.OK, summary="SLB Sessions {}: ".format(item))
    for duration, value in section.items():
        yield Metric(duration, value, levels=(warn_treshold, crit_treshold),
                        boundaries=(0, max))
        if value >= crit_treshold:
            yield Result(state=State.CRIT, summary="{}:{},".format(duration, value))
        elif value >= warn_treshold:
            yield Result(state=State.WARN, summary="{}:{},".format(duration, value))
        else:
            yield Result(state=State.OK, summary="{}:{},".format(duration, value))

    yield Result(state=State.OK, summary="(Limit: {})".format(max))


check_plugin_alteon_sessions_slb = CheckPlugin(     
    name='alteon_sessions_slb',
    service_name='%s',
    discovery_function=discover_alteon_slb_sessions,
    check_function=check_alteon_slb_sessions,
    check_ruleset_name='alteon_sessions',
    check_default_parameters={},
)
