#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.graphing.v1.perfometers import Perfometer, FocusRange, Closed, Open


perfometer_quota_used = Perfometer(
    name = "quota_used",
    focus_range = FocusRange(Closed(1000000000000), Open(20000000000000)),
    segments=["quota_used_bytes"],
)
