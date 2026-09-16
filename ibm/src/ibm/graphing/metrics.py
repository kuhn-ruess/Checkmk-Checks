#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.graphing.v1.graphs import Graph
from cmk.graphing.v1.metrics import Color, DecimalNotation, Metric, TimeNotation, Title, Unit
from cmk.graphing.v1.perfometers import Closed, FocusRange, Perfometer

UNIT_NUMBER = Unit(DecimalNotation(""))
UNIT_PERCENT = Unit(DecimalNotation("%"))
UNIT_TIME = Unit(TimeNotation())


metric_tape_slots_used = Metric(
    name = "tape_slots_used",
    title = Title("Used slots"),
    unit = UNIT_NUMBER,
    color = Color.BLUE,
)

metric_tape_slots_free = Metric(
    name = "tape_slots_free",
    title = Title("Free slots"),
    unit = UNIT_NUMBER,
    color = Color.GREEN,
)

metric_tape_slots_utilization = Metric(
    name = "tape_slots_utilization",
    title = Title("Slot utilization"),
    unit = UNIT_PERCENT,
    color = Color.ORANGE,
)

metric_tape_cleaning_cartridges = Metric(
    name = "tape_cleaning_cartridges",
    title = Title("Cleaning cartridges"),
    unit = UNIT_NUMBER,
    color = Color.CYAN,
)

metric_tape_drive_mounts = Metric(
    name = "tape_drive_mounts",
    title = Title("Tape mounts"),
    unit = UNIT_NUMBER,
    color = Color.PURPLE,
)

metric_tape_drive_operating_time = Metric(
    name = "tape_drive_operating_time",
    title = Title("Operating time"),
    unit = UNIT_TIME,
    color = Color.BROWN,
)


graph_tape_slots = Graph(
    name = "tape_slots",
    title = Title("Media slots"),
    simple_lines = ["tape_slots_used", "tape_slots_free"],
)


perfometer_tape_slots_utilization = Perfometer(
    name = "tape_slots_utilization",
    focus_range = FocusRange(Closed(0), Closed(100)),
    segments = ["tape_slots_utilization"],
)

perfometer_tape_drive_mounts = Perfometer(
    name = "tape_drive_mounts",
    focus_range = FocusRange(Closed(0), Closed(10000)),
    segments = ["tape_drive_mounts"],
)
