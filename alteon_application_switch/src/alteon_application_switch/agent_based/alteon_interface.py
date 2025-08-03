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

def if_render_mac_address(ifPhysAddress):
    if not isinstance(ifPhysAddress, list):
        mac_bytes = map(ord, ifPhysAddress)
    else:
        mac_bytes = ifPhysAddress
    return (":".join(["%02s" % hex(m)[2:] for m in mac_bytes]).replace(' ', '0')).upper()

def parse_alteon_interface(string_table):
    interfaces = {}
    indexes = []
    phy_if_index = {}

    # Conversation Arrays
    cv_port_status = [ "up", "down", "testing", "unknown", "dormant", "not present", "lower layer down" ]

    for if_info in string_table[0]:
        index = int(if_info[0])
        indexes.append(index)
        interface = {}

        interface['ifType2'] = "physical" # Default value, might be overwritten
        interface['ifIndex'] = index
        interface['ifType'] = "{}".format(if_info[1])
        interface['ifSpeed'] = int(if_info[2])
        interface['ifPhysAddress'] = if_render_mac_address(if_info[3])
        interface['ifAdminStatus'] = cv_port_status[int(if_info[4])-1]
        interface['ifOperStatus'] = cv_port_status[int(if_info[5])-1]
        interface['ifLastChange'] = int(if_info[6])
        interface['ifInOctets'] = int(if_info[7])
        interface['ifInUcastPkts'] = int(if_info[8])
        interface['ifInNUcastPkts'] = int(if_info[9])
        interface['ifInDiscards'] = int(if_info[10])
        interface['ifInErrors'] = int(if_info[11])
        interface['ifInUnknownProtos'] = int(if_info[12])
        interface['ifOutOctets'] = int(if_info[13])
        interface['ifOutUcastPkts'] = int(if_info[14])
        interface['ifOutNUcastPkts'] = int(if_info[15])
        interface['ifOutDiscards'] = int(if_info[16])
        interface['ifOutErrors'] = int(if_info[17])
        interface['ifOutQLen'] = int(if_info[18])
        interfaces[index] = interface

    for index, if_stats in zip(indexes, string_table[1]):
        interfaces[index]["ifDescription"] = "{}".format(if_stats[0])
        interfaces[index]["ifInMulticastPkts"] = int(if_stats[1])
        interfaces[index]["ifInBroadcastPkts"] = int(if_stats[2])
        interfaces[index]["ifOutMulticastPkts"] = int(if_stats[3])
        interfaces[index]["ifOutBroadcastPkts"] = int(if_stats[4])
        interfaces[index]["ifHCInOctets"] = int(if_stats[5])
        interfaces[index]["ifHCInUcastPkts"] = int(if_stats[6])
        interfaces[index]["ifHCInMulticastPkts"] = int(if_stats[7])
        interfaces[index]["ifHCInBroadcastPkts"] = int(if_stats[8])
        interfaces[index]["ifHCOutOctets"] = int(if_stats[9])
        interfaces[index]["ifHCOutUcastPkts"] = int(if_stats[10])
        interfaces[index]["ifHCOutMulticastPkts"] = int(if_stats[11])
        interfaces[index]["ifHCOutBroadcastPkts"] = int(if_stats[12])
        interfaces[index]["ifLinkUpDownTrapEnable"] = int(if_stats[13])
        interfaces[index]["ifHighSpeed"] = int(if_stats[14])
        interfaces[index]["ifPromiscuousMode"] = int(if_stats[15])
        interfaces[index]["ifConnectorPresent"] = int(if_stats[16])
        interfaces[index]["ifAlias"] = "{}".format(if_stats[17])
        if interfaces[index]["ifDescription"].startswith("Port "):
            port_id = int(interfaces[index]["ifDescription"].split()[1])
            interfaces[index]["ifPortId"] = port_id
            phy_if_index[port_id] = index

    for if_info in string_table[2]:
        # virutal interfaces
        index = int(if_info[0])
        interfaces[index]['ifDescription'] = "{}".format(if_info[1])
        interfaces[index]['ifVLAN'] = int(if_info[2])
        interfaces[index]['ifIPv4'] = if_info[3]
        interfaces[index]['ifIPv6'] = if_info[4]
        interfaces[index]['ifType2'] = "virtual"

    for if_stats in string_table[3]:
        port_id = int(if_stats[0])
        interfaces[phy_if_index[port_id]]['ifPortStatsInOctetsPerSec'] = int(if_stats[1])
        interfaces[phy_if_index[port_id]]['ifPortStatsOutOctetsPerSec'] = int(if_stats[2])
        interfaces[phy_if_index[port_id]]['ifPortStatsInPktsPerSec'] = int(if_stats[3])
        interfaces[phy_if_index[port_id]]['ifPortStatsOutPktsPerSec'] = int(if_stats[4])

    interfaces[999]['ifType2'] = "virtual"
    interfaces[999]['ifDescription'] = "Management"
    return interfaces


