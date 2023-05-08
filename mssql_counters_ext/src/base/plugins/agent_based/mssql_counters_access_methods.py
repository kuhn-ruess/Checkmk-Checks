#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# MSSQL_SQL2012T:Access_Methods full_scans/sec None 292076 
# MSSQL_SQL2012T:Access_Methods index_searches/sec None 27662568
#

from contextlib import suppress
from .agent_based_api.v1 import get_rate, get_value_store, register, Service, Result, State, Metric, GetRateError
import time


def discover_mssql_counters_access_methods(section):
    # instance is always "None" here
    for (obj_id, instance), counters in iter(section.items()):
        if obj_id.endswith(":Access_Methods") and \
                "full_scans/sec" in counters and \
                "index_searches/sec" in counters:
            yield Service(item=obj_id.split(":")[0])


def check_mssql_access_methods(item, params, section):
    if not section:
        return
    db = item
    obj_id = db + ":Access_Methods"
    instance = "None"

    now = time.time()

    value_store = get_value_store()

    fsrate = None
    with suppress(GetRateError):
        fscans = section[(obj_id, instance)]["full_scans/sec"]
        fscans_counter = "mssql_fscans.%s" % db
        fsrate = get_rate(
                    value_store,
                    fscans_counter,
                    now,
                    fscans,
                )
        finfotext = "%.2f full_scans/sec" % fsrate
        levels = params.get("AccessFullScans")
        if levels is not None:
            warn, crit = levels
            levelstext = " (warn/crit at %.2f/%.2f)" % levels
            yield Metric("perf_AccessFullScans", fsrate, levels=levels)
            if fsrate >= crit:
                yield Result(state=State.CRIT, summary=finfotext + levelstext)
            elif fsrate >= warn:
                yield Result(state=State.WARN, summary=finfotext + levelstext)
            else:
                yield Result(state=State.OK, summary=finfotext)
        else:
            yield Metric("perf_AccessFullScans", fsrate)
            yield Result(state=State.OK, summary=finfotext)


    israte = None
    with suppress(GetRateError):
        isearch = section[(obj_id, instance)]["index_searches/sec"]
        isearch_counter = "mssql_isearch.%s" % db
        israte = get_rate(
                    value_store,
                    isearch_counter,
                    now,
                    isearch
                )
        iinfotext = "%.2f index_searches/sec" % israte
        levels = params.get("AccessIndexSearches")
        if levels is not None:
            warn, crit = levels
            levelstext = " (warn/crit at %.2f/%.2f)" % levels
            yield Metric("perf_AccessIndexSearches" , israte, levels=levels)
            if israte >= crit:
                yield Result(state=State.CRIT, summary=iinfotext + levelstext)
            elif israte > warn:
                yield Result(state=State.WARN, summary=iinfotext + levelstext)
            else:
                yield Result(state=State.OK, summary=iinfotext)
        else:
            yield Metric("perf_AccessIndexSearches" , israte)
            yield Result(state=State.OK, summary=iinfotext)

    if israte is not None and fsrate is not None and (israte + fsrate) != 0:
        if fsrate != 0:
            ispfs = israte / fsrate
            yield Metric("index_searches_per_full_scan", ispfs)
            yield Result(state=State.OK, summary=" %.2f IndexSearches per FullScan" % ispfs)
        index_hitratio_perc = (israte / (israte + fsrate)) * 100
        infotext = "Index hit ratio: %.2f%%" % index_hitratio_perc
        levels = params.get("index_hit_ratio")
        if levels is not None:
            warn, crit = levels
            levelstext = " (warn/crit below %.1f/%.1f%%)" % levels
            yield Metric("index_hitratio", index_hitratio_perc, levels=levels)
            if index_hitratio_perc < crit:
                yield Result(state=State.CRIT, summary=infotext + levelstext)
            elif index_hitratio_perc < warn:
                yield Result(state=State.WARN, summary=infotext + levelstext)
            else:
                yield Result(state=State.OK, summary=infotext)
        else:
            yield Metric("index_hitratio", index_hitratio_perc)
            yield Result(state=State.OK, summary=infotext)
    elif israte is None and fsrate is None:
        raise GetRateError


register.check_plugin(
    name='mssql_counters_access_methods',
    service_name='%s Access Index Usage',
    sections=['mssql_counters'],
    discovery_function=discover_mssql_counters_access_methods,
    check_function=check_mssql_access_methods,
    check_ruleset_name="mssql_counters_access_methods",
    check_default_parameters={
        "AccessFullScans" :  (50.0, 100.0),
        "AccessIndexSearches" :  (500.0, 1000.0),
        "index_hit_ratio" :  (5.0, 1.0),
    }
)
