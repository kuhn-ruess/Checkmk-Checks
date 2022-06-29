#!/usr/bin/env python3

from .agent_based_api.v1 import (
    check_levels,
    render,
    register,
    Service,
    SNMPTree,
    startswith,
)

def parse_gtec_usv_load(string_table):
    line = [int(x) for x in string_table[0]]
    return {
        'phase 1' : line[0],
        'phase 2' : line[1],
        'phase 3' : line[2],
    }


register.snmp_section(
    name="gtec_usv_load",
    parse_function=parse_gtec_usv_load,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.935.1.1.1.8.3",
        oids=[
            "5", #upsThreePhaseOutputLoadPercentageR
            "6", #upsThreePhaseOutputLoadPercentageS
            "7", #upsThreePhaseOutputLoadPercentageT

        ],
    ),
    detect=startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.935"),
)


def discover_gtec_usv_load(section):
    for phase in section:
        yield Service(item=phase)


def check_gtec_usv_load(item, params, section):
    load_raw = section[item]
    load_perc = load_raw / 10
    yield from check_levels(
        value=load_perc,
        levels_upper=params["levels"],
        metric_name="out_load",
        render_func=render.percent,
        label="load",
    )

register.check_plugin(
    name="gtec_usv_load",
    sections=["gtec_usv_load"],
    service_name="OUT Load %s",
    discovery_function=discover_gtec_usv_load,
    check_function=check_gtec_usv_load,
    check_default_parameters={'levels': (85, 90)},
    check_ruleset_name="ups_out_load",
)
