#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.graphing.v1.graphs import Graph, Title


graph_quobyte_quotas = Graph(
    name = "quobyte_quotas",
    title = Title("Quobyte quotas"),
    simple_lines = ["quota_used_bytes", "quota_limit_bytes"],
)
