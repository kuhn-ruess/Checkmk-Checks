#!/usr/bin/env python3

from cmk.gui.i18n import _

from cmk.gui.plugins.metrics import (
    metric_info,
    check_metrics,
)

# RServer	
metric_info["current_sessions"] = {
"title": _("Current Sessions"),
"unit": "count",
"color": "16/a"
}

metric_info["octets_total_rxtx_per_second"] = {
"title": _("Traffic (in + out)"),
"unit": "bytes/s",
"color": "#00e060"
}

metric_info["failures"] = {
"title": _("Failures"),
"unit": "count",
"color": "#ff3333"
}

metric_info["new_sessions_per_sec"] = {
"title": _("New Sessions"),
"unit": "1/s",
"color": "16/a"
}

metric_info["peak_sessions"] = {
"title": _("Peak Sessions"),
"unit": "count",
"color": "16/a"
}

check_metrics["check_mk-alteon_rserver"] = {
    "current_sessions": {
        "name": "current_sessions"
    },
    "new_sessions_per_second": {
        "name": "new_sessions_per_sec"
    },
    "peak_sessions": {
        "name": "peak_sessions"
    },
    "failures": {
        "name": "failures"
    },
    "octets_total_rxtx_per_second": {
        "name": "octets_total_rxtx_per_second"
    }
}


