#!/usr/bin/env python3

from cmk.gui.i18n import _

from cmk.gui.plugins.metrics import (
    metric_info,
    check_metrics,
)

metric_info["alteon_sessions"] = {
"title": _("Current Sessions"),
"unit": "count",
"color": "16/a"
}

metric_info["alteon_sessions_4sec"] = {
"title" : _("Sessions over 4 Seconds averaged"),
"unit" : "count",
"color" : "13/a",
}

metric_info["alteon_sessions_64sec"] = {
"title" : _("Sessions over 64 Seconds averaged"),
"unit" : "count",
"color" : "11/a",
}


#graph_info.append({
#"title" : _("Alteon Sessions T"),
#"metrics" : [
#( "alteon_sessions", "Peak"),
#],
#})

check_metrics["check_mk-alteon_sessions_slb"] = {
    "current_sessions": {
        "name": "alteon_sessions"
    },
    "4sec": {
        "name": "alteon_sessions_4sec"
    },
    "64sec": {
        "name": "alteon_sessions_64sec"
    },
}

check_metrics["check_mk-alteon_sessions"] = check_metrics["check_mk-alteon_sessions_slb"]
