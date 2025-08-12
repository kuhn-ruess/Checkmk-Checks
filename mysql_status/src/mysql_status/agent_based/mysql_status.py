#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from time import time

from cmk.agent_based.v2 import (
    CheckPlugin,
    Metric,
    Result,
    Service,
    State,
    get_rate,
    get_value_store,
    GetRateError,
)


mysql_status_inventory = { #pylint: disable=invalid-name
    "Aborted_clients"                   : ("Counter", False),
    "Aborted_connects"                  : ("Counter", False),
    "Bytes_received"                    : ("Counter", False),
    "Bytes_sent"                        : ("Counter", False),
    "Compression"                       : ("Boolean", False),
    "Connections"                       : ("Counter", False),
    "Created_tmp_disk_tables"           : ("Counter", False),
    "Created_tmp_files"                 : ("Counter", False),
    "Created_tmp_tables"                : ("Counter", False),
    "Innodb_buffer_pool_pages_free"     : ("Gauge",   True),
    "Innodb_buffer_pool_read_requests"  : ("Counter", False),
    "Innodb_buffer_pool_reads"          : ("Counter", False),
    "Innodb_buffer_pool_write_requests" : ("Counter", False),
    "Innodb_log_waits"                  : ("Counter", False),
    "Innodb_os_log_written"             : ("Counter", False),
    "Innodb_row_lock_time"              : ("Counter", False),
    "Innodb_row_lock_waits"             : ("Counter", False),
    "Key_blocks_unused"                 : ("Gauge",   True),
    "Key_read_requests"                 : ("Counter", False),
    "Key_reads"                         : ("Counter", False),
    "Key_write_requests"                : ("Counter", False),
    "Key_writes"                        : ("Counter", False),
    "Open_tables"                       : ("Gauge",   False),
    "Open_files"                        : ("Gauge",   False),
    "Qcache_free_memory"                : ("Gauge",   True),
    "Qcache_free_blocks"                : ("Gauge",   True),
    "Qcache_hits"                       : ("Counter", True),
    "Qcache_inserts"                    : ("Counter", False),
    "Qcache_low_mem_prunes"             : ("Counter", False),
    "Qcache_lowmem_prunes"              : ("Counter", False),
    "Qcache_not_cached"                 : ("Counter", False),
    "Queries"                           : ("Counter", False),
    "Questions"                         : ("Counter", False),
    "Select_full_join"                  : ("Counter", False),
    "Select_range_check"                : ("Counter", False),
    "Slave_retried_transactions"        : ("Counter", False),
    "Slave_running"                     : ("Boolean", False),
    "Slow_launch_threads"               : ("Counter", False),
    "Slow_queries"                      : ("Counter", False),
    "Sort_merge_passes"                 : ("Counter", False),
    "Table_locks_waited"                : ("Counter", False),
    "Threads_cached"                    : ("Gauge",   True),
}


def discover_mysql_status(section):
    for key, items in section.items():
        for item in items:
            if item in mysql_status_inventory.keys():
                yield Service(item=f"{key} {item}")

def check_mysql_status(item, params, section):
    instance, key = item.split()

    if instance not in section:
        yield Result(state=State.UNKNOWN, summary="Instance data not found in output")

    else:
        data = section[instance]

        def check_level(val, warn, crit, is_n, params):
            """
            Internal Helper to do the Check
            """
            state = State.OK

            if "levels" in params:
                warn, crit = params["levels"][1]
                if is_n:
                    if val <= crit:
                        state = State.CRIT
                    elif val <= warn:
                        state = State.WARN
                else:
                    if val >= crit:
                        state = State.CRIT
                    elif val >= warn:
                        state = State.WARN
            return state

        warn, crit = None, None
        for var, value in data.items():
            if key == var:
                perfdata = []
                value_type, is_negativ = mysql_status_inventory[key]

                if value_type == "Counter":
                    try:
                        per_sec = get_rate(value_store=get_value_store(),key="mysql_status." + key, time=time(), value=value, raise_overflow=True)
                    except GetRateError:
                        per_sec = 0.0
                    yield Metric(name=f"mysql_status_{key.lower()}", value=per_sec, levels=(warn, crit))

                    state = check_level(per_sec, warn, crit, is_negativ, params)
                    yield Result(state=state, summary=f"Rate: {per_sec:.3}/s")

                elif value_type == "Boolean":
                    state = State.OK
                    message = f"{key} is {value}"

                    if "target_state" in params:
                        target_state = params["target_state"]

                        if value != target_state:
                            state = State.CRIT

                        message += f" but should be {target_state}"

                    yield Result(state=state, summary=message)

                elif value_type == "Gauge":
                    yield Metric(name=f"mysql_status_{key.lower()}", value=value, levels=(warn, crit))

                    state = check_level(value, warn, crit, is_negativ, params)
                    yield Result(state=state, summary=f"Current: {value}")


check_plugin_mysql_status = CheckPlugin(
    name = "mysql_status",
    sections = ["mysql"],
    service_name = "MySQL Status %s",
    discovery_function = discover_mysql_status,
    check_function = check_mysql_status,
    check_default_parameters = {},
    check_ruleset_name = "mysql_status",
)
