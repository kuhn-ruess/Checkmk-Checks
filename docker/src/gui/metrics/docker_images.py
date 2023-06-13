#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
# 
# Metric definitions for the docker_images check
#
# Author: lars.getwan@metrosystems.net
#

from cmk.gui.i18n import _
from cmk.gui.plugins.metrics.utils import graph_info, metric_info, check_metrics

metric_info["docker_image_mem_used"] = {
    "title" : _("Memory Used"),
    "color": "15/a",
    "unit" : "bytes",
}

metric_info["docker_image_disk_used"] = {
    "title" : _("Disk Space Used"),
    "color": "35/a",
    "unit" : "bytes",
}

metric_info["docker_image_cpu_pct"] = {
    "title" : _("CPU Usage"),
    "color": "35/a",
    "unit" : "%",
}

metric_info["docker_image_running_containers"] = {
    "title" : _("Containers Running"),
    "color": "35/a",
    "unit" : "count",
}

docker_image_translation = {
            "CPU_pct"            : { "name": "docker_image_cpu_pct" },
            "Memory_used"        : { "name": "docker_image_mem_used" },
            "Diskspace_used"     : { "name": "docker_image_disk_used" },
            "Running_containers" : { "name": "docker_image_running_containers" },
            }

check_metrics["check_mk-docker_images"] = docker_image_translation


graph_info.append({
    "title" : _("Docker Image CPU"),
    "metrics" : [
        ( "docker_image_cpu_pct",      "area"),
    ],
    "omit_zero_metrics" : False,
})

graph_info.append({
    "title" : _("Docker Image Memory"),
    "metrics" : [
        ( "docker_image_mem_used",      "area"),
    ],
    "omit_zero_metrics" : False,
})

graph_info.append({
    "title" : _("Docker Image Disk Space"),
    "metrics" : [
        ( "docker_image_disk_used",      "area"),
    ],
    "omit_zero_metrics" : False,
})

graph_info.append({
    "title" : _("Docker Image Containers"),
    "metrics" : [
        ( "docker_image_running_containers",      "area"),
    ],
    "omit_zero_metrics" : False,
})
