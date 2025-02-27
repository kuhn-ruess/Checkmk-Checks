#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""


from cmk.graphing.v1.graphs import Graph, Title


graph_sidecooler_warm = Graph(
    name = "sidecooler_warm",
    title = Title("Temperatures warm side"),
    simple_lines = [
        "temp_warm_mean",
        "temp_warm_top",
        "temp_warm_center",
        "temp_warm_bottom",
    ],
)

graph_sidecooler_cold = Graph(
    name = "sidecooler_cold",
    title = Title("Temperatures cold side"),
    simple_lines = [
        "temp_cold_mean",
        "temp_cold_top",
        "temp_cold_center",
        "temp_cold_bottom",
    ],
)

graph_sidecooler_coldwater = Graph(
    name = "sidecooler_coldwater",
    title = Title("Coldwater temperature"),
    simple_lines = [
        "coldwater_supply",
        "coldwater_return",
    ],
)
