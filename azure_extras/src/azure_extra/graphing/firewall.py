#!/usr/bin/env python3
"""
Azure Extra firewall metrics

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
from cmk.graphing.v1 import Title
from cmk.graphing.v1.metrics import (
    Color,
    DecimalNotation,
    Metric,
    SINotation,
    StrictPrecision,
    Unit,
)
from cmk.graphing.v1.perfometers import Closed, FocusRange, Open, Perfometer

metric_firewall_health = Metric(
    name="firewall_health",
    title=Title("Firewall health"),
    unit=Unit(DecimalNotation("%")),
    color=Color.GREEN,
)

metric_networkrulehit = Metric(
    name="networkrulehit",
    title=Title("Network rule hits per minute"),
    unit=Unit(DecimalNotation("/min"), StrictPrecision(0)),
    color=Color.ORANGE,
)

metric_throughput = Metric(
    name="throughput",
    title=Title("Firewall throughput"),
    unit=Unit(SINotation("bit/s")),
    color=Color.BLUE,
)

perfometer_firewall_health = Perfometer(
    name="firewall_health",
    focus_range=FocusRange(Closed(0), Closed(100)),
    segments=["firewall_health"],
)
