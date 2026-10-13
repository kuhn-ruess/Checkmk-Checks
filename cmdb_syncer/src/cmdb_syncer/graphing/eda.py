#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.graphing.v1 import Title
from cmk.graphing.v1.graphs import Graph
from cmk.graphing.v1.metrics import Color, DecimalNotation, Metric, StrictPrecision, Unit

UNIT_COUNT = Unit(DecimalNotation(""), StrictPrecision(0))

metric_cmdb_syncer_eda_repeating = Metric(
    name = "cmdb_syncer_eda_repeating",
    title = Title("Repeating events"),
    unit = UNIT_COUNT,
    color = Color.RED,
)

metric_cmdb_syncer_eda_repeating_hosts = Metric(
    name = "cmdb_syncer_eda_repeating_hosts",
    title = Title("Hosts with repeating events"),
    unit = UNIT_COUNT,
    color = Color.ORANGE,
)

metric_cmdb_syncer_eda_failing = Metric(
    name = "cmdb_syncer_eda_failing",
    title = Title("Failing events"),
    unit = UNIT_COUNT,
    color = Color.DARK_RED,
)

metric_cmdb_syncer_eda_pending = Metric(
    name = "cmdb_syncer_eda_pending",
    title = Title("Pending events"),
    unit = UNIT_COUNT,
    color = Color.YELLOW,
)

metric_cmdb_syncer_eda_events_24h = Metric(
    name = "cmdb_syncer_eda_events_24h",
    title = Title("Events sent in the last 24 hours"),
    unit = UNIT_COUNT,
    color = Color.BLUE,
)

metric_cmdb_syncer_eda_failed_24h = Metric(
    name = "cmdb_syncer_eda_failed_24h",
    title = Title("Events rejected in the last 24 hours"),
    unit = UNIT_COUNT,
    color = Color.PURPLE,
)

metric_cmdb_syncer_eda_max_sends = Metric(
    name = "cmdb_syncer_eda_max_sends",
    title = Title("Most sends of a single event"),
    unit = UNIT_COUNT,
    color = Color.BROWN,
)

graph_cmdb_syncer_eda_streaks = Graph(
    name = "cmdb_syncer_eda_streaks",
    title = Title("EDA event streaks"),
    simple_lines = [
        "cmdb_syncer_eda_pending",
        "cmdb_syncer_eda_repeating",
        "cmdb_syncer_eda_failing",
    ],
)

graph_cmdb_syncer_eda_sent = Graph(
    name = "cmdb_syncer_eda_sent",
    title = Title("EDA events in the last 24 hours"),
    simple_lines = [
        "cmdb_syncer_eda_events_24h",
        "cmdb_syncer_eda_failed_24h",
    ],
)
