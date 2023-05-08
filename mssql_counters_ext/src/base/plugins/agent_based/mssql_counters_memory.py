#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .agent_based_api.v1 import get_rate, get_value_store, register, Service, Result, State, Metric, render
import time

def _check_memory_usage(db, params, section):
    obj_id = db + ":Memory_Manager"
    instance = "None"

    levels=params.get("MemoryUsage")

    totmem = section[(obj_id, instance)]["total_server_memory_(kb)"]
    tarmem = section[(obj_id, instance)]["target_server_memory_(kb)"]
    value = 100 * (totmem / tarmem)
    targig= tarmem / 1048576    
    infotext = "%.2f %% MemoryUsage of %.2f GB TargetMem" % (value,targig)
    if levels is not None:
        warn, crit = levels
        levelstext = " (warn, crit at %d/%d%%)" % (warn, crit)
        yield Metric("perf_MemoryUsage", value, levels=(warn, crit))
        if value >= crit:
            yield Result(state=State.CRIT, summary=infotext + levelstext)
        elif value >= warn:
            yield Result(state=State.WARN, summary=infotext + levelstext)
        else:
            yield Result(state=State.OK, summary=infotext)
    else:
        yield Metric("perf_MemoryUsage", value)
        yield Result(state=State.OK, summary=infotext)


def _check_memory_grants(db, params, section):
    obj_id = db + ":Memory_Manager"
    instance = "None"

    levels = params.get("MemoryGrantsPending")

    mgrants = section[(obj_id, instance)]["memory_grants_pending"]
    infotext = "%d memory_grants_pending" % mgrants 
    if levels is not None:
        warn, crit = levels
        levelstext = " (warn, crit at %s/%s)" % (warn, crit)
        yield Metric("perf_MemoryGrantsPending", mgrants, levels=(warn, crit))
        if mgrants >= crit: 
            yield Result(state=State.CRIT, summary=infotext+levelstext)
        elif mgrants >= warn:
            yield Result(state=State.WARN, summary=infotext+levelstext)
        else:
            yield Result(state=State.OK, summary=infotext)
    else:
        yield Metric("perf_MemoryGrantsPending", mgrants)
        yield Result(state=State.OK, summary=infotext)


def _check_page_life_expectancy(db, params, section):
    obj_id = db + ":Buffer_Manager"
    instance = "None"
    levels = params.get("page_life_expectancy")

    page_life_expectancy = section[(obj_id, instance)]["page_life_expectancy"]
    infotext = "page_life_expectancy is %s"  % render.timespan(page_life_expectancy)
    if levels != None:
        yield Metric("perf_page_life_expectancy", page_life_expectancy, levels=levels)
        warn, crit = levels
        levelstext =  " (warn / crit below %s/%s)" % (render.timespan(warn), render.timespan(crit))
        if page_life_expectancy < crit:
            yield Result(state=State.CRIT, summary=infotext + levelstext)
        elif page_life_expectancy < warn:
            yield Result(state=State.WARN, summary=infotext + levelstext)
        else:
            yield Result(state=State.OK, summary=infotext)
    else:
        yield Metric("perf_page_life_expectancy", page_life_expectancy)
        yield Result(state=State.OK, summary=infotext)


def _check_lazy_writes(db, params, section):
    obj_id = db + ":Buffer_Manager"
    instance = "None"

    now = time.time()

    value_store = get_value_store()
    levels = params.get("LazyWrites")

    # NOTE: What MSSQL returns under the name lazy_writes/sec is not a rate at all,
    #       but a counter since last server restart, thus we need to calculate the rate
    lwrites = section[(obj_id, instance)]["lazy_writes/sec"]
    lwrites_counter = "mssql_lazy_writes.%s" % db
    value = get_rate(
                value_store,
                lwrites_counter,
                now,
                lwrites,
            )
    infotext = "%.2f lazy_writes/sec" %value
    if levels is not None:
        warn, crit = levels
        levelstext = " (warn, crit at %s/%s)" % (warn, crit)
        yield Metric("perf_LazyWrites", value, levels=(warn, crit))
        if value >= crit: 
            yield Result(state=State.CRIT, summary=infotext+levelstext)
        elif value >= warn:
            yield Result(state=State.WARN, summary=infotext+levelstext)
        else:
            yield Result(state=State.OK, summary=infotext)
    else:
        yield Metric("perf_LazyWrites", value)
        yield Result(state=State.OK, summary=infotext)


def discover_mssql_counters_memory(section):
    # instance is always "None" here
    for (obj_id, instance), counters in iter(section.items()):
        if obj_id.endswith(":Buffer_Manager") and \
                "lazy_writes/sec" in counters and \
                "page_life_expectancy" in counters:
            db = obj_id.split(":")[0]
            memory_manager_obj_id = db + ":Memory_Manager"
            memory_counters = section.get((memory_manager_obj_id, "None"), {})
            if "memory_grants_pending" in memory_counters \
		    and "total_server_memory_(kb)" in memory_counters \
		    and "target_server_memory_(kb)" in memory_counters:
                yield Service(item=db)


def check_mssql_counters_memory(item, params, section):
    yield from _check_lazy_writes(item, params, section)
    yield from _check_page_life_expectancy(item, params, section)
    yield from _check_memory_grants(item, params, section)
    yield from _check_memory_usage(item, params, section)


register.check_plugin(
    name='mssql_counters_memory',
    service_name="Memory %s",
    sections=['mssql_counters'],
    check_function=check_mssql_counters_memory,
    discovery_function=discover_mssql_counters_memory,
    check_ruleset_name="mssql_counters_memory",
    check_default_parameters={
        "LazyWrites" : (20.0, 50.0),
        "page_life_expectancy" : (300, 120),
        "MemoryGrantsPending" : (3, 10),
        "MemoryUsage" : (80.0, 90.0),
    }
)
