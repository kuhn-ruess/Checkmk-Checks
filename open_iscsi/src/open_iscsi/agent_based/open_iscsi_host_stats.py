#!/usr/bin/env python3
# Copyright (C) 2017  Frank Fegert (fra.nospam.nk@gmx.de)
# Updates and refactoring 2020 by Bastian Kuhn (mail@bastian-kuhn.de)
# Migration to cmk.agent_based.v2 / cmk.rulesets.v1 by Kuhn & Ruess GmbH
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
"""Open-iSCSI iSOE host statistics check.

Example agent output:
  <<<open-iscsi_host_stats>>>
  [host stats 84:8f:69:35:fc:70 iqn.2000-04.com.qlogic:isp8214.000e1e37da2c.4]
  mactx_frames: 2920663232
  mactx_bytes: 16009348359436
  ...
"""

import time

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Metric,
    Result,
    Service,
    State,
    StringTable,
    get_rate,
    get_value_store,
    render,
)

# Ordered list of (description, counter) pairs. The order is preserved so
# the summary line keeps the same layout as the legacy check.
HOST_STATS_COUNTERS = [
    ('MAC TX Frames', 'mactx_frames'),
    ('MAC TX Bytes', 'mactx_bytes'),
    ('MAC TX Multicast Frames', 'mactx_multicast_frames'),
    ('MAC TX Broadcast Frames', 'mactx_broadcast_frames'),
    ('MAC TX Pause Frames', 'mactx_pause_frames'),
    ('MAC TX Control Frames', 'mactx_control_frames'),
    ('MAC TX Deferral', 'mactx_deferral'),
    ('MAC TX Excess Deferral', 'mactx_excess_deferral'),
    ('MAC TX Late Collision', 'mactx_late_collision'),
    ('MAC TX Abort', 'mactx_abort'),
    ('MAC TX Single Collision', 'mactx_single_collision'),
    ('MAC TX Multiple Collision', 'mactx_multiple_collision'),
    ('MAC TX Collision', 'mactx_collision'),
    ('MAC TX Dropped Frames', 'mactx_frames_dropped'),
    ('MAC TX Jumbo Frames', 'mactx_jumbo_frames'),
    ('MAC RX Frames', 'macrx_frames'),
    ('MAC RX Bytes', 'macrx_bytes'),
    ('MAC RX Unknown Control Frames', 'macrx_unknown_control_frames'),
    ('MAC RX Pause Frames', 'macrx_pause_frames'),
    ('MAC RX Control Frames', 'macrx_control_frames'),
    ('MAC RX Dribble', 'macrx_dribble'),
    ('MAC RX Frame Length Error', 'macrx_frame_length_error'),
    ('MAC RX Jabber', 'macrx_jabber'),
    ('MAC RX Carrier Sense Error', 'macrx_carrier_sense_error'),
    ('MAC RX Discarded Frames', 'macrx_frame_discarded'),
    ('MAC RX Dropped Frames', 'macrx_frames_dropped'),
    ('MAC CRC Error', 'mac_crc_error'),
    ('MAC Encoding Error', 'mac_encoding_error'),
    ('MAC RX Length Error Large', 'macrx_length_error_large'),
    ('MAC RX Length Error Small', 'macrx_length_error_small'),
    ('MAC RX Multicast Frames', 'macrx_multicast_frames'),
    ('MAC RX Broadcast Frames', 'macrx_broadcast_frames'),
    ('IP TX Packets', 'iptx_packets'),
    ('IP TX Bytes', 'iptx_bytes'),
    ('IP TX Fragments', 'iptx_fragments'),
    ('IP RX Packets', 'iprx_packets'),
    ('IP RX Bytes', 'iprx_bytes'),
    ('IP RX Fragments', 'iprx_fragments'),
    ('IP Datagram Assy', 'ip_datagram_reassembly'),
    ('IP Address Error', 'ip_invalid_address_error'),
    ('IP Error Packets', 'ip_error_packets'),
    ('IP Fragmentation Overlap', 'ip_fragrx_overlap'),
    ('IP Fragmentation Out-of-order', 'ip_fragrx_outoforder'),
    ('IP Datagram Reassembly Timeout', 'ip_datagram_reassembly_timeout'),
    ('IPv6 TX Packets', 'ipv6tx_packets'),
    ('IPv6 TX Bytes', 'ipv6tx_bytes'),
    ('IPv6 TX Fragments', 'ipv6tx_fragments'),
    ('IPv6 RX Packets', 'ipv6rx_packets'),
    ('IPv6 RX Bytes', 'ipv6rx_bytes'),
    ('IPv6 RX Fragments', 'ipv6rx_fragments'),
    ('IPv6 Datagram Assy', 'ipv6_datagram_reassembly'),
    ('IPv6 Address Error', 'ipv6_invalid_address_error'),
    ('IPv6 Error Packets', 'ipv6_error_packets'),
    ('IPv6 Fragmentation Overlap', 'ipv6_fragrx_overlap'),
    ('IPv6 Fragmentation Out-of-order', 'ipv6_fragrx_outoforder'),
    ('IPv6 Datagram Reassembly Timeout', 'ipv6_datagram_reassembly_timeout'),
    ('TCP TX Segments', 'tcptx_segments'),
    ('TCP TX Bytes', 'tcptx_bytes'),
    ('TCP RX Segments', 'tcprx_segments'),
    ('TCP RX Bytes', 'tcprx_byte'),
    ('TCP Duplicate ACK Retransmit', 'tcp_duplicate_ack_retx'),
    ('TCP Retransmit Timer Expired', 'tcp_retx_timer_expired'),
    ('TCP RX Duplicate ACK', 'tcprx_duplicate_ack'),
    ('TCP RX Pure ACK', 'tcprx_pure_ackr'),
    ('TCP TX Delayed ACK', 'tcptx_delayed_ack'),
    ('TCP TX Pure ACK', 'tcptx_pure_ack'),
    ('TCP RX Segment Error', 'tcprx_segment_error'),
    ('TCP RX Segment Out-of-order', 'tcprx_segment_outoforder'),
    ('TCP RX Window Probe', 'tcprx_window_probe'),
    ('TCP RX Window Update', 'tcprx_window_update'),
    ('TCP TX Window Probe Persist', 'tcptx_window_probe_persist'),
    ('ECC Error Correction', 'ecc_error_correction'),
    ('iSCSI TX PDU', 'iscsi_pdu_tx'),
    ('iSCSI TX Bytes', 'iscsi_data_bytes_tx'),
    ('iSCSI RX PDU', 'iscsi_pdu_rx'),
    ('iSCSI RX Bytes', 'iscsi_data_bytes_rx'),
    ('iSCSI I/O Completed', 'iscsi_io_completed'),
    ('iSCSI I/O Unexpected', 'iscsi_unexpected_io_rx'),
    ('iSCSI Format Error', 'iscsi_format_error'),
    ('iSCSI Header Digest (CRC) Error', 'iscsi_hdr_digest_error'),
    ('iSCSI Data Digest (CRC) Error', 'iscsi_data_digest_error'),
    ('iSCSI Sequence Error', 'iscsi_sequence_error'),
]

