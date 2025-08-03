#!/usr/bin/env python3

from cmk.agent_based.v2 import (
    SNMPTree, 
    startswith,
    Service,
    Result,
    State,
    Metric,
    CheckPlugin,
    SNMPSection,
    check_levels,
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


snmp_section_alteon_memory = SNMPSection(
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
    yield Service(item="Alteon Memory")
    for sp_core in section['cores'].keys():
        yield Service(item="Alteon Memory SP Core {}".format(sp_core + 1))


def check_alteon_memory(item, params, section):
    if item == "Alteon Memory":
        yield Result(state=State.OK, summary=f"{item}")
        
        global_stats = section['global']
        # Calculate percentages
        global_stats['percentVirtual'] = global_stats['MpMemStatsVirtual'] / global_stats['MpMemStatsTotal'] * 100
        global_stats['percentRss'] = global_stats['MpMemStatsRss'] / global_stats['MpMemStatsTotal'] * 100

        # Check thresholds for percentage values
        for key in ['percentVirtual', 'percentRss']:
            if key in params["alteon_memory_tresholds"]:
                warn, crit = params["alteon_memory_tresholds"][key]
                yield from check_levels(
                    global_stats[key],
                    levels_upper=(warn, crit),
                    metric_name=key,
                    label=f"Memory {key}",
                    render_func=lambda x: f"{x:.1f}%",
                )
        
        # Yield metrics for other global stats without thresholds
        for key, val in global_stats.items():
            if key not in ['percentVirtual', 'percentRss']:
                yield Metric(key, val)

    elif item.startswith("Alteon Memory SP Core"):
        yield Result(state=State.OK, summary=f"{item}")
        
        core_id = int(item.split()[4]) - 1
        if core_id not in section['cores']:
            return
            
        core_stats = section['cores'][core_id]
        warn, crit = params["alteon_memory_tresholds"]["CurrentSP"]
        
        # Check CurrentMemUsageSP with thresholds
        if "CurrentMemUsageSP" in core_stats:
            yield from check_levels(
                core_stats["CurrentMemUsageSP"],
                levels_upper=(warn, crit),
                metric_name="CurrentMemUsageSP",
                label="Current Memory Usage SP",
                render_func=lambda x: f"{x:.1f}%",
            )
        
        # Yield metrics for other core stats without thresholds
        for key, val in core_stats.items():
            if key != "CurrentMemUsageSP":
                yield Metric(key, val)


check_plugin_alteon_memory = CheckPlugin(     
    name='alteon_memory',
    service_name='%s',
    discovery_function=discover_alteon_memory,
    check_function=check_alteon_memory,
    check_ruleset_name='alteon_memory',
    check_default_parameters={
        "alteon_memory_tresholds": {
            "percentVirtual": ('fixed', (75.0, 90.0)),
            "percentRss": ('fixed', (75.0, 90.0)),
            "CurrentSP": ('fixed', (75.0, 90.0)),
        }
    },
)
