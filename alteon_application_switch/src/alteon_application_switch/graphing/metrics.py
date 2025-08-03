#!/usr/bin/env python3
from cmk.graphing.v1 import metrics, Title

# CPU Metrics (verwendet dynamische Namen: "1sec", "4sec", "64sec")
metric_1sec = metrics.Metric(
    name="1sec",
    title=Title("CPU Utilization last second"),
    unit=metrics.Unit(metrics.DecimalNotation("%")),
    color=metrics.Color.BLUE,
)

metric_4sec = metrics.Metric(
    name="4sec", 
    title=Title("CPU Utilization last 4 seconds"),
    unit=metrics.Unit(metrics.DecimalNotation("%")),
    color=metrics.Color.GREEN,
)

metric_64sec = metrics.Metric(
    name="64sec",
    title=Title("CPU Utilization last 64 seconds"), 
    unit=metrics.Unit(metrics.DecimalNotation("%")),
    color=metrics.Color.PURPLE,
)

# Interface Metrics
metric_ifPortStatsInOctetsPerSec = metrics.Metric(
    name="ifPortStatsInOctetsPerSec",
    title=Title("Input Octets"),
    unit=metrics.Unit(metrics.DecimalNotation("bytes/s")),
    color=metrics.Color.GREEN,
)

metric_ifPortStatsOutOctetsPerSec = metrics.Metric(
    name="ifPortStatsOutOctetsPerSec",
    title=Title("Output Octets"),
    unit=metrics.Unit(metrics.DecimalNotation("bytes/s")),
    color=metrics.Color.BLUE,
)

metric_ifPortStatsInPktsPerSec = metrics.Metric(
    name="ifPortStatsInPktsPerSec",
    title=Title("Input Packets"),
    unit=metrics.Unit(metrics.DecimalNotation("1/s")),
    color=metrics.Color.CYAN,
)

metric_ifPortStatsOutPktsPerSec = metrics.Metric(
    name="ifPortStatsOutPktsPerSec",
    title=Title("Output Packets"),
    unit=metrics.Unit(metrics.DecimalNotation("1/s")),
    color=metrics.Color.LIGHT_BLUE,
)

# Memory Metrics
metric_MpMemStatsTotal = metrics.Metric(
    name="MpMemStatsTotal",
    title=Title("Memory Total"),
    unit=metrics.Unit(metrics.IECNotation("B")),
    color=metrics.Color.BLUE,
)

metric_MpMemStatsFree = metrics.Metric(
    name="MpMemStatsFree",
    title=Title("Memory Free"),
    unit=metrics.Unit(metrics.IECNotation("B")),
    color=metrics.Color.GREEN,
)

metric_MpMemStatsVirtual = metrics.Metric(
    name="MpMemStatsVirtual",
    title=Title("Memory Virtual"),
    unit=metrics.Unit(metrics.IECNotation("B")),
    color=metrics.Color.PURPLE,
)

metric_MpMemStatsRss = metrics.Metric(
    name="MpMemStatsRss",
    title=Title("Memory Rss"),
    unit=metrics.Unit(metrics.IECNotation("B")),
    color=metrics.Color.ORANGE,
)

metric_PeakMemUsageSP1 = metrics.Metric(
    name="PeakMemUsageSP1",
    title=Title("Memory Peak"),
    unit=metrics.Unit(metrics.DecimalNotation("%")),
    color=metrics.Color.RED,
)

metric_CurrentMemUsageSP1 = metrics.Metric(
    name="CurrentMemUsageSP1",
    title=Title("Memory Current"),
    unit=metrics.Unit(metrics.DecimalNotation("%")),
    color=metrics.Color.CYAN,
)

metric_percentVirtual = metrics.Metric(
    name="percentVirtual",
    title=Title("Memory Virtual Percent"),
    unit=metrics.Unit(metrics.DecimalNotation("%")),
    color=metrics.Color.LIGHT_PURPLE,
)

metric_percentRss = metrics.Metric(
    name="percentRss",
    title=Title("Memory Rss Percent"),
    unit=metrics.Unit(metrics.DecimalNotation("%")),
    color=metrics.Color.LIGHT_ORANGE,
)

