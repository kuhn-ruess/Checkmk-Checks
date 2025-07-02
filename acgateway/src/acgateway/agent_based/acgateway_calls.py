#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.agent_based.v2 import (
    all_of,
    contains,
    get_rate,
    get_value_store,
    register,
    render,
    Metric,
    OIDEnd,
    Result,
    Service,
    SNMPTree,
    State,
)

from time import time

def parse_acgateway_calls(string_table):
    section = None
    if len(string_table) == 1:
        for active_calls, total_calls, asr, acd in string_table:
            section = {
                'active_calls': int(active_calls),
                'total_calls': int(total_calls),
                'asr': int(asr),
                'acd': int(acd),
            }
    return section

snmp_section_acgateway_calls = SimpleSNMPSection(
    name = "acgateway_calls",
    parse_function = parse_acgateway_calls,
    fetch = SNMPTree(
        base = '.1.3.6.1.4.1.5003.10.8.2',
        oids = [
            "52.43.1.2.0",   # AC-PM-Control-MIB::acPMSIPSBCEstablishedCallsVal.0
            "52.43.1.9.0",   # AC-PM-Control-MIB::acPMSIPSBCEstablishedCallsTotal.0
            "54.49.1.2.0",   # AC-PM-Control-MIB::acPMSBCAsrVal.0
            "54.52.1.2.0",   # AC-PM-Control-MIB::acPMSBCAcdVal.0
        ]
    ),
    detect = all_of(
        contains(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.5003.8.1.1"),
        contains(".1.3.6.1.2.1.1.1.0", "SW Version: 7.20A"),
    ),
)

def discover_acgateway_calls(section):
    yield Service()

def check_acgateway_calls(section):
    vs = get_value_store()
    now = time.time()
    yield Result(state=State.OK,
                 summary="Active Calls: %d" % section['active_calls'])
    yield Metric('active_calls', section['active_calls'])
    call_rate = get_rate(vs, 'acgateway_calls.total_calls', now, section['total_calls'])
    yield Result(state=State.OK,
                 summary="Calls per Second: %d/s" % call_rate)
    yield Metric('calls_per_sec', call_rate)
    yield Result(state=State.OK,
                 summary="Average Succes Ratio: %s" % render.percent(section['asr']))
    yield Metric('average_success_ratio', section['asr'])
    yield Result(state=State.OK,
                 summary="Average Call Duration: %s" % render.timespan(section['acd']))
    yield Metric('average_call_duration', section['acd'])

check_plugin_acgateway_calls = CheckPlugin(
    name = "acgateway_calls",
    service_name = "SBC Calls",
    discovery_function = discover_acgateway_calls,
    check_function = check_acgateway_calls,
)
