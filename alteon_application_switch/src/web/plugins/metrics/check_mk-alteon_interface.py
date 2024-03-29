#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# Copyright (C) 2020 Benjamin Hollentin <me@benji.at>
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
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from cmk.gui.i18n import _

from cmk.gui.plugins.metrics import (
    metric_info,
    check_metrics,
)


metric_info["alteon_if_in_octets"] = {
"title": _("Input Octets"),
"unit": "bytes/s",
"color": "#00e060"
}

metric_info["alteon_if_out_octets"] = {
"title": _("Output Octets"),
"unit": "bytes/s",
"color": "#0080e0"
}

metric_info["alteon_if_in_packets"] = {
"title": _("Input Packets"),
"unit": "1/s",
"color": "#00c080"
}

metric_info["alteon_if_out_packets"] = {
"title": _("Output Packets"),
"unit": "1/s",
"color": "#00c0ff"
}


check_metrics["check_mk-alteon_interface"] = {
    "ifPortStatsInOctetsPerSec": {
        "name": "alteon_if_in_octets"
    },
    "ifPortStatsOutOctetsPerSec": {
        "name": "alteon_if_out_octets"
    },
    "ifPortStatsInPktsPerSec": {
        "name": "alteon_if_in_packets"
    },
    "ifPortStatsOutPktsPerSec": {
        "name": "alteon_if_out_packets"
    },
}
