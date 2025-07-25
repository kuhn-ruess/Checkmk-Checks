#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.agent_based.v2 import (
    contains,
    get_rate,
    get_value_store,
    Metric,
    Result,
    Service,
    SNMPTree,
    State,
    SNMPSection,
    CheckPlugin,
)

from time import time

def parse_acgateway_sipperf(string_table):
    return string_table

snmp_section_acgateway_sipperf = SNMPSection(
    name = "acgateway_sipperf",
    parse_function = parse_acgateway_sipperf,
    fetch = [
        SNMPTree(
            base = '.1.3.6.1.4.1.5003.10.3.1.1.1',
            oids = [
                '1.0',  # AcPerfH323SIPGateway::acPerfTel2IPAttemptedCalls
                '2.0',  # AcPerfH323SIPGateway::acPerfTel2IPEstablishedCalls
                '3.0',  # AcPerfH323SIPGateway::acPerfTel2IPBusyCalls
                '4.0',  # AcPerfH323SIPGateway::acPerfTel2IPNoAnswerCalls
                '5.0',  # AcPerfH323SIPGateway::acPerfTel2IPNoRouteCalls
                '6.0',  # AcPerfH323SIPGateway::acPerfTel2IPNoMatchCalls
                '7.0',  # AcPerfH323SIPGateway::acPerfTel2IPFailCalls
                '8.0',  # AcPerfH323SIPGateway::acPerfTel2IPFaxAttemptedCalls
                '9.0',  # AcPerfH323SIPGateway::acPerfTel2IPFaxSuccessCalls
                '10.0', # AcPerfH323SIPGateway::acPerfTel2IPTotalDuration
            ],
        ),
        SNMPTree(
            base = '.1.3.6.1.4.1.5003.10.3.1.1.2',
            oids = [
                '1.0',  # AcPerfH323SIPGateway::acPerfIP2TelAttemptedCalls
                '2.0',  # AcPerfH323SIPGateway::acPerfIP2TelEstablishedCalls
                '3.0',  # AcPerfH323SIPGateway::acPerfIP2TelBusyCalls
                '4.0',  # AcPerfH323SIPGateway::acPerfIP2TelNoAnswerCalls
                '5.0',  # AcPerfH323SIPGateway::acPerfIP2TelNoRouteCalls
                '6.0',  # AcPerfH323SIPGateway::acPerfIP2TelNoMatchCalls
                '7.0',  # AcPerfH323SIPGateway::acPerfIP2TelFailCalls
                '8.0',  # AcPerfH323SIPGateway::acPerfIP2TelFaxAttemptedCalls
                '9.0',  # AcPerfH323SIPGateway::acPerfIP2TelFaxSuccessCalls
                '10.0', # AcPerfH323SIPGateway::acPerfIP2TelTotalDuration
            ],
        ),
    ],
    detect = contains(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.5003.8.1.1"),
)

def discover_acgateway_sipperf(section):
    if len(section) == 2 and len(section[0]) == 1 and len(section[1]) == 1:
        yield Service()

def check_acgateway_sipperf(section):
    sipperf_info = {
        0:  ("sip_calls_attempted", "Number of Attempted SIP/H323 calls"),
        1:  ("sip_calls_established", "Number of established (connected and voice activated) SIP/H323 calls"),
        2:  ("sip_destination_busy", "Number of Destination Busy SIP/H323 calls"),
        3:  ("sip_no_answer", "Number of No Answer SIP/H323 calls"),
        4:  ("sip_no_route", "Number of No Route SIP/H323 calls. Most likely to be due to wrong number"),
        5:  ("sip_no_capability", "Number of No capability match between peers on SIP/H323 calls"),
        6:  ("sip_failed", "Number of failed SIP/H323 calls"),
        7:  ("sip_fax_attempted", "Number of Attempted SIP/H323 fax calls"),
        8:  ("sip_fax_success", "Number of SIP/H323 fax success calls"),
        9:  ("sip_total_duration", "total duration of SIP/H323 calls"),
        }
    if len(section) == 2:
        vs = get_value_store()
        this_time = time()
        # Tel2IP
        for key, value in enumerate(section[0][0]):
            if key == 9:
                yield Result(state=State.OK,
                             notice="Tel2IP %s: %d" % (sipperf_info[key][1], int(value)))
                yield Metric('tel2ip_%s' % sipperf_info[key][0], int(value))
            else:
                rate = get_rate(vs, 'acgateway_sipperf.tel2ip_%s' % sipperf_info[key][0], this_time, int(value))
                yield Result(state=State.OK,
                             notice="Tel2IP %s: %0.1f/s" % (sipperf_info[key][1], rate))
                yield Metric('tel2ip_%s' % sipperf_info[key][0], rate)
        # IP2Tel
        for key, value in enumerate(section[1][0]):
            if key == 9:
                yield Result(state=State.OK,
                             notice="IP2Tel %s: %d" % (sipperf_info[key][1], int(value)))
                yield Metric('ip2tel_%s' % sipperf_info[key][0], int(value))
            else:
                rate = get_rate(vs, 'acgateway_sipperf.ip2tel_%s' % sipperf_info[key][0], this_time, int(value))
                yield Result(state=State.OK,
                             notice="IP2Tel %s: %0.1f/s" % (sipperf_info[key][1], rate))
                yield Metric('ip2tel_%s' % sipperf_info[key][0], rate)

check_plugin_acgateway_sipperf = CheckPlugin(
    name = "acgateway_sipperf",
    service_name = "SIP Performance",
    discovery_function = discover_acgateway_sipperf,
    check_function = check_acgateway_sipperf,
)
