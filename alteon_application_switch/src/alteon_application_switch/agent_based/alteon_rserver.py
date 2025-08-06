#!/usr/bin/env python3

from cmk.agent_based.v2 import (
    SNMPTree, 
    startswith,
    Service,
    Result,
    State,
    Metric,
    get_value_store,
    get_rate,
    GetRateError,
    CheckPlugin,
    SNMPSection,
)

import time

def parse_alteon_rserver(string_table):
    rserver = {}
    for ip_data in string_table:
        values = {}
        values["name"] = ip_data[0]
        values["current_sessions"] = int(ip_data[1])
        #values["total_sessions"] = int(ip_data[2])
        values["new_sessions_per_second"] = int(ip_data[2])
        values["failures"] = int(ip_data[3])
        values["peak_sessions"] = int(ip_data[4])
        #values["octets_total"] = int(ip_data[5])
        #values["octets_total_low"] = int(ip_data[6])
        #values["octets_total_rxtx"] = int(ip_data[7])
        values["octets_total_rxtx_per_second"] = int(ip_data[7])
        rserver[ip_data[0]] = values
    return rserver


snmp_section_alteon_server = SNMPSection(
    name="alteon_rserver",
    detect=startswith('.1.3.6.1.2.1.1.1.0', "Alteon Application Switch"),
    parse_function=parse_alteon_rserver,
    fetch=[
        SNMPTree(
            base='.1.3.6.1.4.1.1872.2.5.4.2.30.1', # Real Server utilization
            oids=[
                '1', # Name
                '2', # Current Sessions
                '3', # Total Sessions
                '4', # Failures slbStatEnhRServerFailures
                '5', # Session Peak slbStatEnhRServerHighestSessions
                '6', # Total Octets In + Out slbStatEnhRServerHCOctets
                '7', # Total Octets In + Out Low slbStatEnhRServerHCOctetsLow32
                '8', # Total rx/tx Octets slbStatEnhRServerHCOctets
            ]
        )],
)


def discover_alteon_rserver(section):
    for name, data in section.items():
        yield Service(item=name) 


def get_traffic_human_readable(speed, in_unit, out_unit):
    base = 1000.0
    if in_unit == "Bit" and out_unit == 'Byte':
        speed = speed / 8
    if in_unit == "Byte" and out_unit == "Bit":
        #base = 1024.0
        speed = speed * 8

    units = [
        "",
        "k",
        "M",
        "G",
        "T"
    ]
    i = 0
    while speed >= base:
        speed = speed / base
        i = i + 1

    return "{:.4g} {}{}/s".format(speed, units[i], out_unit)


def check_alteon_rserver(item, section):
    this_time = time.time()
    value_store = get_value_store()

    continuous_counter = [
        "octets_total",
        "octets_total_low",
        "octets_total_rxtx",
        "new_sessions_per_second",
        "octets_total_rxtx_per_second"
    ]

    rserver_data = section[item]
    name = rserver_data["name"]
    del rserver_data["name"]
    for counter, value in rserver_data.items():
        if counter in continuous_counter:
            try:
                value = get_rate(value_store, "Alteon_RServer.{}.{}".format(item, counter), this_time, value, raise_overflow=True)
                rserver_data[counter] = value
            except GetRateError:
                continue

        yield Metric(counter, value)

    yield Result(state=State.OK, summary="[{}]: Sessions: {}, Traffic {} ".format(
            name,
            rserver_data["current_sessions"],
            get_traffic_human_readable(rserver_data["octets_total_rxtx_per_second"], 'Byte', 'Byte')
        ))


check_plugin_alteon_rserver = CheckPlugin(     
    name='alteon_rserver',
    service_name='RServer [%s]',
    discovery_function=discover_alteon_rserver,
    check_function=check_alteon_rserver,
)
