#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
# pylint: disable=undefined-variable
"""
Subcheck mysql.status for Check_MK Mysql Checks
"""
# +-----------------------------------------------------------------+
# |                                                                 |
# |        (  ___ \     | \    /\|\     /||\     /|( (    /|        |
# |        | (   ) )    |  \  / /| )   ( || )   ( ||  \  ( |        |
# |        | (__/ /     |  (_/ / | |   | || (___) ||   \ | |        |
# |        |  __ (      |   _ (  | |   | ||  ___  || (\ \) |        |
# |        | (  \ \     |  ( \ \ | |   | || (   ) || | \   |        |
# |        | )___) )_   |  /  \ \| (___) || )   ( || )  \  |        |
# |        |/ \___/(_)  |_/    \/(_______)|/     \||/    )_)        |
# |                                                                 |
# | Copyright Bastian Kuhn 2018                mail@bastian-kuhn.de |
# +-----------------------------------------------------------------+
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import time
from .agent_based_api.v1 import get_rate, get_value_store, Metric, register, Result, Service, State

# mysql_status_vars = {
#     "variable name" : ("Gauge|Counter|Voolean"), IS_NEGATIV),
# }

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
    "Innodb_buffer_pool_read_requests"  : ("Counter", False),
    "Innodb_buffer_pool_reads"          : ("Counter", False),
    "Innodb_buffer_pool_write_requests" : ("Counter", False),
    "Innodb_log_waits"                  : ("Counter", False),
    "Innodb_os_log_written"             : ("Counter", False),
    "Innodb_row_lock_time"              : ("Counter", False),
    "Innodb_row_lock_waits"             : ("Counter", False),
    "Key_read_requests"                 : ("Counter", False),
    "Key_reads"                         : ("Counter", False),
    "Key_write_requests"                : ("Counter", False),
    "Key_writes"                        : ("Counter", False),
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
    "Innodb_buffer_pool_pages_free"     : ("Gauge", True),
    "Qcache_free_memory"                : ("Gauge", True),
    "Qcache_free_blocks"                : ("Gauge", True),
    "Key_blocks_unused"                 : ("Gauge", True),
    "Threads_cached"                    : ("Gauge", True),
    "Open_tables"                       : ("Gauge", False),
    "Open_files"                        : ("Gauge", False),
}


def check_mysql_status(item, params, section):
    """
    Check Function
    """
    instance, key = item.split()
    if instance not in section:
        yield Result(state=State.UNKNOWN, summary="Instance Data not found in output")
        return

    data = section[instance]

    def check_level(val, warn, crit, is_n, params):
        """
        Internal Helper to do the Check
        """
        state = State.OK
        if 'levels' in params:
            warn, crit = params['levels']
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
                my_store = get_value_store()

                per_sec = get_rate(my_store, "mysql_status." + key, time.time(), value)

                perfdata.append((key, per_sec, warn, crit))
                message = "rate is %d/s" % (per_sec)

                state = check_level(per_sec, warn, crit, is_negativ, params)

            elif value_type == "Boolean":
                state = State.OK
                message = "%s is %s" % (key, value)
                if 'target_state' in params:
                    target_state = params['target_state']
                    if value != target_state:
                        state = State.CRIT
                    message += " but should be %s" % target_state

            elif value_type == "Gauge":
                perfdata.append((key, value, warn, crit))
                message = "Current %d" % value

                state = check_level(value, warn, crit, is_negativ, params)

            if state != State.OK and value_type != "Boolean":
                warn, crit = params['levels']
                message += ", Levels at (%s/ %s)" % (warn, crit)

            yield Result(state=state, summary=message)
            for p in perfdata:
                yield Metric(p[0], p[1], levels=(p[2], p[3]))


def discover_mysql_status(section):
    for key, items in section.items():
        for item in items:
            if item in mysql_status_inventory.keys():
                yield Service(item="{} {}".format(key, item))


register.check_plugin(
    name = "mysql_status",
    sections = ["mysql"],
    service_name = "MySQL Status %s",
    discovery_function = discover_mysql_status,
    check_function = check_mysql_status,
    check_default_parameters = {},
    check_ruleset_name = "mysql_status",
)
