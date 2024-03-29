#!/usr/bin/env python3

from cmk.gui.i18n import _

from cmk.gui.plugins.metrics import (
    metric_info,
    check_metrics,
)

# VServer	
metric_info["current_sessions"] = {
"title": _("Current Sessions"),
"unit": "count",
"color": "16/a"
}

metric_info["hc_octets_per_sec"] = {
"title": _("Traffic (in + out)"),
"unit": "bytes/s",
"color": "#00e060"
}

metric_info["http_header_sessions"] = {
"title": _("HTTP Header Sessions"),
"unit": "count",
"color": "16/a"
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

check_metrics["check_mk-alteon_vserver"] = {
    "current_sessions": {
        "name": "current_sessions"
    },
    "new_sessions_per_second": {
        "name": "new_sessions_per_sec"
    },
    "peak_sessions": {
        "name": "peak_sessions"
    },
    "http_header_sessions": {
        "name": "http_header_sessions"
    },
    "hc_octets_per_sec": {
        "name": "hc_octets_per_sec"
    }
}