snmp_section_alteon_interface = SNMPSection(
    name="alteon_interface",
    detect=startswith('.1.3.6.1.2.1.1.1.0', "Alteon Application Switch"),
    parse_function=parse_alteon_interface,
    fetch=[
        SNMPTree(
            base='.1.3.6.1.2.1.2.2.1',
            oids=[
                '1', # Interface Index
                '2', # Interface Type
                '5', # Interface Speed
                '6', # Interface MAC Address
                '7', # ifAdminStatus (1: up, 2: down, 3: testing)
                '8', # ifOperStatus (1: up, 2: down, 3: testing, 4: unknown, 5: dormant, 6: notPresent, 7: lowerLayerDown)
                '9', # ifLastChange Last changed seconds
                '10', # ifInOctets
                '11', # ifInUcastPkts
                '12', # ifInNUcastPkts
                '13', # ifInDiscards
                '14', # ifInErrors
                '15', # ifInUnknownProtos
                '16', # ifOutOctets
                '17', # ifOutUcastPkts
                '18', # ifOutNUcastPkts
                '19', # ifOutDiscards
                '20', # ifOutErrors
                '21', # ifOutQLen
            ]
        ),
        SNMPTree(
            base='.1.3.6.1.2.1.31.1.1.1',
            oids=[
                '1', # Interface Description (only for physical interfaces)
                '2', # ifInMulticastPkts
                '3', # ifInBroadcastPkts
                '4', # ifOutMulticastPkts
                '5', # ifOutBroadcastPkts
                '6', # ifHCInOctets
                '7', # ifHCInUcastPkts
                '8', # ifHCInMulticastPkts
                '9', # ifHCInBroadcastPkts
                '10', # ifHCOutOctets
                '11', # ifHCOutUcastPkts
                '12', # ifHCOutMulticastPkts
                '13', # ifHCOutBroadcastPkts
                '14', # ifLinkUpDownTrapEnable
                '15', # ifHighSpeed -> Interface Speed (only for physical interfaces)
                '16', # ifPromiscuousMode
                '17', # ifConnectorPresent
                '18', # ifAlias
            ]
        ),
        SNMPTree(
            base='.1.3.6.1.4.1.1872.2.5.3.1.1.2.1',
            oids=[
                '1', # Interface Index
                '14', # Interface Description (only for virtual interfaces)
                '5', # VLAN
                '2', # IPv4
                '10', # IPv6
            ]
        ),
        SNMPTree(
            base='.1.3.6.1.4.1.1872.2.5.1.2.3.2.1',
            oids=[
                '1', # Port Index
                '2', # portStatsInOctetsPerSec Port input octets
                '6', # portStatsOutOctetsPerSec Port output octets per seconds
                '3', # portStatsInPktsPerSec Amount of port input data in packets in the last sec
                '7', # portStatsOutPktsPerSec Amount of port output data in packets in the last sec
            ]
        )
    ],
)


def discover_alteon_interface(section):
    for index, interface in section.items():
        port_num = interface['ifIndex']
        if interface['ifIndex'] == 999:
            port_num = "MGMT"
        elif interface['ifType2'] == "physical":
            port_num = int(interface['ifDescription'].split()[1])        

        service_name = "{} - {} {}".format(
            interface['ifIndex'],
            interface['ifType2'],
            port_num
        )
        if interface['ifHighSpeed'] > 0 or interface['ifType2'] == "virtual" or interface['ifOperStatus'] == "up":
            yield Service(item=service_name)


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
        "T",
    ]
    i = 0
    while speed >= base:
        speed = speed / base
        i = i + 1

    return "{:.4g} {}{}/s".format(speed, units[i], out_unit)


