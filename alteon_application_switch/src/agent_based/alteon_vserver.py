#!/usr/bin/env python3

from .agent_based_api.v1 import (
    register,
    SNMPTree, 
    startswith,
    Service,
    Result,
    State,
    Metric,
    get_value_store,
    get_rate,
    GetRateError
)

def parse_alteon_vserver(string_table):
    vserver = {}
    for ip_data in string_table:
        values = {}
        values["ip"] = "{}".format(ip_data[0])
        values["current_sessions"] = int(ip_data[1])
        values["new_sessions_per_second"] = int(ip_data[2])
        #values["total_sessions"] = int(ip_data[2])
        values["peak_sessions"] = int(ip_data[3])
        #values["octets_low"] = int(ip_data[4])
        #values["octets_high"] = int(ip_data[5])
        values["http_header_sessions"] = int(ip_data[6])
        #values["hc_octets"] = int(ip_data[7])
        values["hc_octets_per_sec"] = int(ip_data[7])
        values["label"] = "{}".format(ip_data[8])
        vserver[values["label"]] = values
    return vserver


register.snmp_section(
    name="alteon_vserver",
    detect=startswith('.1.3.6.1.2.1.1.1.0', "Alteon Application Switch"),
    parse_function=parse_alteon_vserver,
    fetch=SNMPTree(
            base='.1.3.6.1.4.1.1872.2.5.4.2.32.1', # Virtual Server utilization
            oids=[
                '14', # IPs
                '2', # Current Sessions
                '3', # Total Sessions
                '4', # Peak Sessions
                '5', # Octets In + Out slbStatEnhVServerHCOctetsLow32
                '6', # Octets In + Out slbStatEnhVServerHCOctetsHigh32
                '10', # The total HTTP header sessions slbStatEnhVServerHeaderTotalSessions
                '13', # HC Octets slbStatEnhVServerHCOctets
                '1', # label?
            ]
        ),
)


def discover_alteon_vserver(section):
    for idx, data in section.items():
        #service_name = "{} [{}]".format(idx, data["ip"])
        yield Service(item=idx)


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


def check_alteon_vserver(item, section):
    this_time = time.time()
    value_store = get_value_store()

    continuous_counter = [
        "hc_octets",
        "octets_high",
        "octets_low",
        "new_sessions_per_second",
        "hc_octets_per_sec"
    ]
    #idx, ip = item.split()
    #idx = int(idx)
    #ip = ip[1:-1]
    if not item in section.keys():
        return None

    vserver_data = section[item]
    perfdata = []
    wrapped = False
    infotext = "[{}]: ".format(vserver_data["ip"])
    del vserver_data["ip"]
    del vserver_data["label"]
    for counter, value in vserver_data.items():
        if counter in continuous_counter:
            try:
                value = get_rate(value_store,
                        "Alteon_VServer.{}.{}".format(item, counter),
                        this_time, value,
                        raise_overflow=True)
                vserver_data[counter] = value
            except GetRateError:
                value = None

        yield Metric(counter, value)
        #infotext = "{}\n{} :{}".format(infotext, counter, value)
    infotext = "{} Sessions: {}, Traffic: {}".format(
        infotext,
        vserver_data["current_sessions"],
        get_traffic_human_readable(vserver_data["hc_octets_per_sec"], 'Byte', 'Byte')
    )
    yield Result(state=State.OK, summary=infotext)


register.check_plugin(
    name='alteon_vserver',
    service_name='VServer [%s]',
    discovery_function=discover_alteon_vserver,
    check_function=check_alteon_vserver,
)
