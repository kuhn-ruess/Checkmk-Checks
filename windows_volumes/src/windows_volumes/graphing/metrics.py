#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.graphing.v1 import Title
from cmk.graphing.v1.metrics import (
    Color,
    DecimalNotation,
    IECNotation,
    Metric,
    Unit,
)
from cmk.graphing.v1.perfometers import Closed, FocusRange, Perfometer
from cmk.graphing.v1.graphs import Graph, MinimalRange

UNIT_BYTES = Unit(IECNotation("B"))
UNIT_PERCENT = Unit(DecimalNotation("%"))


metric_windows_volume_used = Metric(
    name="windows_volume_used",
    title=Title("Used space"),
    unit=UNIT_BYTES,
    color=Color.BLUE,
)

metric_windows_volume_size = Metric(
    name="windows_volume_size",
    title=Title("Total size"),
    unit=UNIT_BYTES,
    color=Color.GRAY,
)

metric_windows_volume_used_percent = Metric(
    name="windows_volume_used_percent",
    title=Title("Used space %"),
    unit=UNIT_PERCENT,
    color=Color.GREEN,
)


perfometer_windows_volume_used_percent = Perfometer(
    name="windows_volume_used_percent",
    focus_range=FocusRange(Closed(0), Closed(100)),
    segments=["windows_volume_used_percent"],
)


graph_windows_volume_usage = Graph(
    name="windows_volume_usage",
    title=Title("Filesystem usage"),
    minimal_range=MinimalRange(0, "windows_volume_size"),
    compound_lines=["windows_volume_used"],
    simple_lines=["windows_volume_size"],
)
