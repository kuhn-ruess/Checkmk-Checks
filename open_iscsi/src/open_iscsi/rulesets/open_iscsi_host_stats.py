#!/usr/bin/env python3
# Copyright (C) 2017  Frank Fegert (fra.nospam.nk@gmx.de)
# Migration to cmk.rulesets.v1 by Kuhn & Ruess GmbH
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
"""WATO ruleset for the Open-iSCSI iSOE host statistics check."""

from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    Integer,
    LevelDirection,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic

# (key, title, unit) for every host statistics counter. Order follows the
# legacy check output.
_HOST_STATS_PARAMS = [
    ("mactx_frames", "Transmitted MAC/Layer2 frames", "Frames/sec"),
    ("macrx_frames", "Received MAC/Layer2 frames", "Frames/sec"),
    ("mactx_bytes", "Transmitted MAC/Layer2 bytes", "Bytes/sec"),
    ("macrx_bytes", "Received MAC/Layer2 bytes", "Bytes/sec"),
    ("mactx_multicast_frames", "Transmitted MAC multicast frames", "Frames/sec"),
    ("macrx_multicast_frames", "Received MAC multicast frames", "Frames/sec"),
    ("mactx_broadcast_frames", "Transmitted MAC broadcast frames", "Frames/sec"),
    ("macrx_broadcast_frames", "Received MAC broadcast frames", "Frames/sec"),
    ("mactx_pause_frames", "Transmitted MAC pause frames", "Frames/sec"),
    ("macrx_pause_frames", "Received MAC pause frames", "Frames/sec"),
    ("mactx_control_frames", "Transmitted MAC control frames", "Frames/sec"),
    ("macrx_control_frames", "Received MAC control frames", "Frames/sec"),
    ("mactx_frames_dropped", "Transmitted MAC dropped frames", "Frames/sec"),
    ("macrx_frames_dropped", "Received MAC dropped frames", "Frames/sec"),
    ("mactx_deferral", "MAC TX deferral", "Frames/sec"),
    ("mactx_excess_deferral", "MAC TX excess deferral", "Frames/sec"),
    ("mactx_abort", "MAC TX abort", "Frames/sec"),
    ("mactx_jumbo_frames", "Transmitted MAC jumbo frames", "Frames/sec"),
    ("mactx_late_collision", "MAC TX late collision", "Frames/sec"),
    ("mactx_single_collision", "MAC TX single collision", "Frames/sec"),
    ("mactx_multiple_collision", "MAC TX multiple collision", "Frames/sec"),
    ("mactx_collision", "MAC TX collision", "Frames/sec"),
    ("macrx_unknown_control_frames", "Received MAC unknown control frames", "Frames/sec"),
    ("macrx_dribble", "MAC RX dribble", "Frames/sec"),
    ("macrx_frame_length_error", "MAC RX frame length error", "Frames/sec"),
    ("macrx_frame_discarded", "MAC RX discarded frames", "Frames/sec"),
    ("macrx_jabber", "MAC RX jabber", "Frames/sec"),
    ("macrx_carrier_sense_error", "MAC RX carrier sense error", "Errors/sec"),
    ("mac_crc_error", "MAC CRC error", "Errors/sec"),
    ("mac_encoding_error", "MAC encoding error", "Errors/sec"),
    ("macrx_length_error_large", "MAC RX length error large", "Errors/sec"),
    ("macrx_length_error_small", "MAC RX length error small", "Errors/sec"),
    ("iptx_packets", "Transmitted IP packets", "Packets/sec"),
    ("iprx_packets", "Received IP packets", "Packets/sec"),
    ("iptx_bytes", "Transmitted IP bytes", "Bytes/sec"),
    ("iprx_bytes", "Received IP bytes", "Bytes/sec"),
    ("iptx_fragments", "Transmitted IP fragments", "Fragments/sec"),
    ("iprx_fragments", "Received IP fragments", "Fragments/sec"),
    ("ip_datagram_reassembly", "IP datagram reassembly", "Packets/sec"),
    ("ip_invalid_address_error", "IP invalid address error", "Errors/sec"),
    ("ip_error_packets", "IP error packets", "Errors/sec"),
    ("ip_fragrx_overlap", "IP fragmentation overlap", "Errors/sec"),
    ("ip_fragrx_outoforder", "IP fragmentation out-of-order", "Errors/sec"),
    ("ip_datagram_reassembly_timeout", "IP datagram reassembly timeout", "Timeouts/sec"),
    ("ipv6tx_packets", "Transmitted IPv6 packets", "Packets/sec"),
    ("ipv6rx_packets", "Received IPv6 packets", "Packets/sec"),
    ("ipv6tx_bytes", "Transmitted IPv6 bytes", "Bytes/sec"),
    ("ipv6rx_bytes", "Received IPv6 bytes", "Bytes/sec"),
    ("ipv6tx_fragments", "Transmitted IPv6 fragments", "Fragments/sec"),
    ("ipv6rx_fragments", "Received IPv6 fragments", "Fragments/sec"),
    ("ipv6_datagram_reassembly", "IPv6 datagram reassembly", "Packets/sec"),
    ("ipv6_invalid_address_error", "IPv6 invalid address error", "Errors/sec"),
    ("ipv6_error_packets", "IPv6 error packets", "Errors/sec"),
    ("ipv6_fragrx_overlap", "IPv6 fragmentation overlap", "Errors/sec"),
    ("ipv6_fragrx_outoforder", "IPv6 fragmentation out-of-order", "Errors/sec"),
    ("ipv6_datagram_reassembly_timeout", "IPv6 datagram reassembly timeout", "Timeouts/sec"),
    ("tcptx_segments", "Transmitted TCP segments", "Segments/sec"),
    ("tcprx_segments", "Received TCP segments", "Segments/sec"),
    ("tcptx_bytes", "Transmitted TCP bytes", "Bytes/sec"),
    ("tcprx_byte", "Received TCP bytes", "Bytes/sec"),
    ("tcp_duplicate_ack_retx", "TCP duplicate ACK retransmit", "Segments/sec"),
    ("tcp_retx_timer_expired", "TCP retransmit timer expired", "Segments/sec"),
    ("tcprx_duplicate_ack", "TCP RX duplicate ACK", "Segments/sec"),
    ("tcprx_pure_ackr", "TCP RX pure ACK", "Segments/sec"),
    ("tcptx_delayed_ack", "TCP TX delayed ACK", "Segments/sec"),
    ("tcptx_pure_ack", "TCP TX pure ACK", "Segments/sec"),
    ("tcprx_segment_error", "TCP RX segment error", "Segments/sec"),
    ("tcprx_segment_outoforder", "TCP RX segment out-of-order", "Segments/sec"),
    ("tcprx_window_probe", "TCP RX window probe", "Segments/sec"),
    ("tcprx_window_update", "TCP RX window update", "Segments/sec"),
    ("tcptx_window_probe_persist", "TCP TX window probe persist", "Segments/sec"),
    ("iscsi_pdu_tx", "Transmitted iSCSI PDUs", "PDUs/sec"),
    ("iscsi_pdu_rx", "Received iSCSI PDUs", "PDUs/sec"),
    ("iscsi_data_bytes_tx", "Transmitted iSCSI bytes", "Bytes/sec"),
    ("iscsi_data_bytes_rx", "Received iSCSI bytes", "Bytes/sec"),
    ("iscsi_io_completed", "iSCSI I/O completed", "IO/sec"),
    ("iscsi_unexpected_io_rx", "iSCSI I/O unexpected", "IO/sec"),
    ("iscsi_format_error", "iSCSI format error", "Errors/sec"),
    ("iscsi_hdr_digest_error", "iSCSI header digest (CRC) error", "Errors/sec"),
    ("iscsi_data_digest_error", "iSCSI data digest (CRC) error", "Errors/sec"),
    ("iscsi_sequence_error", "iSCSI sequence error", "Errors/sec"),
    ("ecc_error_correction", "ECC error correction", "Corrections/sec"),
]


def _make_elements() -> dict:
    elements = {}
    for key, title, unit in _HOST_STATS_PARAMS:
        elements[key] = DictElement(
            parameter_form=SimpleLevels(
                title=Title("%s") % title,
                help_text=Help("Levels for %s (%s).") % (title.lower(), unit),
                form_spec_template=Integer(unit_symbol=unit),
                level_direction=LevelDirection.UPPER,
                prefill_fixed_levels=DefaultValue((0, 0)),
            ),
        )
    return elements


def _parameter_form() -> Dictionary:
    return Dictionary(
        help_text=Help("The levels for the Open-iSCSI host statistics values."),
        elements=_make_elements(),
    )


rule_spec_open_iscsi_host_stats = CheckParameters(
    name="open_iscsi_host_stats",
    title=Title("Open-iSCSI Host Statistics"),
    topic=Topic.STORAGE,
    parameter_form=_parameter_form,
    condition=HostAndItemCondition(
        item_title=Title("MAC address and iSOE host name")
    ),
)
