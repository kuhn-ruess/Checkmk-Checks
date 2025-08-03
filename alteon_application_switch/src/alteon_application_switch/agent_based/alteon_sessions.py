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


def parse_alteon_sessions(string_table): # [[[u'17889', u'17919', u'17727'], [u'18715', u'18714', u'18527']]]
    # session per SP-Core
    sessions = {}
    for core_id, core_sessions in enumerate(string_table):
        values = {}
        values["max"] = int(core_sessions[0])
        values["current_sessions"] = int(core_sessions[1])
        values["4sec"] = int(core_sessions[2])
        values["64sec"] = int(core_sessions[3])
        sessions["SP {}".format(core_id + 1)] = values
    return sessions

snmp_section_alteon_sessions = SNMPSection(
    name="alteon_sessions",
    detect=startswith('.1.3.6.1.2.1.1.1.0', "Alteon Application Switch"),
    parse_function=parse_alteon_sessions,
    fetch=SNMPTree(
            base='.1.3.6.1.4.1.1872.2.5.4.2.1.5.1', # SP Session Bindings
            oids=[
                # http://oidref.com/1.3.6.1.4.1.1872.2.5.4.2.1.5.1.4
                '2', # he maximun number of entries per SP in the session table for Treshold Calculation.
                '3', # SP Current Session Binding
                '4', # SP Session Bindings over 4 Sec
                '5', # SP Session Bindings over 64 sec
            ]
        ),
)


def discover_alteon_sessions(section):
    for core, sessions in section.items():
        tresholds = {}
        tresholds["alteon_session_tresholds"] = (80, 90)
        yield Service(item=core, parameters=tresholds)


def check_alteon_sessions(item, params, section):
    warn_treshold, crit_treshold = params["alteon_session_tresholds"] # in percent
    values = section[item]
    max_sessions = values["max"]
    warn_treshold = max_sessions / 100 * warn_treshold # in sessions
    crit_treshold = max_sessions / 100 * crit_treshold # in sessions

    del values["max"]

    yield Result(state=State.OK, summary="Sessions {}: ".format(item))
    for duration, value in values.items():
        yield Metric(duration, value, levels=(warn_treshold, crit_treshold), 
                        boundaries=(0, max_sessions))
        if value >= crit_treshold:
            yield Result(state=State.CRIT, summary="{}:{},".format(duration, value))
        elif value >= warn_treshold:
            yield Result(state=State.WARN, summary="{}:{},".format(duration, value))
        else:
            yield Result(state=State.OK, summary="{}:{},".format(duration, value))
    
    yield Result(state=State.OK, summary="(Limit: {})".format(max_sessions))


check_plugin_alteon_sessions = CheckPlugin(     
    name='alteon_sessions',
    service_name='Sessions %s',
    discovery_function=discover_alteon_sessions,
    check_function=check_alteon_sessions,
    check_ruleset_name='alteon_sessions',
    check_default_parameters={},
)
