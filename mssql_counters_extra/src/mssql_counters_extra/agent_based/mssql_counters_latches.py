#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

# 
# MSSQL_SQL2012T:Latches latch_waits/sec None 52531
# MSSQL_SQL2012T:Latches average_latch_wait_time_(ms) None 39066
# MSSQL_SQL2012T:Latches average_latch_wait_time_base None 52531
# MSSQL_SQL2012T:Latches total_latch_wait_time_(ms) None 39066
#

from contextlib import suppress
from time import time
from .agent_based_api.v2 import (
    get_rate,
    get_value_store,
    register,
    Service,
    Result,
    State,
    Metric,
    GetRateError,
    check_levels
)


def discover_mssql_latches(section):
    # instance is always "None" here
    for (obj_id, instance), counters in iter(section.items()):
        if obj_id.endswith(":Latches") and "latch_waits/sec" in counters and \
                "average_latch_wait_time_(ms)" in counters and \
                "latch_waits/sec" in counters:
            yield Service(item=obj_id.split(":")[0])


def check_mssql_latches(item, params, section):
    if not section:
        return

    db = item
    obj_id = db + ":Latches"
    instance = "None"

    now = time()

    value_store = get_value_store()

    latch_waits = None
    with suppress(GetRateError):
        lw = section[(obj_id, instance)]["latch_waits/sec"]
        lw_counter = "mssql_latch_waits.%s" % db
        latch_waits = get_rate(
            value_store,
            lw_counter,
            now,
            lw,
        )
        yield from check_levels(
            value=latch_waits,
            levels_upper=params.get("LatchWaits"),
            metric_name="latch_waits_per_sec",
            label="Latch waits/sec"
        )

    latch_wait_time = None
    with suppress(GetRateError):
        lwt = section[(obj_id, instance)]["total_latch_wait_time_(ms)"]
        lwt_counter = "mssql_latch_wait_time.%s" % db
        latch_wait_time = get_rate(
            value_store,
            lwt_counter,
            now,
            lwt,
        )
        yield from check_levels(
            value=latch_wait_time,
            levels_upper=params.get("LatchWaitTime"),
            metric_name="latch_wait_time",
            label="Latch wait time"
        )

    avg_latch_wait_time = None
    with suppress(GetRateError):
        alwt = section[(obj_id, instance)]["average_latch_wait_time_(ms)"]
        alwt_counter = "mssql_avg_latch_wait_time.%s" % db
        avg_latch_wait_time = get_rate(
            value_store,
            alwt_counter,
            now,
            alwt,
        )
        yield from check_levels(
            value=latch_wait_time,
            levels_upper=params.get("LatchAverage"),
            metric_name="avg_latch_wait_time",
            label="Average latch wait time"
        )

    if latch_waits is None and latch_wait_time is None and avg_latch_wait_time is None:
        raise GetRateError


check_plugin_mssql_counters_latches = CheckPlugin(
    name = "mssql_counters_latches",
    service_name = "MSSQL %s Latch Waits",
    sections = ["mssql_counters"],
    discovery_function = discover_mssql_latches,
    check_function = check_mssql_latches,
    check_ruleset_name = "mssql_counters_latches",
    check_default_parameters = {
        "LatchWaits" : (100.0, 200.0),
        "LatchWaitTime" : (200.0, 400.0),
        "LatchAverage" : (20.0, 40.0),
    },
)