MESSAGE_LINE_COUNTERS = {
    'mactx_bytes', 'macrx_bytes', 'iptx_bytes', 'iprx_bytes', 'ipv6tx_bytes',
    'ipv6rx_bytes', 'tcptx_bytes', 'tcprx_byte', 'iscsi_data_bytes_tx',
    'iscsi_data_bytes_rx',
}

ERROR_COUNTERS = {
    'mactx_collision', 'mactx_frames_dropped', 'macrx_frame_length_error',
    'macrx_carrier_sense_error', 'macrx_frame_discarded', 'macrx_frames_dropped',
    'mac_crc_error', 'mac_encoding_error', 'macrx_length_error_large',
    'macrx_length_error_small', 'ip_invalid_address_error', 'ip_error_packets',
    'ip_fragrx_overlap', 'ip_fragrx_outoforder', 'ip_datagram_reassembly_timeout',
    'ipv6_invalid_address_error', 'ipv6_error_packets', 'ipv6_fragrx_overlap',
    'ipv6_fragrx_outoforder', 'ipv6_datagram_reassembly_timeout',
    'tcp_duplicate_ack_retx', 'tcp_retx_timer_expired', 'tcprx_segment_error',
    'tcprx_segment_outoforder', 'ecc_error_correction', 'iscsi_format_error',
    'iscsi_hdr_digest_error', 'iscsi_data_digest_error', 'iscsi_sequence_error',
}


def parse_open_iscsi_host_stats(string_table: StringTable) -> dict:
    hosts: dict = {}
    mac_host = None
    for line in string_table:
        if len(line) >= 4 and line[0] == "[host" and line[1] == "stats":
            mac_host = " ".join(line[2:4])[:-1]
            hosts[mac_host] = {}
        elif len(line) == 2 and mac_host is not None:
            counter = line[0].replace(":", "")
            hosts[mac_host][counter] = line[1]
    return hosts


def discover_open_iscsi_host_stats(section: dict) -> DiscoveryResult:
    for host in section:
        yield Service(item=host)


def check_open_iscsi_host_stats(item: str, params: dict, section: dict) -> CheckResult:
    if item not in section:
        return
    counters = section[item]
    host_id = item.replace(" ", "_")
    value_store = get_value_store()
    this_time = time.time()

    message = ""
    status = State.OK
    sum_errors = 0

    for descr, counter in HOST_STATS_COUNTERS:
        if counter not in counters:
            continue
        try:
            t_value = int(counters[counter])
        except ValueError:
            continue
        value_rate = get_rate(
            value_store,
            "%s.%s" % (counter, host_id),
            this_time,
            t_value,
        )

        if counter in MESSAGE_LINE_COUNTERS:
            if message:
                message += ", "
            message += "%s: %s/s" % (descr, render.bytes(value_rate))

        levels = params.get(counter)
        warn = crit = None
        if isinstance(levels, tuple) and levels[0] == "fixed":
            warn, crit = levels[1]

        if crit is not None and crit > 0 and value_rate >= crit:
            message += ", %s: %s/s (!!)" % (descr, value_rate)
            status = State.worst(status, State.CRIT)
        elif warn is not None and warn > 0 and value_rate >= warn:
            message += ", %s: %s/s (!)" % (descr, value_rate)
            status = State.worst(status, State.WARN)
        elif counter in ERROR_COUNTERS:
            sum_errors += value_rate
            if value_rate > 0:
                message += ", %s: %s/s" % (descr, value_rate)

        yield Metric(counter, value_rate)

    if sum_errors == 0:
        message += ", no protocol errors"

    yield Result(state=status, summary="Host Stats: " + message)


agent_section_open_iscsi_host_stats = AgentSection(
    name="open_iscsi_host_stats",
    parse_function=parse_open_iscsi_host_stats,
)

check_plugin_open_iscsi_host_stats = CheckPlugin(
    name="open_iscsi_host_stats",
    service_name="iSCSI Host Stats %s",
    discovery_function=discover_open_iscsi_host_stats,
    check_function=check_open_iscsi_host_stats,
    check_default_parameters={},
    check_ruleset_name="open_iscsi_host_stats",
)
