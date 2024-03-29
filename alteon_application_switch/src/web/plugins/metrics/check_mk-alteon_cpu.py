#!/usr/bin/env python3
#Exception: [('1sec', 4, '', 80, 90, None, None), ('64sec', 8, '', 80, 90, None, None), ('4sec', 5, '', 80, 90, None, None)]

from cmk.gui.i18n import _

from cmk.gui.plugins.metrics import (
    metric_info,
    check_metrics,
)

metric_info["alteon_cpu_1sec"] = {
"title": _("CPU Utilization last second"),
"unit": "%",
"color": "16/a"
}

metric_info["alteon_cpu_4sec"] = {
"title" : _("CPU Utilization last 4 seconds"),
"unit" : "%",
"color" : "13/a",
}

metric_info["alteon_cpu_64sec"] = {
"title" : _("CPU Utilization last 64 seconds"),
"unit" : "%",
"color" : "11/a",
}


#graph_info.append({
#"title" : _("Alteon Sessions T"),
#"metrics" : [
#( "alteon_sessions", "Peak"),
#],
#})

check_metrics["check_mk-alteon_cpu"] = {
    "1sec": {
        "name": "alteon_cpu_1sec"
    },
    "4sec": {
        "name": "alteon_cpu_4sec"
    },
    "64sec": {
        "name": "alteon_cpu_64sec"
    },
}

