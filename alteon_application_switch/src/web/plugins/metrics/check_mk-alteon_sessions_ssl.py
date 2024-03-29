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

metric_info["alteon_session_peak"] = {
"title" : _("Session Peak"),
"unit" : "count",
"color" : "13/a",
}

#unit_info["Sessions"] = {
#    "title": "Sessions",
#    "description": _("Integer number"),
#    "symbol": "",
#    "render": lambda v: cmk.utils.render.scientific(v, 2),
#}

#graph_info.append({
#"title" : _("Alteon Sessions T"),
#"metrics" : [
#( "alteon_sessions", "Peak"),
#],
#})

check_metrics["check_mk-alteon_sessions_ssl"] = {
    "Current": {
        "name": "alteon_sessions"
    },
    "Peak": {
        "name": "alteon_session_peak"
    },
}
