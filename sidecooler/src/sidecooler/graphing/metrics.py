#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""


from cmk.graphing.v1.metrics import Metric, Title, Color, Unit, DecimalNotation, StrictPrecision


UNIT_NUMBER = Unit(DecimalNotation(""), StrictPrecision(1))


metric_temp_warm_mean = Metric(
    name = "temp_warm_mean",
    title = Title("Warm side mean temperature"),
    unit = UNIT_NUMBER,
    color = Color.RED,
)

metric_temp_warm_top = Metric(
    name = "temp_warm_top",
    title = Title("Warm side top temperature"),
    unit = UNIT_NUMBER,
    color = Color.ORANGE,
)

metric_temp_warm_center = Metric(
    name = "temp_warm_center",
    title = Title("Warm side center temperature"),
    unit = UNIT_NUMBER,
    color = Color.GREEN,
)

metric_temp_warm_bottom = Metric(
    name = "temp_warm_bottom",
    title = Title("Warm side bottom temperature"),
    unit = UNIT_NUMBER,
    color = Color.BLUE,
)

metric_temp_cold_mean = Metric(
    name = "temp_cold_mean",
    title = Title("Cold side mean temperature"),
    unit = UNIT_NUMBER,
    color = Color.RED,
)

metric_temp_cold_top = Metric(
    name = "temp_cold_top",
    title = Title("Cold side top temperature"),
    unit = UNIT_NUMBER,
    color = Color.ORANGE,
)

metric_temp_cold_center = Metric(
    name = "temp_cold_center",
    title = Title("Cold side center temperature"),
    unit = UNIT_NUMBER,
    color =  Color.GREEN,
)

metric_temp_cold_bottom = Metric(
    name = "temp_cold_bottom",
    title = Title("Cold side bottom temperature"),
    unit = UNIT_NUMBER,
    color = Color.BLUE,
)

metric_coldwater_supply = Metric(
    name = "coldwater_supply",
    title = Title("Coldwater supply"),
    unit = UNIT_NUMBER,
    color = Color.BLUE,
)

metric_coldwater_return = Metric(
    name = "coldwater_return",
    title = Title("Coldwater return"),
    unit = UNIT_NUMBER,
    color = Color.RED,
)