metric_percentPeakMemUsageSP = metrics.Metric(
    name="percentPeakMemUsageSP",
    title=Title("Peak memory used from 1st watermark"),
    unit=metrics.Unit(metrics.DecimalNotation("%")),
    color=metrics.Color.DARK_RED,
)

metric_percentCurrentMemUsageSP = metrics.Metric(
    name="percentCurrentMemUsageSP",
    title=Title("Current memory used from 1st watermark"),
    unit=metrics.Unit(metrics.DecimalNotation("%")),
    color=metrics.Color.LIGHT_CYAN,
)

metric_SpMemUseStatsCurFrontEndSessions = metrics.Metric(
    name="SpMemUseStatsCurFrontEndSessions",
    title=Title("Current front-end sessions"),
    unit=metrics.Unit(metrics.DecimalNotation("")),
    color=metrics.Color.YELLOW,
)

metric_SpMemUseStatsAvgFrontEndSessions = metrics.Metric(
    name="SpMemUseStatsAvgFrontEndSessions",
    title=Title("Average front-end session size"),
    unit=metrics.Unit(metrics.IECNotation("B")),
    color=metrics.Color.PINK,
)

metric_SpMemUseStatsMaxAllowConnections = metrics.Metric(
    name="SpMemUseStatsMaxAllowConnections",
    title=Title("Max allowed front-end sessions"),
    unit=metrics.Unit(metrics.DecimalNotation("")),
    color=metrics.Color.BROWN,
)

# RServer Metrics (echte Feldnamen aus parse_alteon_rserver)
metric_new_sessions_per_second = metrics.Metric(
    name="new_sessions_per_second",
    title=Title("RServer New Sessions per Second"),
    unit=metrics.Unit(metrics.DecimalNotation("1/s")),
    color=metrics.Color.PURPLE,
)

metric_failures = metrics.Metric(
    name="failures",
    title=Title("RServer Failures"),
    unit=metrics.Unit(metrics.DecimalNotation("")),
    color=metrics.Color.RED,
)

metric_peak_sessions = metrics.Metric(
    name="peak_sessions",
    title=Title("Peak Sessions"),
    unit=metrics.Unit(metrics.DecimalNotation("")),
    color=metrics.Color.ORANGE,
)

metric_octets_total_rxtx_per_second = metrics.Metric(
    name="octets_total_rxtx_per_second",
    title=Title("RServer Traffic (in + out)"),
    unit=metrics.Unit(metrics.DecimalNotation("bytes/s")),
    color=metrics.Color.GREEN,
)

# Sessions SLB Metrics (verwendet dynamische Namen: "current_sessions", "4sec", "64sec")
metric_current_sessions = metrics.Metric(
    name="current_sessions",
    title=Title("Current Sessions"),
    unit=metrics.Unit(metrics.DecimalNotation("")),
    color=metrics.Color.BLUE,
)

# Sessions SSL Metrics (verwendet statische Namen: "Peak", "Current")
# Peak und Current sind bereits oben definiert

# Throughput Metrics (verwendet statische Namen: "Peak", "Current")
metric_Peak = metrics.Metric(
    name="Peak",
    title=Title("Throughput Peak"),
    unit=metrics.Unit(metrics.DecimalNotation("bits/s")),
    color=metrics.Color.GREEN,
)

metric_Current = metrics.Metric(
    name="Current",
    title=Title("Current Throughput"),
    unit=metrics.Unit(metrics.DecimalNotation("bits/s")),
    color=metrics.Color.BLUE,
)

# VServer Metrics (echte Feldnamen aus parse_alteon_vserver)
# current_sessions ist bereits oben definiert
# new_sessions_per_second ist bereits oben für RServer definiert
# peak_sessions ist bereits oben definiert

metric_http_header_sessions = metrics.Metric(
    name="http_header_sessions",
    title=Title("VServer HTTP Header Sessions"),
    unit=metrics.Unit(metrics.DecimalNotation("")),
    color=metrics.Color.LIGHT_PURPLE,
)

metric_hc_octets_per_sec = metrics.Metric(
    name="hc_octets_per_sec",
    title=Title("VServer Traffic (in + out)"),
    unit=metrics.Unit(metrics.DecimalNotation("bytes/s")),
    color=metrics.Color.LIGHT_GREEN,
)
