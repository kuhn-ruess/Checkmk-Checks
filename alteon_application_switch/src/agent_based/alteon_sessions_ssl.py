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

def parse_alteon_sessions_ssl(string_table): # [[[u'1000']], [[u'722 CPS', u'28 CPS']]]
    print(string_table)
    values = {}
    values['max_ssl_sessions'] = int(string_table[0][0][0])
    values['peak_ssl_sessions'] = int(string_table[1][0][0].split()[0])
    values['current_ssl_sessions'] = int(string_table[1][0][1].split()[0])
    return values


register.snmp_section(
    name="alteon_sessions_ssl",
    detect=startswith('.1.3.6.1.2.1.1.1.0', "Alteon Application Switch"),
    parse_function=parse_alteon_sessions_ssl,
    fetch=[
        SNMPTree(
            base='.1.3.6.1.4.1.1872.2.5.1.3.10.3.1.2',
            oids=[
                '10', # Max SSL Sessions for Context (Try and Error)
            ]
        ),
        # NOTE: Checkmk no longer allows empty OID strings, thus the change
        SNMPTree(
            base='.1.3.6.1.4.1.1872.2.5.1.2.12', # Peak SSL Sessions
            oids=[
                '3',
                '4',
            ]
        ),
    ],
)


def discover_alteon_sessions_ssl(section): 
    max_ssl_sessions = section['max_ssl_sessions']
    if max_ssl_sessions > 0: # do not inventory if max_ssl_sessions is 0
        tresholds = {}
        tresholds["alteon_session_ssl_tresholds"] = (80, 90)
        yield Service(item="SSL Sessions", parameters=tresholds)


def check_alteon_sessions_ssl(item, params, section):
    max_ssl_sessions = section['max_ssl_sessions']
    peak_ssl_sessions = section['peak_ssl_sessions']
    current_ssl_sessions = section['current_ssl_sessions']
    warn_treshold, crit_treshold = params["alteon_session_ssl_tresholds"] # in percent
    warn_treshold = max_ssl_sessions / 100 * warn_treshold # in sessions
    crit_treshold = max_ssl_sessions / 100 * crit_treshold # in sessions

    yield Metric("Peak", peak_ssl_sessions,
                    levels=(warn_treshold, crit_treshold),
                    boundaries=(0, max_ssl_sessions))
    yield Metric("Current", current_ssl_sessions,
                    levels=(warn_treshold, crit_treshold),
                    boundaries=(0, max_ssl_sessions))

    infotext = "SSL Sessions: Current:{}, Peak:{}, (Limit:{})".format(current_ssl_sessions, peak_ssl_sessions, max_ssl_sessions)

    if current_ssl_sessions >= crit_treshold:
        yield Result(state=State.CRIT, summary=infotext)
    elif current_ssl_sessions >= warn_treshold:
        yield Result(state=State.WARN, summary=infotext)
    else:
        yield Result(state=State.OK, summary=infotext)


register.check_plugin(
    name='alteon_sessions_ssl',
    service_name='%s',
    discovery_function=discover_alteon_sessions_ssl,
    check_function=check_alteon_sessions_ssl,
    check_ruleset_name='alteon_sessions',
    check_default_parameters={},
)
