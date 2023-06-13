#!/usr/bin/env python3

from cmk.gui.i18n import _
from cmk.gui.plugins.metrics.utils import graph_info, metric_info, check_metrics

metric_info["docker_container_cpu_usage"] = {
    "title" : _("CPU Usage"),
    "color": "25/a",
    "unit" : "%",
}

metric_info["docker_container_mem_limit"] = {
    "title" : _("Memory Limit"),
    "color": "25/a",
    "unit" : "bytes",
}

metric_info["docker_container_mem_used"] = {
    "title" : _("Memory Used"),
    "color": "15/a",
    "unit" : "bytes",
}

metric_info["docker_container_size_root_fs"] = {
    "title" : _("Size Root FS"),
    "color": "35/a",
    "unit" : "bytes",
}

metric_info["docker_container_sizerw"] = {
    "title" : _("Size Changed"),
    "color": "45/a",
    "unit" : "bytes",
}

docker_container_translation = {
            "CPU_pct"         : { "name": "docker_container_cpu_usage" },
            "Memory_limit"    : { "name": "docker_container_mem_limit" },
            "Memory_used"     : { "name": "docker_container_mem_used" },
            "SizeRootFs"      : { "name": "docker_container_size_root_fs" },
            "SizeRw"          : { "name": "docker_container_sizerw" },
            }

check_metrics["check_mk-docker_containers"] = docker_container_translation


graph_info.append({
    "title" : _("Docker Container CPU"),
    "metrics" : [
        ( "docker_container_cpu_usage",      "area"),
    ],
    "omit_zero_metrics" : False,
})

graph_info.append({
    "title" : _("Docker Container Memory"),
    "metrics" : [
        ( "docker_container_mem_limit",      "line"),
        ( "docker_container_mem_used",      "area"),
    ],
    "omit_zero_metrics" : False,
})

graph_info.append({
    "title" : _("Docker Container Disk Space"),
    "metrics" : [
        ( "docker_container_size_root_fs",      "line"),
        ( "docker_container_sizerw",      "area"),
    ],
    "omit_zero_metrics" : False,
})

