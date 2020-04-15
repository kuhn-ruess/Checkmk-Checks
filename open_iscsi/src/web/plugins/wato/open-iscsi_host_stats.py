#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# Copyright (C) 2017  Frank Fegert (fra.nospam.nk@gmx.de)
#
# WATO plugin for the parametrization of the threshold values used
# by the "open-iscsi_host_stats" Check_MK check script.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

register_check_parameters(
    subgroup_storage,
    "open-iscsi_host_stats",
    _("Open-iSCSI Host Statistics"),
    Dictionary(
        help = _("The levels for the Open-iSCSI host statistics values."),
        title = _("The levels for the Open-iSCSI host statistics values"),
        elements = [
            # MAC/Layer2 statistics
            ( "mactx_frames",
              Tuple(
                help = _("The levels for the number of transmitted MAC/Layer2 frames on an iSOE host."),
                title = _("The levels for the number of transmitted MAC/Layer2 frames on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Frames/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Frames/sec"), default_value = 0),
                ]),
            ),
            ( "macrx_frames",
              Tuple(
                help = _("The levels for the number of received MAC/Layer2 frames on an iSOE host."),
                title = _("The levels for the number of received MAC/Layer2 frames on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Frames/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Frames/sec"), default_value = 0),
                ]),
            ),
            ( "mactx_bytes",
              Tuple(
                help = _("The levels for the number of transmitted MAC/Layer2 bytes on an iSOE host."),
                title = _("The levels for the number of transmitted MAC/Layer2 bytes on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Bytes/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Bytes/sec"), default_value = 0),
                ]),
            ),
            ( "macrx_bytes",
              Tuple(
                help = _("The levels for the number of received MAC/Layer2 bytes on an iSOE host."),
                title = _("The levels for the number of received MAC/Layer2 bytes on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Bytes/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Bytes/sec"), default_value = 0),
                ]),
            ),
            ( "mactx_multicast_frames",
              Tuple(
                help = _("The levels for the number of transmitted MAC/Layer2 multicast frames on an iSOE host."),
                title = _("The levels for the number of transmitted MAC/Layer2 multicast frames on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Frames/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Frames/sec"), default_value = 0),
                ]),
            ),
            ( "macrx_multicast_frames",
              Tuple(
                help = _("The levels for the number of received MAC/Layer2 multicast frames on an iSOE host."),
                title = _("The levels for the number of received MAC/Layer2 multicast frames on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Frames/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Frames/sec"), default_value = 0),
                ]),
            ),
            ( "mactx_broadcast_frames",
              Tuple(
                help = _("The levels for the number of transmitted MAC/Layer2 broadcast frames on an iSOE host."),
                title = _("The levels for the number of transmitted MAC/Layer2 broadcast frames on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Frames/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Frames/sec"), default_value = 0),
                ]),
            ),
            ( "macrx_broadcast_frames",
              Tuple(
                help = _("The levels for the number of received MAC/Layer2 broadcast frames on an iSOE host."),
                title = _("The levels for the number of received MAC/Layer2 broadcast frames on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Frames/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Frames/sec"), default_value = 0),
                ]),
            ),
            ( "mactx_pause_frames",
              Tuple(
                help = _("The levels for the number of transmitted MAC/Layer2 pause frames on an iSOE host."),
                title = _("The levels for the number of transmitted MAC/Layer2 pause frames on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Frames/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Frames/sec"), default_value = 0),
                ]),
            ),
            ( "macrx_pause_frames",
              Tuple(
                help = _("The levels for the number of received MAC/Layer2 pause frames on an iSOE host."),
                title = _("The levels for the number of received MAC/Layer2 pause frames on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Frames/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Frames/sec"), default_value = 0),
                ]),
            ),
            ( "mactx_control_frames",
              Tuple(
                help = _("The levels for the number of transmitted MAC/Layer2 control frames on an iSOE host."),
                title = _("The levels for the number of transmitted MAC/Layer2 control frames on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Frames/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Frames/sec"), default_value = 0),
                ]),
            ),
            ( "macrx_control_frames",
              Tuple(
                help = _("The levels for the number of received MAC/Layer2 control frames on an iSOE host."),
                title = _("The levels for the number of received MAC/Layer2 control frames on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Frames/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Frames/sec"), default_value = 0),
                ]),
            ),
            ( "mactx_frames_dropped",
              Tuple(
                help = _("The levels for the number of transmitted MAC/Layer2 dropped frames on an iSOE host."),
                title = _("The levels for the number of transmitted MAC/Layer2 dropped frames on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Frames/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Frames/sec"), default_value = 0),
                ]),
            ),
            ( "macrx_frames_dropped",
              Tuple(
                help = _("The levels for the number of received MAC/Layer2 dropped frames on an iSOE host."),
                title = _("The levels for the number of received MAC/Layer2 dropped frames on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Frames/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Frames/sec"), default_value = 0),
                ]),
            ),
            ( "mactx_deferral",
              Tuple(
                help = _("The levels for the number of transmitted MAC/Layer2 deferral frames on an iSOE host."),
                title = _("The levels for the number of transmitted MAC/Layer2 deferral frames on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Frames/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Frames/sec"), default_value = 0),
                ]),
            ),
            ( "mactx_excess_deferral",
              Tuple(
                help = _("The levels for the number of transmitted MAC/Layer2 deferral frames on an iSOE host."),
                title = _("The levels for the number of transmitted MAC/Layer2 deferral frames on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Frames/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Frames/sec"), default_value = 0),
                ]),
            ),
            ( "mactx_abort",
              Tuple(
                help = _("The levels for the number of transmitted MAC/Layer2 abort frames on an iSOE host."),
                title = _("The levels for the number of transmitted MAC/Layer2 abort frames on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Frames/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Frames/sec"), default_value = 0),
                ]),
            ),
            ( "mactx_jumbo_frames",
              Tuple(
                help = _("The levels for the number of transmitted MAC/Layer2 jumbo frames on an iSOE host."),
                title = _("The levels for the number of transmitted MAC/Layer2 jumbo frames on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Frames/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Frames/sec"), default_value = 0),
                ]),
            ),
            ( "mactx_late_collision",
              Tuple(
                help = _("The levels for the number of MAC/Layer2 late transmit collisions on an iSOE host."),
                title = _("The levels for the number of MAC/Layer2 late transmit collisions on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Frames/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Frames/sec"), default_value = 0),
                ]),
            ),
            ( "mactx_single_collision",
              Tuple(
                help = _("The levels for the number of MAC/Layer2 single transmit collisions on an iSOE host."),
                title = _("The levels for the number of MAC/Layer2 single transmit collisions on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Frames/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Frames/sec"), default_value = 0),
                ]),
            ),
            ( "mactx_multiple_collision",
              Tuple(
                help = _("The levels for the number of MAC/Layer2 multiple transmit collisions on an iSOE host."),
                title = _("The levels for the number of MAC/Layer2 multiple transmit collisions on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Frames/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Frames/sec"), default_value = 0),
                ]),
            ),
            ( "mactx_collision",
              Tuple(
                help = _("The levels for the number of MAC/Layer2 collisions on an iSOE host."),
                title = _("The levels for the number of MAC/Layer2 collisions on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Frames/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Frames/sec"), default_value = 0),
                ]),
            ),
            ( "macrx_unknown_control_frames",
              Tuple(
                help = _("The levels for the number of received MAC/Layer2 control frames on an iSOE host."),
                title = _("The levels for the number of received MAC/Layer2 control frames on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Frames/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Frames/sec"), default_value = 0),
                ]),
            ),
            ( "macrx_dribble",
              Tuple(
                help = _("The levels for the number of received MAC/Layer2 dribble on an iSOE host."),
                title = _("The levels for the number of received MAC/Layer2 dribble on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Frames/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Frames/sec"), default_value = 0),
                ]),
            ),
            ( "macrx_frame_length_error",
              Tuple(
                help = _("The levels for the number of received MAC/Layer2 frame length errors on an iSOE host."),
                title = _("The levels for the number of received MAC/Layer2 frame length errors on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Frames/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Frames/sec"), default_value = 0),
                ]),
            ),
            ( "macrx_frame_discarded",
              Tuple(
                help = _("The levels for the number of discarded received MAC/Layer2 frames on an iSOE host."),
                title = _("The levels for the number of discarded received MAC/Layer2 frames on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Frames/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Frames/sec"), default_value = 0),
                ]),
            ),
            ( "macrx_jabber",
              Tuple(
                help = _("The levels for the number of received MAC/Layer2 jabber on an iSOE host."),
                title = _("The levels for the number of received MAC/Layer2 jabber on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Frames/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Frames/sec"), default_value = 0),
                ]),
            ),
            ( "macrx_carrier_sense_error",
              Tuple(
                help = _("The levels for the number of received MAC/Layer2 carrier sense errors on an iSOE host."),
                title = _("The levels for the number of received MAC/Layer2 carrier sense errors on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Errors/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Errors/sec"), default_value = 0),
                ]),
            ),
            ( "mac_crc_error",
              Tuple(
                help = _("The levels for the number of received MAC/Layer2 CRC errors on an iSOE host."),
                title = _("The levels for the number of received MAC/Layer2 CRC errors on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Errors/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Errors/sec"), default_value = 0),
                ]),
            ),
            ( "mac_encoding_error",
              Tuple(
                help = _("The levels for the number of received MAC/Layer2 encoding errors on an iSOE host."),
                title = _("The levels for the number of received MAC/Layer2 encoding errors on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Errors/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Errors/sec"), default_value = 0),
                ]),
            ),
            ( "macrx_length_error_large",
              Tuple(
                help = _("The levels for the number of received MAC/Layer2 length too large errors on an iSOE host."),
                title = _("The levels for the number of received MAC/Layer2 length too large errors on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Errors/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Errors/sec"), default_value = 0),
                ]),
            ),
            ( "macrx_length_error_small",
              Tuple(
                help = _("The levels for the number of received MAC/Layer2 length too small errors on an iSOE host."),
                title = _("The levels for the number of received MAC/Layer2 length too small errors on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Errors/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Errors/sec"), default_value = 0),
                ]),
            ),
            # IP/Layer3 statistics
            ( "iptx_packets",
              Tuple(
                help = _("The levels for the number of transmitted IP packets on an iSOE host."),
                title = _("The levels for the number of transmitted IP packets on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Packets/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Packets/sec"), default_value = 0),
                ]),
            ),
            ( "iprx_packets",
              Tuple(
                help = _("The levels for the number of received IP packets on an iSOE host."),
                title = _("The levels for the number of received IP packets on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Packets/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Packets/sec"), default_value = 0),
                ]),
            ),
            ( "iptx_bytes",
              Tuple(
                help = _("The levels for the number of transmitted IP bytes on an iSOE host."),
                title = _("The levels for the number of transmitted IP bytes on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Bytes/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Bytes/sec"), default_value = 0),
                ]),
            ),
            ( "iprx_bytes",
              Tuple(
                help = _("The levels for the number of received IP bytes on an iSOE host."),
                title = _("The levels for the number of received IP bytes on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Bytes/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Bytes/sec"), default_value = 0),
                ]),
            ),
            ( "iptx_fragments",
              Tuple(
                help = _("The levels for the number of transmitted IP fragments on an iSOE host."),
                title = _("The levels for the number of transmitted IP fragments on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Fragments/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Fragments/sec"), default_value = 0),
                ]),
            ),
            ( "iprx_fragments",
              Tuple(
                help = _("The levels for the number of received IP fragments on an iSOE host."),
                title = _("The levels for the number of received IP fragments on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Fragments/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Fragments/sec"), default_value = 0),
                ]),
            ),
            ( "ip_datagram_reassembly",
              Tuple(
                help = _("The levels for the number of IP datagram reassemblies on an iSOE host."),
                title = _("The levels for the number of IP datagram reassemblies on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Packets/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Packets/sec"), default_value = 0),
                ]),
            ),
            ( "ip_invalid_address_error",
              Tuple(
                help = _("The levels for the number of IP invalid address errors on an iSOE host."),
                title = _("The levels for the number of IP invalid address errors on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Errors/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Errors/sec"), default_value = 0),
                ]),
            ),
            ( "ip_error_packets",
              Tuple(
                help = _("The levels for the number of IP packet errors on an iSOE host."),
                title = _("The levels for the number of IP packet errors on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Errors/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Errors/sec"), default_value = 0),
                ]),
            ),
            ( "ip_fragrx_overlap",
              Tuple(
                help = _("The levels for the number of IP fragmentation overlaps on an iSOE host."),
                title = _("The levels for the number of IP fragmentation overlaps on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Errors/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Errors/sec"), default_value = 0),
                ]),
            ),
            ( "ip_fragrx_outoforder",
              Tuple(
                help = _("The levels for the number of IP fragmentation out-of-order on an iSOE host."),
                title = _("The levels for the number of IP fragmentation out-of-order on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Errors/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Errors/sec"), default_value = 0),
                ]),
            ),
            ( "ip_datagram_reassembly_timeout",
              Tuple(
                help = _("The levels for the number of IP datagram reassembly timeouts on an iSOE host."),
                title = _("The levels for the number of IP datagram reassembly timeouts on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Timeouts/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Timeouts/sec"), default_value = 0),
                ]),
            ),
            # IPv6/Layer3 statistics
            ( "ipv6tx_packets",
              Tuple(
                help = _("The levels for the number of transmitted IPv6 packets on an iSOE host."),
                title = _("The levels for the number of transmitted IPv6 packets on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Packets/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Packets/sec"), default_value = 0),
                ]),
            ),
            ( "ipv6rx_packets",
              Tuple(
                help = _("The levels for the number of received IPv6 packets on an iSOE host."),
                title = _("The levels for the number of received IPv6 packets on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Packets/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Packets/sec"), default_value = 0),
                ]),
            ),
            ( "ipv6tx_bytes",
              Tuple(
                help = _("The levels for the number of transmitted IPv6 bytes on an iSOE host."),
                title = _("The levels for the number of transmitted IPv6 bytes on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Bytes/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Bytes/sec"), default_value = 0),
                ]),
            ),
            ( "ipv6rx_bytes",
              Tuple(
                help = _("The levels for the number of received IPv6 bytes on an iSOE host."),
                title = _("The levels for the number of received IPv6 bytes on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Bytes/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Bytes/sec"), default_value = 0),
                ]),
            ),
            ( "ipv6tx_fragments",
              Tuple(
                help = _("The levels for the number of transmitted IPv6 fragments on an iSOE host."),
                title = _("The levels for the number of transmitted IPv6 fragments on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Fragments/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Fragments/sec"), default_value = 0),
                ]),
            ),
            ( "ipv6rx_fragments",
              Tuple(
                help = _("The levels for the number of received IPv6 fragments on an iSOE host."),
                title = _("The levels for the number of received IPv6 fragments on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Fragments/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Fragments/sec"), default_value = 0),
                ]),
            ),
            ( "ipv6_datagram_reassembly",
              Tuple(
                help = _("The levels for the number of IPv6 datagram reassemblies on an iSOE host."),
                title = _("The levels for the number of IPv6 datagram reassemblies on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Packets/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Packets/sec"), default_value = 0),
                ]),
            ),
            ( "ipv6_invalid_address_error",
              Tuple(
                help = _("The levels for the number of IPv6 invalid address errors on an iSOE host."),
                title = _("The levels for the number of IPv6 invalid address errors on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Errors/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Errors/sec"), default_value = 0),
                ]),
            ),
            ( "ipv6_error_packets",
              Tuple(
                help = _("The levels for the number of IPv6 packet errors on an iSOE host."),
                title = _("The levels for the number of IPv6 packet errors on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Errors/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Errors/sec"), default_value = 0),
                ]),
            ),
            ( "ipv6_fragrx_overlap",
              Tuple(
                help = _("The levels for the number of IPv6 fragmentation overlaps on an iSOE host."),
                title = _("The levels for the number of IPv6 fragmentation overlaps on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Errors/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Errors/sec"), default_value = 0),
                ]),
            ),
            ( "ipv6_fragrx_outoforder",
              Tuple(
                help = _("The levels for the number of IPv6 fragmentation out-of-order on an iSOE host."),
                title = _("The levels for the number of IPv6 fragmentation out-of-order on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Errors/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Errors/sec"), default_value = 0),
                ]),
            ),
            ( "ipv6_datagram_reassembly_timeout",
              Tuple(
                help = _("The levels for the number of IPv6 datagram reassembly timeouts on an iSOE host."),
                title = _("The levels for the number of IPv6 datagram reassembly timeouts on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Timeouts/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Timeouts/sec"), default_value = 0),
                ]),
            ),
            # TCP/Layer4 statistics
            ( "tcptx_segments",
              Tuple(
                help = _("The levels for the number of transmitted TCP segments on an iSOE host."),
                title = _("The levels for the number of transmitted TCP segments on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Segments/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Segments/sec"), default_value = 0),
                ]),
            ),
            ( "tcprx_segments",
              Tuple(
                help = _("The levels for the number of received TCP segments on an iSOE host."),
                title = _("The levels for the number of received TCP segments on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Segments/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Segments/sec"), default_value = 0),
                ]),
            ),
            ( "tcptx_bytes",
              Tuple(
                help = _("The levels for the number of transmitted TCP bytes on an iSOE host."),
                title = _("The levels for the number of transmitted TCP bytes on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Bytes/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Bytes/sec"), default_value = 0),
                ]),
            ),
            ( "tcprx_byte",
              Tuple(
                help = _("The levels for the number of received TCP bytes on an iSOE host."),
                title = _("The levels for the number of received TCP bytes on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Bytes/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Bytes/sec"), default_value = 0),
                ]),
            ),
            ( "tcp_duplicate_ack_retx",
              Tuple(
                help = _("The levels for the number of duplicate TCP ACK retransmits on an iSOE host."),
                title = _("The levels for the number of duplicate TCP ACK retransmits on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Segments/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Segments/sec"), default_value = 0),
                ]),
            ),
            ( "tcp_retx_timer_expired",
              Tuple(
                help = _("The levels for the number of TCP retransmit timer expiries on an iSOE host."),
                title = _("The levels for the number of received TCP retransmit timer expiries on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Segments/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Segments/sec"), default_value = 0),
                ]),
            ),
            ( "tcprx_duplicate_ack",
              Tuple(
                help = _("The levels for the number of received TCP duplicate ACKs on an iSOE host."),
                title = _("The levels for the number of received TCP duplicate ACKs on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Segments/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Segments/sec"), default_value = 0),
                ]),
            ),
            ( "tcprx_pure_ackr",
              Tuple(
                help = _("The levels for the number of received TCP pure ACKs on an iSOE host."),
                title = _("The levels for the number of received TCP pure ACKs on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Segments/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Segments/sec"), default_value = 0),
                ]),
            ),
            ( "tcptx_delayed_ack",
              Tuple(
                help = _("The levels for the number of transmitted TCP delayed ACKs on an iSOE host."),
                title = _("The levels for the number of transmitted TCP delayed ACKs on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Segments/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Segments/sec"), default_value = 0),
                ]),
            ),
            ( "tcptx_pure_ack",
              Tuple(
                help = _("The levels for the number of transmitted TCP pure ACKs on an iSOE host."),
                title = _("The levels for the number of transmitted TCP pure ACKs on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Segments/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Segments/sec"), default_value = 0),
                ]),
            ),
            ( "tcprx_segment_error",
              Tuple(
                help = _("The levels for the number of received TCP segment errors on an iSOE host."),
                title = _("The levels for the number of received TCP segment errors on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Segments/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Segments/sec"), default_value = 0),
                ]),
            ),
            ( "tcprx_segment_outoforder",
              Tuple(
                help = _("The levels for the number of received TCP segment out-of-order on an iSOE host."),
                title = _("The levels for the number of received TCP segment out-of-order on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Segments/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Segments/sec"), default_value = 0),
                ]),
            ),
            ( "tcprx_window_probe",
              Tuple(
                help = _("The levels for the number of received TCP window probe on an iSOE host."),
                title = _("The levels for the number of received TCP window probe on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Segments/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Segments/sec"), default_value = 0),
                ]),
            ),
            ( "tcprx_window_update",
              Tuple(
                help = _("The levels for the number of received TCP window update on an iSOE host."),
                title = _("The levels for the number of received TCP window update on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Segments/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Segments/sec"), default_value = 0),
                ]),
            ),
            ( "tcptx_window_probe_persist",
              Tuple(
                help = _("The levels for the number of transmitted TCP window probe persist on an iSOE host."),
                title = _("The levels for the number of transmitted TCP window probe persist on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Segments/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Segments/sec"), default_value = 0),
                ]),
            ),
            # iSCSI statistics
            ( "iscsi_pdu_tx",
              Tuple(
                help = _("The levels for the number of transmitted iSCSI PDUs on an iSOE host."),
                title = _("The levels for the number of transmitted iSCSI PDUs on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("PDUs/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("PDUs/sec"), default_value = 0),
                ]),
            ),
            ( "iscsi_pdu_rx",
              Tuple(
                help = _("The levels for the number of received iSCSI PDUs on an iSOE host."),
                title = _("The levels for the number of received iSCSI PDUs on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("PDUs/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("PDUs/sec"), default_value = 0),
                ]),
            ),
            ( "iscsi_data_bytes_tx",
              Tuple(
                help = _("The levels for the number of transmitted iSCSI Bytes on an iSOE host."),
                title = _("The levels for the number of transmitted iSCSI Bytes on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Bytes/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Bytes/sec"), default_value = 0),
                ]),
            ),
            ( "iscsi_data_bytes_rx",
              Tuple(
                help = _("The levels for the number of received iSCSI Bytes on an iSOE host."),
                title = _("The levels for the number of received iSCSI Bytes on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Bytes/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Bytes/sec"), default_value = 0),
                ]),
            ),
            ( "iscsi_io_completed",
              Tuple(
                help = _("The levels for the number of iSCSI I/Os completed on an iSOE host."),
                title = _("The levels for the number of iSCSI I/Os completed on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("IO/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("IO/sec"), default_value = 0),
                ]),
            ),
            ( "iscsi_unexpected_io_rx",
              Tuple(
                help = _("The levels for the number of iSCSI unexpected I/Os on an iSOE host."),
                title = _("The levels for the number of iSCSI unexpected I/Os on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("IO/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("IO/sec"), default_value = 0),
                ]),
            ),
            ( "iscsi_format_error",
              Tuple(
                help = _("The levels for the number of iSCSI format errors on an iSOE host."),
                title = _("The levels for the number of iSCSI format errors on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Errors/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Errors/sec"), default_value = 0),
                ]),
            ),
            ( "iscsi_hdr_digest_error",
              Tuple(
                help = _("The levels for the number of iSCSI header digest (CRC) errors on an iSOE host."),
                title = _("The levels for the number of iSCSI header digest (CRC) errors on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Errors/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Errors/sec"), default_value = 0),
                ]),
            ),
            ( "iscsi_data_digest_error",
              Tuple(
                help = _("The levels for the number of iSCSI data digest (CRC) errors on an iSOE host."),
                title = _("The levels for the number of iSCSI data digest (CRC) errors on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Errors/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Errors/sec"), default_value = 0),
                ]),
            ),
            ( "iscsi_sequence_error",
              Tuple(
                help = _("The levels for the number of iSCSI sequence errors on an iSOE host."),
                title = _("The levels for the number of iSCSI sequence errors on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Errors/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Errors/sec"), default_value = 0),
                ]),
            ),
            # iSOE statistics
            ( "ecc_error_correction",
              Tuple(
                help = _("The levels for the number of ECC error corrections on an iSOE host."),
                title = _("The levels for the number of ECC error corrections on an iSOE host."),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Corrections/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Corrections/sec"), default_value = 0),
                ]),
            ),
        ]
    ),
    None,
    "dict"
) 
