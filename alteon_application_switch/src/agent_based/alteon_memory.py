#!/usr/bin/env python3

from .agent_based_api.v1 import (
    register,
    SNMPTree, 
    startswith,
    Service,
    Result,
    State,
    Metric,
)

# [[['97619512', '49935420', '1876.988', '1174.395']], [['3', '2'], ['2', '2']]]
def parse_alteon_memory(string_table):
    values = {}
    values['global'] = {}
    values['cores'] = {}

    values['global']['MpMemStatsTotal'] = float(string_table[0][0][0])
    values['global']['MpMemStatsFree'] = float(string_table[0][0][1])
    values['global']['MpMemStatsVirtual'] = float(string_table[0][0][2]) * 1024
    values['global']['MpMemStatsRss'] = float(string_table[0][0][3]) * 1024

    for core_id, usage in zip(range(0, len(string_table[1])), string_table[1]):
        values['cores'][core_id] = {}
        values['cores'][core_id]["PeakMemUsageSP"] = float(usage[0])
        values['cores'][core_id]["CurrentMemUsageSP"] = float(usage[1])
        values['cores'][core_id]["SpMemUseStatsCurFrontEndSessions"] = int(usage[2]) * 1024
        values['cores'][core_id]["SpMemUseStatsAvgFrontEndSessions"] = int(usage[3]) * 1024
        values['cores'][core_id]["SpMemUseStatsMaxAllowConnections"] = int(usage[4]) * 1024

    return values


register.snmp_section(
    name="alteon_memory",
    detect=startswith('.1.3.6.1.2.1.1.1.0', "Alteon Application Switch"),
    parse_function=parse_alteon_memory,
    fetch=[
        SNMPTree(
            base='.1.3.6.1.4.1.1872.2.5.1.2.8',
            oids=[
                 '1', # MpMemStatsTotal - System Memory stats – total (/stats/mp/mem)
                 '3', # MpMemStatsFree - System Memory stats – free
                 '4', # mpMemStatsVirtual - MP Virtual memory in KB
                 '5', # mpMemStatsRss - MP Resident(RSS Linux) memory in KB
            ],
        ),
        SNMPTree(
             base='.1.3.6.1.4.1.1872.2.5.1.2.4.5.1',
             oids=[
                 '12', # Peak memory used from 1st watermark
                 '14', # Memory used from 1st watermark
                 '10', # spMemUseStatsCurFrontEndSessions
                 '11', # spMemUseStatsAvgFrontEndSessions
                 '18', # spMemUseStatsMaxAllowConnections
             ]
        ),
    ],
)


def discover_alteon_memory(section):
    tresholds = {}
    tresholds["alteon_memory_tresholds"] = {
        "percentVirtual": (75, 90),
        "percentRss": (75, 90),
        "CurrentSP": (75, 90),
    }

    yield Service(item="Alteon Memory", parameters=tresholds)
    for sp_core in section['cores'].keys():
        yield Service(item="Alteon Memory SP Core {}".format(sp_core + 1),
                        parameters=tresholds)


def check_alteon_memory(item, params, section):

    yield Result(state=State.OK, summary="{}:".format(item))

    global_stats = section['global']

    global_stats['percentVirtual'] = global_stats['MpMemStatsVirtual'] / global_stats['MpMemStatsTotal'] * 100
    global_stats['percentRss'] = global_stats['MpMemStatsRss'] / global_stats['MpMemStatsTotal'] * 100

    if item == "Alteon Memory":
        for key, val in global_stats.items():
            val_perfdata = None
            if key in params["alteon_memory_tresholds"].keys():
                val_perfdata = params["alteon_memory_tresholds"][key]
                if val > params["alteon_memory_tresholds"][key][1]:
                    yield Result(state=State.CRIT, summary="{}:{}".format(key, val))
                elif val > params["alteon_memory_tresholds"][key][0]:
                    yield Result(state=State.WARN, summary="{}:{}".format(key, val))
                else:
                    yield Result(state=State.OK, summary="{}:{}".format(key, val))
            yield Metric(key, val, levels=val_perfdata)

    ######
    elif item.startswith("Alteon Memory SP Core"):
        if not "CurrentSP" in params["alteon_memory_tresholds"].keys():
            params["alteon_memory_tresholds"]["CurrentSP"] = params["alteon_memory_tresholds"]["Peak"]
        warn, crit = params["alteon_memory_tresholds"]["CurrentSP"]
        core_id = int(item.split()[4]) - 1
        for key, val in section['cores'][core_id].items():
            val_perfdata = None
            if key.startswith("Current"):
                val_perfdata = (warn, crit)
                if val > crit:
                    yield Result(state=State.CRIT, summary="{}:{}".format(key, val))
                elif val >  warn:
                    yield Result(state=State.WARN, summary="{}:{}".format(key, val))
                else:
                    yield Result(state=State.OK, summary="{}:{}".format(key, val))

            yield Metric(key, val, levels=val_perfdata)


register.check_plugin(
    name='alteon_memory',
    service_name='%s',
    discovery_function=discover_alteon_memory,
    check_function=check_alteon_memory,
    check_ruleset_name='alteon_memory',
    check_default_parameters={},
)