def check_alteon_interface(item, params, section):
    this_time = time.time()
    value_store = get_value_store()

    continuous_counter = [
        'ifHCInOctets',
        'ifHCInUcastPkts',
        'ifHCOutOctets',
        'ifHCOutUcastPkts',
        'ifInNUcastPkts',
        'ifInDiscards',
        'ifOutNUcastPkts',
        'ifOutDiscards',
    ]
    performancedata_keys = [
        'ifHCInOctets',
        'ifHCInUcastPkts',
        'ifHCOutOctets',
        'ifHCOutUcastPkts',
        'ifInNUcastPkts',
        'ifInDiscards',
        'ifInErrors',
        'ifOutNUcastPkts',
        'ifOutDiscards',
        'ifOutErrors',
        'ifSpeed',
        'ifPortStatsInOctetsPerSec',
        'ifPortStatsOutOctetsPerSec',
        'ifPortStatsInPktsPerSec',
        'ifPortStatsOutPktsPerSec',
        'ifLastChange',
        'ifInUnknownProtos',
        'ifOutQLen'
    ]

    interface_id = int(item.split()[0])
    interface = section[interface_id]
    perfdata = {}
    infotext = ""
    wrapped = False

    for key, value in interface.items():

        # get value for coninuous counter
        if key in continuous_counter:
            try:
                value = get_rate(value_store, "Alteon_IF.{}.{}.{}".format(interface['ifPhysAddress'], interface_id, key), this_time, value, raise_overflow=True)
            except GetRateError:
                value = None

        if value is not None:
            infotext = "{}\n{}: {}".format(
                infotext,
                key,
                value
            )

        if key in performancedata_keys:
            perfdata[key] = value

    perfdata_final = [
        ('in', perfdata['ifHCInOctets']),
        ('inucast',  perfdata['ifHCInUcastPkts']),
        ('innucast', perfdata['ifInNUcastPkts']),
        ('indisc', perfdata['ifInDiscards']),
        ('inerr', perfdata['ifInErrors']),
        ('out', perfdata['ifHCOutOctets']),
        ('outucast', perfdata['ifHCOutUcastPkts']),
        ('outnucast', perfdata['ifOutNUcastPkts']),
        ('outdisc', perfdata['ifOutDiscards']),
        ('outerr', perfdata['ifOutErrors']),
        ('outqlen', perfdata['ifOutQLen']),
    ]
    if 'ifPortStatsInOctetsPerSec' in perfdata:
        perfdata_final.append(('ifPortStatsInOctetsPerSec', perfdata['ifPortStatsInOctetsPerSec']))
        perfdata_final.append(('ifPortStatsOutOctetsPerSec', perfdata['ifPortStatsOutOctetsPerSec']))
        perfdata_final.append(('ifPortStatsInPktsPerSec', perfdata['ifPortStatsInPktsPerSec']))
        perfdata_final.append(('ifPortStatsOutPktsPerSec', perfdata['ifPortStatsOutPktsPerSec']))
    else:
        perfdata_final.append(('ifPortStatsInOctetsPerSec', 0))
        perfdata_final.append(('ifPortStatsOutOctetsPerSec', 0))
        perfdata_final.append(('ifPortStatsInPktsPerSec', 0))
        perfdata_final.append(('ifPortStatsOutPktsPerSec', 0))

    for perf_key, perf_value in perfdata_final:
        yield Metric(perf_key, perf_value)

    errors_in = 0
    if perfdata['ifHCInOctets'] > 0:
        errors_in = perfdata['ifInErrors'] * 100 / perfdata['ifHCInOctets']

    errors_out = 0
    if perfdata['ifHCOutOctets'] > 0:
        errors_out = perfdata['ifOutErrors'] * 100 / perfdata['ifHCOutOctets']

    if interface['ifHighSpeed'] == 0:
        speed = "speed unknown"
    else:
        speed = get_traffic_human_readable(interface['ifHighSpeed'] * 1000 * 1000, "Bit", "Bit")

    infotext = "[{}] - [{}]({}) MAC: {} {}, In: {} ({}), Out: {} ({}){}".format(
        interface['ifDescription'],
        # Type
        interface['ifType'],
        # State
        interface['ifOperStatus'],
        # MAC
        interface['ifPhysAddress'],
        # Speed
        speed,
        # Bits in
        "{}".format(get_traffic_human_readable(perfdata['ifHCInOctets'], "Byte", "Bit")),
        # Errors in %
        "{}%".format(errors_in),
        # Bits out
        "{}".format(get_traffic_human_readable(perfdata['ifHCOutOctets'], "Byte", "Bit")),
        # Errors out %
        "{}%".format(errors_out),
        # 
        infotext
    )
    yield Result(state=State.OK, summary=infotext)


check_plugin_alteon_interface = CheckPlugin(
    name='alteon_interface',
    service_name='Alteon IF %s',
    discovery_function=discover_alteon_interface,
    check_function=check_alteon_interface,
    # NOTE: This ruleset exists, but the check function above does not
    #       do anything with the parameters. Migrated anyway.
    check_ruleset_name='alteon_throughput',
    check_default_parameters={},
)
