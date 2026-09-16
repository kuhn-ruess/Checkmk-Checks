#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.graphing.v1.graphs import Graph
from cmk.graphing.v1.metrics import Color, DecimalNotation, Metric, Title, Unit
from cmk.graphing.v1.perfometers import Closed, FocusRange, Open, Perfometer

UNIT_NUMBER = Unit(DecimalNotation(""))
UNIT_PERCENT = Unit(DecimalNotation("%"))
UNIT_DBM = Unit(DecimalNotation("dBm"))


metric_aruba_ap_clients = Metric(
    name = "aruba_ap_clients",
    title = Title("Connected clients"),
    unit = UNIT_NUMBER,
    color = Color.BLUE,
)

metric_aruba_radio_utilization = Metric(
    name = "aruba_radio_utilization",
    title = Title("Channel utilization"),
    unit = UNIT_PERCENT,
    color = Color.ORANGE,
)

metric_aruba_radio_tx_power = Metric(
    name = "aruba_radio_tx_power",
    title = Title("TX power"),
    unit = UNIT_DBM,
    color = Color.GREEN,
)

metric_aruba_aps_up = Metric(
    name = "aruba_aps_up",
    title = Title("Access points up"),
    unit = UNIT_NUMBER,
    color = Color.GREEN,
)

metric_aruba_aps_down = Metric(
    name = "aruba_aps_down",
    title = Title("Access points down"),
    unit = UNIT_NUMBER,
    color = Color.RED,
)

metric_aruba_clients = Metric(
    name = "aruba_clients",
    title = Title("Wireless clients"),
    unit = UNIT_NUMBER,
    color = Color.BLUE,
)

metric_aruba_api_rate_remaining = Metric(
    name = "aruba_api_rate_remaining",
    title = Title("Remaining API calls"),
    unit = UNIT_NUMBER,
    color = Color.PURPLE,
)


graph_aruba_aps = Graph(
    name = "aruba_aps",
    title = Title("Access points"),
    simple_lines = ["aruba_aps_up", "aruba_aps_down"],
)


perfometer_aruba_radio_utilization = Perfometer(
    name = "aruba_radio_utilization",
    focus_range = FocusRange(Closed(0), Closed(100)),
    segments = ["aruba_radio_utilization"],
)

perfometer_aruba_ap_clients = Perfometer(
    name = "aruba_ap_clients",
    focus_range = FocusRange(Closed(0), Open(50)),
    segments = ["aruba_ap_clients"],
)

perfometer_aruba_clients = Perfometer(
    name = "aruba_clients",
    focus_range = FocusRange(Closed(0), Open(500)),
    segments = ["aruba_clients"],
)
