#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

# 
# MSSQL_SQL2012T:Access_Methods workfiles_created/sec None 209728^M
# MSSQL_SQL2012T:Access_Methods worktables_created/sec None 50631^M
#

from time import time

from .agent_based_api.v2 import (
    get_rate,
    get_value_store,
    register,
    Service,
    Result,
    State,
    Metric
)


def discover_mssql_work_files_tables(section):
    # instance is always "None" here
    for (obj_id, instance), counters in iter(section.items()):
        if obj_id.endswith(":Access_Methods") and \
                "workfiles_created/sec" in counters and \
                "worktables_created/sec" in counters:
                yield Service(item=obj_id.split(":")[0])


def check_mssql_work_files_tables(item, params, section):
    if not section:
        return

    db = item
    obj_id = db + ":Access_Methods"
    instance = "None"

    now = time()

    value_store = get_value_store()

    wf = section[(obj_id, instance)]["workfiles_created/sec"]
    wf_counter = "mssql_work_files_tables.%s" % db
    value = get_rate(
        value_store,
        wf_counter,
        now,
        wf,
    )
    infotext = "%.2f workfiles_created/sec" % value
    levels = params.get("WorkFiles")

    if levels is not None:
        warn, crit = levels
        levelstext = " (warn/crit at %.2f/%.2f)" % levels
        yield Metric("perf_WorkFiles", value, levels=levels)
        if value >= crit: 
            yield Result(state=State.CRIT, summary=infotext+levelstext)
        elif value >= warn:
            yield Result(state=State.WARN, summary=infotext+levelstext)
        else:
            yield Result(state=State.OK, summary=infotext)
    else:
        yield Metric("perf_WorkFiles", value)
        yield Result(state=State.OK, summary=infotext)

    wt = section[(obj_id, instance)]["worktables_created/sec"]
    wt_counter = "mssql_work_files_tabels.%s" % db
    value = get_rate(
        value_store,
        wt_counter,
        now,
        wt,
    )
    infotext = "%.2f worktables_created/sec " % value
    levels = params.get("WorkTables")

    if levels is not None:
        warn, crit = levels
        levelstext = " (warn/crit at %.2f/%.2f)" % levels
        yield Metric("perf_WorkTables", value, levels=levels)
        if value >= crit: 
            yield Result(state=State.CRIT, summary=infotext+levelstext)
        elif value >= warn:
            yield Result(state=State.WARN, summary=infotext+levelstext)
        else:
            yield Result(state=State.OK, summary=infotext)
    else:
        yield Metric("perf_WorkTables", value)
        yield Result(state=State.OK, summary=infotext)


check_plugin_mssql_countes_work_files_tables = CheckPlugin(
    name = "mssql_counters_work_files_tables",
    service_name = "MSSQL %s WorkFiles and WorkTables",
    sections = ["mssql_counters"],
    check_function = check_mssql_work_files_tables,
    discovery_function = discover_mssql_work_files_tables,
    check_ruleset_name = "mssql_counters_work_files_tables",
    check_default_parameters = {
        "WorkFiles" : (100.0, 200.0),
        "WorkTables" : (200.0, 400.0),
    },
)
