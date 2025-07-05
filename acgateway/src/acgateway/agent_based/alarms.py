#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from mk.agent_based.v2 import (
    all_of,
    contains,
    register,
    render,
    Metric,
    Result,
    Service,
    SNMPTree,
    State,
)

from datetime import datetime

def _convert_date_and_time(octet_string):
    return datetime(
        year=ord(octet_string[0]) * 256 + ord(octet_string[1]),
        month=ord(octet_string[2]),
        day=ord(octet_string[3]),
        hour=ord(octet_string[4]),
        minute=ord(octet_string[5]),
        second=ord(octet_string[6]),
        microsecond=ord(octet_string[7])*100,
    )

def parse_acgateway_alarms(string_table):
    map_severity = {
        "0": "cleared",
        "1": "indeterminate",
        "2": "warning",
        "3": "minor",
        "4": "major",
        "5": "critical",
    }
    map_state = {
        "0": State.OK,
        "1": State.UNKNOWN,
        "2": State.WARN,
        "3": State.WARN,
        "4": State.CRIT,
        "5": State.CRIT,
    }
    section = {
        'alarms': [],
        'archived': len(string_table[1]),
    }
    for alarm in string_table[0]:
        section['alarms'].append({
            'seq': int(alarm[0]),
            'sysuptime': int(alarm[1]),
            'datetime': _convert_date_and_time(alarm[2]),
            'name': alarm[3],
            'desc': alarm[4],
            'source': alarm[5],
            'severity': map_severity.get(alarm[6], alarm[6]),
            'state': map_state.get(alarm[6], State.UNKNOWN),
        })
    return section
    
snmp_section_acgateway_alarms = SimpleSNMPSection(
    name = "acgateway_alarms",
    parse_function = parse_acgateway_alarms,
    fetch = [
        SNMPTree(
            base = ".1.3.6.1.4.1.5003.11.1.1.1.1",
            oids = [
                '1', # AcAlarm::acActiveAlarmSequenceNumber
                '2', # AcAlarm::acActiveAlarmSysuptime
                '4', # AcAlarm::acActiveAlarmDateAndTime
                '5', # AcAlarm::acActiveAlarmName
                '6', # AcAlarm::acActiveAlarmTextualDescription
                '7', # AcAlarm::acActiveAlarmSource
                '8', # AcAlarm::acActiveAlarmSeverity
            ]
        ),
        SNMPTree(
            base = ".1.3.6.1.4.1.5003.11.1.2.1.1",
            oids = [
                '1', # AcAlarm::acAlarmHistorySequenceNumber
            ]
        ),
    ],
    detect = all_of(
        contains(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.5003.8.1.1"),
        contains(".1.3.6.1.2.1.1.1.0", "SW Version: 7.20A"),
    ),
)

def discover_acgateway_alarms(section):
    yield Service()

def check_acgateway_alarms(section):
    if len(section['alarms']) == 0:
        yield Result(state=State.OK,
                     summary="No active alarms present")
    else:
        for alarm in section['alarms']:
            yield Result(state=alarm['state'],
                         notice="ALARM#%d: %s %s %s, source: %s, uptime: %s, severity: %s" % (
                             alarm['seq'],
                             alarm['datetime'].isoformat(),
                             alarm['name'],
                             alarm['desc'],
                             alarm['source'],
                             render.timespan(alarm['sysuptime']),
                             alarm['severity']
                         ))
    yield Metric('active_alarms', len(section['alarms']))
    yield Result(state=State.OK,
                 summary="%d alarms archived" % section['archived'])
    yield Metric('archived_alarms', section['archived'])

check_plugin_acgateway_alarms = CheckPlugin(
    name = "acgateway_alarms",
    service_name = "SIP Alarms",
    discovery_function = discover_acgateway_alarms,
    check_function = check_acgateway_alarms,
)
