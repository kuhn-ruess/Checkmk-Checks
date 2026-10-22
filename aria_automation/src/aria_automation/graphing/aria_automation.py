#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.graphing.v1 import Title
from cmk.graphing.v1.metrics import Color, DecimalNotation, IECNotation, Metric, Unit

metric_aria_cpu_percent = Metric(
    name="aria_cpu_percent",
    title=Title("CPU usage"),
    unit=Unit(DecimalNotation("%")),
    color=Color.BLUE,
)

metric_aria_memory_bytes = Metric(
    name="aria_memory_bytes",
    title=Title("Memory usage"),
    unit=Unit(IECNotation("B")),
    color=Color.GREEN,
)

metric_aria_disk_bytes = Metric(
    name="aria_disk_bytes",
    title=Title("Disk usage"),
    unit=Unit(IECNotation("B")),
    color=Color.ORANGE,
)

metric_aria_instances = Metric(
    name="aria_instances",
    title=Title("Service instances"),
    unit=Unit(DecimalNotation("")),
    color=Color.PURPLE,
)
