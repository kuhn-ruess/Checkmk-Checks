#!/usr/bin/env python3
# Copyright (C) 2017  Frank Fegert (fra.nospam.nk@gmx.de)
# Migration to cmk.graphing.v1 by Kuhn & Ruess GmbH
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
"""Perfometers for the Open-iSCSI host and session statistics checks."""

from cmk.graphing.v1.perfometers import (
    Bidirectional,
    Closed,
    FocusRange,
    Open,
    Perfometer,
)

perfometer_open_iscsi_host_stats = Bidirectional(
    name="open_iscsi_host_stats",
    left=Perfometer(
        name="open_iscsi_host_stats_rx",
        focus_range=FocusRange(Closed(0), Open(10000000)),
        segments=["macrx_bytes"],
    ),
    right=Perfometer(
        name="open_iscsi_host_stats_tx",
        focus_range=FocusRange(Closed(0), Open(10000000)),
        segments=["mactx_bytes"],
    ),
)

perfometer_open_iscsi_session_stats = Bidirectional(
    name="open_iscsi_session_stats",
    left=Perfometer(
        name="open_iscsi_session_stats_rx",
        focus_range=FocusRange(Closed(0), Open(10000000)),
        segments=["rxdata_octets"],
    ),
    right=Perfometer(
        name="open_iscsi_session_stats_tx",
        focus_range=FocusRange(Closed(0), Open(10000000)),
        segments=["txdata_octets"],
    ),
)
