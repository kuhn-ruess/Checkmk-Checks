#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.graphing.v1.metrics import Color, DecimalNotation, IECNotation, Metric, Title, Unit

metric_exasol_db_size = Metric(
    name="exasol_db_size",
    title=Title("Exasol Database size"),
    unit=Unit(IECNotation("B")),
    color=Color.PURPLE,
)

metric_exasol_db_size_perc = Metric(
    name="exasol_db_size_perc",
    title=Title("Exasol Database percentage"),
    unit=Unit(DecimalNotation("%")),
    color=Color.PURPLE,
)
