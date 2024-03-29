#!/usr/bin/env python3

from cmk.gui.i18n import _

from cmk.gui.plugins.metrics import (
    metric_info,
    check_metrics,
)


metric_info["MpMemStatsTotal"] = {
  "title": _("Memory Total"),
  "unit": "bytes",
  "color": "16/a"
}


metric_info["MpMemStatsFree"] = {
  "title": _("Memory Free"),
  "unit": "bytes",
  "color": "16/a"
}


metric_info["MpMemStatsVirtual"] = {
  "title": _("Memory Virtual"),
  "unit": "bytes",
  "color": "16/a"
}


metric_info["MpMemStatsRss"] = {
  "title": _("Memory Rss"),
  "unit": "bytes",
  "color": "16/a"
}

metric_info["PeakMemUsageSP1"] = {
  "title": _("Memory Peak"),
  "unit": "%",
  "color": "16/a"
}


metric_info["CurrentMemUsageSP1"] = {
  "title": _("Memory Current"),
  "unit": "%",
  "color": "16/a"
}


metric_info["percentVirtual"] = {
  "title": _("Memory Virtual Percent"),
  "unit": "%",
  "color": "16/a"
}

metric_info["percentRss"] = {
  "title": _("Memory Rss Percent"),
  "unit": "%",
  "color": "16/a"
}

metric_info["percentPeakMemUsageSP"] = {
  "title": _("Peak memory used from 1st watermark"),
  "unit": "%",
  "color": "16/a"
}

metric_info["percentCurrentMemUsageSP"] = {
  "title": _("Current memory used from 1st watermark"),
  "unit": "%",
  "color": "16/a"
}

metric_info["SpMemUseStatsCurFrontEndSessions"] = {
  "title": _("Current front-end sessions"),
  "unit": "count",
  "color": "16/a"
}

metric_info["SpMemUseStatsAvgFrontEndSessions"] = {
  "title": _("Average front-end session size"),
  "unit": "bytes",
  "color": "16/a"
}

metric_info["SpMemUseStatsMaxAllowConnections"] = {
  "title": _("Max allowed front-end sessions"),
  "unit": "count",
  "color": "16/a"
}

check_metrics["check_mk-alteon_memory"] = {
  "percentRss": {
    "name": "percentRss"
  },
  "percentVirtual": {
    "name": "percentVirtual"
  },
  "MpMemStatsTotal": {
    "name": "MpMemStatsTotal"
  },
  "MpMemStatsFree": {
    "name": "MpMemStatsFree"
  },
  "MpMemStatsVirtual": {
    "name": "MpMemStatsVirtual"
  },
  "MpMemStatsRss": {
    "name": "MpMemStatsRss"
  },
  "PeakMemUsageSP": {
    "name": "percentPeakMemUsageSP"
  },
  "CurrentMemUsageSP": {
    "name": "percentCurrentMemUsageSP"
  },
  "SpMemUseStatsCurFrontEndSessions": {
    "name": "SpMemUseStatsCurFrontEndSessions"
  },
  "SpMemUseStatsAvgFrontEndSessions": {
    "name": "SpMemUseStatsAvgFrontEndSessions"
  },
  "SpMemUseStatsMaxAllowConnections": {
    "name": "SpMemUseStatsMaxAllowConnections"
  },
}
