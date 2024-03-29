#!/usr/bin/env python3

from cmk.gui.i18n import _

from cmk.gui.plugins.metrics import (
    metric_info,
    check_metrics,
)

metric_info["alteon_throughput"] = {
"title": _("Current Throughput"),
"unit": "bits/s",
"color": "16/a"
}

metric_info["alteon_throughput_peak"] = {
"title" : _("Throughput Peak"),
"unit" : "bits/s",
"color" : "13/a",
}

check_metrics["check_mk-alteon_throughput"] = {
    "Current": {
        "name": "alteon_throughput"
    },
    "Peak": {
        "name": "alteon_throughput_peak"
    },
}
