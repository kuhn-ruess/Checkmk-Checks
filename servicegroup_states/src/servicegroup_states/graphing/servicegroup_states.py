#!/usr/bin/env python3

"""
Service Group States Graphing

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.graphing.v1 import Title
from cmk.graphing.v1.graphs import Graph, MinimalRange
from cmk.graphing.v1.metrics import Color, DecimalNotation, Metric, StrictPrecision, Unit
from cmk.graphing.v1.perfometers import Closed, FocusRange, Open, Perfometer

UNIT_COUNT = Unit(DecimalNotation(""), StrictPrecision(0))

metric_servicegroup_services = Metric(
    name="servicegroup_services",
    title=Title("Services in group"),
    unit=UNIT_COUNT,
    color=Color.BLUE,
)

metric_servicegroup_services_problem = Metric(
    name="servicegroup_services_problem",
    title=Title("Services in a problem state"),
    unit=UNIT_COUNT,
    color=Color.RED,
)

metric_servicegroup_services_stale = Metric(
    name="servicegroup_services_stale",
    title=Title("Stale services"),
    unit=UNIT_COUNT,
    color=Color.ORANGE,
)

graph_servicegroup_states = Graph(
    name="servicegroup_states",
    title=Title("Service group members"),
    minimal_range=MinimalRange(0, 10),
    simple_lines=["servicegroup_services"],
    compound_lines=[
        "servicegroup_services_problem",
        "servicegroup_services_stale",
    ],
)

perfometer_servicegroup_states = Perfometer(
    name="servicegroup_states",
    focus_range=FocusRange(Closed(0), Open(10)),
    segments=["servicegroup_services_problem", "servicegroup_services_stale"],
)
