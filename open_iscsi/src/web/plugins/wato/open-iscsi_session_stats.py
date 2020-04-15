#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# Copyright (C) 2017  Frank Fegert (fra.nospam.nk@gmx.de)
#
# WATO plugin for the parametrization of the threshold values used
# by the "open-iscsi_session_stats" Check_MK check script.
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
    "open-iscsi_session_stats",
    _("Open-iSCSI Session Statistics"),
    Dictionary(
        help = _("The levels for the Open-iSCSI session statistics values."),
        title = _("The levels for the Open-iSCSI session statistics values"),
        elements = [
            ( "txdata_octets",
              Tuple(
                help = _("The levels for the number of transmitted bytes in an Open-iSCSI session."),
                title = _("The levels for the number of transmitted bytes in an Open-iSCSI session"),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Bytes/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Bytes/sec"), default_value = 0),
                ]),
            ),
            ( "rxdata_octets",
              Tuple(
                help = _("The levels for the number of received bytes in an Open-iSCSI session."),
                title = _("The levels for the number of received bytes in an Open-iSCSI session"),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("Bytes/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("Bytes/sec"), default_value = 0),
                ]),
            ),
            ( "digest_err",
              Tuple(
                help = _("The levels for the number of digest (CRC) errors in an Open-iSCSI session."),
                title = _("The levels for the number of digest (CRC) errors in an Open-iSCSI session"),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("PDUs/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("PDUs/sec"), default_value = 0),
                ]),
            ),
            ( "timeout_err",
              Tuple(
                help = _("The levels for the number of timeout errors in an Open-iSCSI session."),
                title = _("The levels for the number of timeout errors in an Open-iSCSI session"),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("PDUs/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("PDUs/sec"), default_value = 0),
                ]),
            ),
            ( "noptx_pdus",
              Tuple(
                help = _("The levels for the number of transmitted NOP commands in an Open-iSCSI session."),
                title = _("The levels for the number of transmitted NOP commands in an Open-iSCSI session"),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("PDUs/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("PDUs/sec"), default_value = 0),
                ]),
            ),
            ( "noprx_pdus",
              Tuple(
                help = _("The levels for the number of received NOP commands in an Open-iSCSI session."),
                title = _("The levels for the number of received NOP commands in an Open-iSCSI session"),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("PDUs/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("PDUs/sec"), default_value = 0),
                ]),
            ),
            ( "scsicmd_pdus",
              Tuple(
                help = _("The levels for the number of transmitted SCSI command requests in an Open-iSCSI session."),
                title = _("The levels for the number of transmitted SCSI command requests in an Open-iSCSI session"),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("PDUs/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("PDUs/sec"), default_value = 0),
                ]),
            ),
            ( "scsirsp_pdus",
              Tuple(
                help = _("The levels for the number of received SCSI command reponses in an Open-iSCSI session."),
                title = _("The levels for the number of received SCSI command reponses in an Open-iSCSI session"),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("PDUs/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("PDUs/sec"), default_value = 0),
                ]),
            ),
            ( "tmfcmd_pdus",
              Tuple(
                help = _("The levels for the number of transmitted task management function commands in an Open-iSCSI session."),
                title = _("The levels for the number of transmitted task management function commands in an Open-iSCSI session"),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("PDUs/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("PDUs/sec"), default_value = 0),
                ]),
            ),
            ( "tmfrsp_pdus",
              Tuple(
                help = _("The levels for the number of received task management function responses in an Open-iSCSI session."),
                title = _("The levels for the number of received task management function responses in an Open-iSCSI session"),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("PDUs/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("PDUs/sec"), default_value = 0),
                ]),
            ),
            ( "login_pdus",
              Tuple(
                help = _("The levels for the number of transmitted login requests in an Open-iSCSI session."),
                title = _("The levels for the number of transmitted login requests in an Open-iSCSI session"),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("PDUs/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("PDUs/sec"), default_value = 0),
                ]),
            ),
            ( "logout_pdus",
              Tuple(
                help = _("The levels for the number of transmitted logout requests in an Open-iSCSI session."),
                title = _("The levels for the number of transmitted logout requests in an Open-iSCSI session"),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("PDUs/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("PDUs/sec"), default_value = 0),
                ]),
            ),
            ( "logoutrsp_pdus",
              Tuple(
                help = _("The levels for the number of received logout responses in an Open-iSCSI session."),
                title = _("The levels for the number of received logout responses in an Open-iSCSI session"),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("PDUs/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("PDUs/sec"), default_value = 0),
                ]),
            ),
            ( "text_pdus",
              Tuple(
                help = _("The levels for the number of transmitted text PDUs in an Open-iSCSI session."),
                title = _("The levels for the number of transmitted text PDUs in an Open-iSCSI session"),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("PDUs/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("PDUs/sec"), default_value = 0),
                ]),
            ),
            ( "textrsp_pdus",
              Tuple(
                help = _("The levels for the number of received text PDUs in an Open-iSCSI session."),
                title = _("The levels for the number of received text PDUs in an Open-iSCSI session"),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("PDUs/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("PDUs/sec"), default_value = 0),
                ]),
            ),
            ( "dataout_pdus",
              Tuple(
                help = _("The levels for the number of transmitted data PDUs in an Open-iSCSI session."),
                title = _("The levels for the number of transmitted data PDUs in an Open-iSCSI session"),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("PDUs/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("PDUs/sec"), default_value = 0),
                ]),
            ),
            ( "datain_pdus",
              Tuple(
                help = _("The levels for the number of received data PDUs in an Open-iSCSI session."),
                title = _("The levels for the number of received data PDUs in an Open-iSCSI session"),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("PDUs/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("PDUs/sec"), default_value = 0),
                ]),
            ),
            ( "snack_pdus",
              Tuple(
                help = _("The levels for the number of transmitted single negative ACKs in an Open-iSCSI session."),
                title = _("The levels for the number of transmitted single negative ACKs in an Open-iSCSI session"),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("PDUs/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("PDUs/sec"), default_value = 0),
                ]),
            ),
            ( "r2t_pdus",
              Tuple(
                help = _("The levels for the number of received ready to transfer PDUs in an Open-iSCSI session."),
                title = _("The levels for the number of received ready to transfer PDUs in an Open-iSCSI session"),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("PDUs/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("PDUs/sec"), default_value = 0),
                ]),
            ),
            ( "rjt_pdus",
              Tuple(
                help = _("The levels for the number of received reject PDUs in an Open-iSCSI session."),
                title = _("The levels for the number of received reject PDUs in an Open-iSCSI session"),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("PDUs/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("PDUs/sec"), default_value = 0),
                ]),
            ),
            ( "async_pdus",
              Tuple(
                help = _("The levels for the number of received asynchronous messages in an Open-iSCSI session."),
                title = _("The levels for the number of received asynchronous messages in an Open-iSCSI session"),
                elements = [
                    Integer(title = _("Warning if above"), unit = _("PDUs/sec"), default_value = 0),
                    Integer(title = _("Critical if above"), unit = _("PDUs/sec"), default_value = 0),
                ]),
            ),
        ]
    ),
    None,
    "dict"
)
