#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.graphing.v1.metrics import Metric, Title, Color, Unit, DecimalNotation, IECNotation

UNIT_NUMBER = Unit(DecimalNotation(""))
UNIT_BYTES = Unit(IECNotation("B"))


metric_directories_total = Metric(
    name = "total_directories",
    title = Title("Total Directories"),
    unit = UNIT_NUMBER,
    color = Color.BLUE,
)


metric_files_total = Metric(
    name = "total_files",
    title = Title("Total Files"),
    unit = UNIT_NUMBER,
    color = Color.BLUE,
)


metric_disk_used = Metric(
    name = "diskspace_used_bytes",
    title = Title("Diskspace Used"),
    unit = UNIT_BYTES,
    color = Color.BLUE,
)


metric_physical_used = Metric(
    name = "physical_used_bytes",
    title = Title("Physical Used"),
    unit = UNIT_BYTES,
    color = Color.BLUE,
)


metric_quota_used = Metric(
    name = "quota_used_bytes",
    title = Title("Quota Usage"),
    unit = UNIT_BYTES,
    color = Color.ORANGE,
)


metric_quota_limit = Metric(
    name = "quota_limit_bytes",
    title = Title("Limit"),
    unit = UNIT_BYTES,
    color = Color.YELLOW,
)
