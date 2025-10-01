#!/usr/bin/env python3

from cmk.graphing.v1 import Title
from cmk.graphing.v1.metrics import Metric, Unit, SINotation, DecimalNotation, Color, WarningOf, CriticalOf
from cmk.graphing.v1.graphs import Graph

metric_used_metadata_space_pct = Metric(
    name="used_metadata_space_pct",
    title=Title("Used Metadata Space %"),
    unit=Unit(DecimalNotation("%")),
    color=Color.PURPLE,
)

metric_avail_metadata_space = Metric(
    name="avail_metadata_space",
    title=Title("Available Metadata Space"),
    unit=Unit(SINotation("B")),
    color=Color.BLUE,
)

metric_percent_used = Metric(
    name="percent_used",
    title=Title("Used Storage %"),
    unit=Unit(DecimalNotation("%")),
    color=Color.PURPLE,
)

metric_used_storage = Metric(
    name="used_storage",
    title=Title("Used Storage"),
    unit=Unit(SINotation("B")),
    color=Color.BLUE,
)

graph_used_metadata_space_pct = Graph(
    name = "used_metadata_space_pct",
    title = Title("Used Metadata Space %"),
    compound_lines = ["used_metadata_space_pct"],
    simple_lines=(
        WarningOf("used_metadata_space_pct"),
        CriticalOf("used_metadata_space_pct"),
    ),
)

graph_avail_metadata_space = Graph(
    name = "avail_metadata_space",
    title = Title("Available Metadata Space"),
    compound_lines = ["avail_metadata_space"],
)

graph_percent_used = Graph(
    name = "percent_used",
    title = Title("Used Storage %"),
    compound_lines = ["percent_used"],
    simple_lines=(
        WarningOf("percent_used"),
        CriticalOf("percent_used"),
    ),
)

graph_used_storage = Graph(
    name = "used_storage",
    title = Title("Used Storage"),
    compound_lines = ["used_storage"],
    simple_lines=(
        WarningOf("used_storage"),
        CriticalOf("used_storage"),
    ),
)

