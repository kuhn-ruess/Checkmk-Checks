#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.agent_based.v2 import (
    Service,
    Result,
    State,
    Metric,
    SimpleSNMPSection,
    SNMPTree,
    exists,
    CheckPlugin,
)

class SidecoolerTemp():
    warm: dict
    cold: dict


    def __init__(self, warm, cold):
        self.warm = warm
        self.cold = cold


def parse_sidecooler_temp(string_table):
    if not string_table:
        return None

    warm = {
        "mean": int(string_table[0][0]) / 10,
        "top": int(string_table[0][1]) / 10,
        "center": int(string_table[0][2]) / 10,
        "bottom": int(string_table[0][3]) / 10,
    }

    cold = {
        "mean": int(string_table[0][4]) / 10,
        "top": int(string_table[0][5]) / 10,
        "center": int(string_table[0][6]) / 10,
        "bottom": int(string_table[0][7]) / 10,
    }

    return SidecoolerTemp(warm, cold)


def discover_sidecooler_temp(section):
    if section.warm:
        yield Service(item="warm")

    if section.cold:
        yield Service(item="cold")


def check_sidecooler_temp(item, params, section):
    if item == "warm":
        data = section.warm
        name = "temp_warm_"
    else:
        data = section.cold
        name = "temp_cold_"

    for which in ("mean", "top", "center", "bottom"):
        warn, crit = params[which]

        if data[which] >= crit:
            yield Result(state=State.CRIT, summary=f"{which.capitalize()}: {data[which]}°C")
        elif data[which] >= warn:
            yield Result(state=State.WARN, summary=f"{which.capitalize()}: {data[which]}°C")
        else:
            yield Result(state=State.OK, summary=f"{which.capitalize()}: {data[which]}°C")

        yield Metric(name=f"{name}{which}", value=data[which], levels=params[which])


snmp_section_sidecooler_temp = SimpleSNMPSection(
    name = "sidecooler_temp",
    parse_function = parse_sidecooler_temp,
    fetch = SNMPTree(
        base = ".1.3.6.1.4.1.46984.17.3",
        oids = [
            "1",   # SideCoolerMib::tempWarmMean
            "2",   # SideCoolerMib::tempWarmTop
            "3",   # SideCoolerMib::tempWarmCenter
            "4",   # SideCoolerMib::tempWarmBottom

            "5",   # SideCoolerMib::tempColdMean
            "6",   # SideCoolerMib::tempColdTop
            "7",   # SideCoolerMib::tempColdCenter
            "8",   # SideCoolerMib::tempColdBottom
        ],
    ),
    detect = exists(".1.3.6.1.4.1.46984.17.3.*"),
)


check_plugin_sidecooler_temp = CheckPlugin(
    name = "sidecooler_temp",
    service_name = "Sidecooler Temp %s side",
    discovery_function = discover_sidecooler_temp,
    check_function = check_sidecooler_temp,
    check_ruleset_name = "sidecooler_temp",
    check_default_parameters = {
        "mean": (30, 35),
        "top": (30, 35),
        "center": (30, 35),
        "bottom": (30, 35),
    },
)
