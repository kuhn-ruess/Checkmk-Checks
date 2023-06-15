from cmk.gui.plugins.metrics import metric_info, graph_info

metric_info['directories_total'] = {
    'title': "Total Directories",
    'unit': "count",
    'color': "blue",
}
metric_info['files_total'] = {
    'title': "Total Files",
    'unit': "count",
    'color': "blue",
}
metric_info['disk_used'] = {
    'title': "Diskspace Used",
    'unit': "bytes",
    'color': "blue",
}

metric_info['physical_used'] = {
    'title': "Physical Used",
    'unit': "bytes",
    'color': "blue",
}

metric_info['quota_used_bytes'] = {
    'title': "Quota Usage",
    'unit': "bytes",
    'color': "16/a",
}

metric_info['quota_limit_bytes'] = {
    'title': "Limit",
    'unit': "bytes",
    'color': "24/a",
}

graph_info['quobyte_quotas'] = {
    'metrics': [
        ('quota_used_bytes', "line"),
        ('quota_limit_bytes', "line"),
    ]
}
