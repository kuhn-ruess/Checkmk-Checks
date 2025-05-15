#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.graphing.v1.metrics import Color, DecimalNotation, IECNotation, Metric, Title, Unit

metric_info_pure_1_datareduction = Metric(
    name="pure_1_datareduction",
    title=Title("Data reduction for volume"),
    unit=Unit(DecimalNotation("")),
    color=Color.PURPLE,
)

metric_info_pure_2_totalreduction = Metric(
    name="pure_2_totalreduction",
    title=Title("Total reduction for volume"),
    unit=Unit(DecimalNotation("")),
    color=Color.PINK,
)

metric_info_pure_3_thinprovisioned = Metric(
    name="pure_3_thinprovisioned",
    title=Title("Thin Provisioned space"),
    unit=Unit(DecimalNotation("")),
    color=Color.ORANGE,
)

metric_info_pure_4_snaphots = Metric(
    name="pure_4_snapshots",
    title=Title("Space in use for snapshots"),
    unit=Unit(IECNotation("B")),
    color=Color.BROWN,
)
