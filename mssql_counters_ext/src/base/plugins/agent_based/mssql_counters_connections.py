#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# 
# MSSQL_SQL2012T:General_Statistics logins/sec None 5208^M
# MSSQL_SQL2012T:General_Statistics logouts/sec None 5205^M
# MSSQL_SQL2012T:General_Statistics user_connections None 3^M

from contextlib import suppress
from .agent_based_api.v1 import get_rate, get_value_store, register, Service, Result, State, Metric, GetRateError, check_levels
import time
 

def discover_mssql_counters_connections(section):
    # instance is always "None" here
    for (obj_id, instance), counters in iter(section.items()):
        if obj_id.endswith("General_Statistics") and "logins/sec" in counters and \
                "logouts/sec" in counters and "user_connections" in counters:
            yield Service(item=obj_id.split(":")[0])


def check_mssql_counters_connections(item, params, section):
    db = item
    obj_id = db + ":General_Statistics"
    instance = "None"

    now = time.time()

    value_store = get_value_store()

    uconn = section[(obj_id, instance)]["user_connections"]
    yield from check_levels(
                value=uconn,
                levels_upper=params.get("user_connections"),
                label="User Connections",
        )

    with suppress(GetRateError):
        logins = section[(obj_id, instance)]["logins/sec"]
        login_counter = "mssql_connections_logins.%s" % db
        logins_per_sec = get_rate(
                value_store,
                login_counter,
                now,
                logins,
            )
        yield from check_levels(
                    value=logins_per_sec,
                    levels_upper=params.get("LogInConnects"),
                    metric_name="logins_per_sec",
                    label="Logins/sec",
                )

    with suppress(GetRateError):
        #what2 = "LogOutConnects"
        logouts = section[(obj_id, instance)]["logouts/sec"]
        logout_counter = "mssql_connections_logouts.%s" % db
        logouts_per_sec = get_rate(
                            value_store,
                            logout_counter,
                            now,
                            logouts,
                        )
        yield from check_levels(
                    value=logouts_per_sec,
                    levels_upper=params.get("LogOutConnects"),
                    metric_name="logouts_per_sec",
                    label="Logouts/sec",
                )


register.check_plugin(
    name='mssql_counters_connections',
    service_name='%s User Connections',
    sections=['mssql_counters'],
    discovery_function=discover_mssql_counters_connections,
    check_function=check_mssql_counters_connections,
    check_ruleset_name="mssql_counters_connections",
    check_default_parameters={
        "user_connections" : (100, 200),
        "LogInConnects" : (2.0, 10.0),
        "LogOutConnects" : (2.0, 10.0),
    },
)
