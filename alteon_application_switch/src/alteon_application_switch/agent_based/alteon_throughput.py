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


def parse_alteon_throughput(string_table): # [[[u'3000']], [[u'2620639424', u'158306176']]]
    values = {}
    values['max_throughput'] = int(string_table[0][0][0])
    values['peak_throughput'] = int(string_table[1][0][0])
    values['current_throughput'] = int(string_table[1][0][1])
    return values


snmp_section_alteon_throughput = SNMPSection(
    name="alteon_throughput",
    detect=startswith('.1.3.6.1.2.1.1.1.0', "Alteon Application Switch"),
    parse_function=parse_alteon_throughput,
    fetch=[
        SNMPTree(
            base='.1.3.6.1.4.1.1872.2.5.1.3.10.3.1.2',
            oids=[
                '9', # Max Throughput for Context (Try and Error)
            ]
        ),
        SNMPTree(
            base='.1.3.6.1.4.1.1872.2.5.1.2.12', # Throughput
            oids=[
                '1', # PeakThroughputUsage Peak throughput of ports in bits per second.
                '2', # curThroughputUsage Current Throughput Usage
            ]
        )
    ],
)


def discover_alteon_throughput(section):
    max_throughput = section['max_throughput']
    if max_throughput > 0: # do not inventory if max_throughput is 0
        tresholds = {}
        tresholds["alteon_throughput_tresholds"] = (70, 80)
        yield Service(item="Throughput", parameters=tresholds)


def get_traffic_human_readable(speed, in_unit, out_unit):
    base = 1024.0
    if speed == 0:
        return "{Speed not available}"
    if in_unit == "Bit" and out_unit == 'Byte':
        base = 1000.0
        speed = speed / 8
    if in_unit == "Byte" and out_unit == "Bit":
        speed = speed * 8

    units = [
        "",
        "k",
        "M",
        "G",
        "T"
    ]
    i = 0
    while speed > base:
        speed = speed / base
        i = i + 1

    return "{:.3f} {}{}/s".format(speed, units[i], out_unit)


def check_alteon_throughput(item, params, section):
    max_throughput = section['max_throughput'] # in Mbit/s
    peak_throughput = section['peak_throughput']
    current_throughput = section['current_throughput']
    warn_treshold, crit_treshold = params["alteon_throughput_tresholds"] # in percent
    max = max_throughput * 1000 * 1000 # in bit/s
    warn_treshold = max / 100 * warn_treshold # in bit/s
    crit_treshold = max / 100 * crit_treshold # in bit/s

    yield Metric("Peak", peak_throughput, 
                    levels=(warn_treshold, crit_treshold),
                    boundaries=(0, max))
    yield Metric("Current", current_throughput, 
                    levels=(warn_treshold, crit_treshold),
                    boundaries=(0, max))

    infotext = "Throughput: Current:{}, Peak:{} (Limit:{}Mbps)".format(
        get_traffic_human_readable(current_throughput, "Bit", "Bit"), 
        get_traffic_human_readable(peak_throughput, "Bit", "Bit"), 
        max_throughput
    )

    if current_throughput >= crit_treshold:
        yield Result(state=State.CRIT, summary=infotext)
    elif current_throughput >= warn_treshold:
        yield Result(state=State.WARN, summary=infotext)
    else:
        yield Result(state=State.OK, summary=infotext)


check_plugin_alteon_throughput = CheckPlugin(     
    name='alteon_throughput',
    service_name='%s',
    discovery_function=discover_alteon_throughput,
    check_function=check_alteon_throughput,
    check_ruleset_name='alteon_throughput',
    check_default_parameters={},
)
