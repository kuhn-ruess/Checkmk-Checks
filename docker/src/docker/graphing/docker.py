#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.graphing.v1.metrics import Metric, Title, Color, Unit, DecimalNotation, SINotation, StrictPrecision

UNIT_NUMBER = Unit(DecimalNotation(""), StrictPrecision(1))
BYTES = Unit(SINotation("bytes"))

metric_cpu_pct = Metric(
    name = "CPU_pct",
    title = Title("CPU percentage"),
    unit = UNIT_NUMBER,
    color = Color.RED,
)

metric_memory_limit = Metric(
    name = "Memory_limit",
    title = Title("Memory limit"),
    unit = BYTES,
    color = Color.ORANGE,
)

metric_memory_used = Metric(
    name = "Memory_used",
    title = Title("Memory used"),
    unit = BYTES,
    color = Color.GREEN,
)

metric_sizerootfs = Metric(
    name = "SizeRootFs",
    title = Title("Size of rootfs"),
    unit = BYTES,
    color = Color.BLUE,
)

metric_sizerw = Metric(
    name = "SizeRw",
    title = Title("Size of RW"),
    unit = BYTES,
    color = Color.PURPLE,
)

from cmk.graphing.v1.graphs import Graph, Title

graph_docker_container_memory = Graph(
    name = "docker_container_memory",
    title = Title("Memory"),
    simple_lines = [
        "Memory_limit",
        "Memory_used",
    ],
)
