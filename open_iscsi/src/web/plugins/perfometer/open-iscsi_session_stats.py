#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# Copyright (C) 2017  Frank Fegert (fra.nospam.nk@gmx.de)
#
# Check_MK perf-o-meter script to display the current data transfer
# rate of Open-iSCSI sessions.
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

def perfometer_check_mk_open_iscsi_session_stats(row, check_command, perf_data):
    # Uncomment and restart Apache to debug:
    #return repr(perf_data), ''
    # Data sample:  
    # [
    #    ...
    #    (u'rxdata_octets', u'204.7'),
    #    (u'txdata_octets', u'0'),
    #    ...
    # ]
    text = ""
    for perf_item in perf_data:
        metric = perf_item[0]
        value = perf_item[1]
        if (metric == "rxdata_octets"):
            in_traffic = value
        if (metric == "txdata_octets"):
            out_traffic = value

    return perfometer_bandwidth(in_traffic, out_traffic, 0, 0)

perfometers["check_mk-open-iscsi_session_stats"] = perfometer_check_mk_open_iscsi_session_stats

#
# EOF
