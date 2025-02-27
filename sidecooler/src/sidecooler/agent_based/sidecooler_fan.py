#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from typing import NamedTuple

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

class SidecoolerFan(NamedTuple):
    power_setpoint: int
    power_current: int
    rpm_current: int
    status: int
    operating_hours: int


class SidecoolerFans():
    fans = {}

    def __init__(self, fan1, fan2, fan3, fan4, fan5, fan6):
        self.fans["1"] = fan1
        self.fans["2"] = fan2
        self.fans["3"] = fan3
        self.fans["4"] = fan4
        self.fans["5"] = fan5
        self.fans["6"] = fan6


def parse_sidecooler_fans(string_table):
    if not string_table:
        return None

    fan1 = SidecoolerFan(*map(int, string_table[0][0:5]))
    fan2 = SidecoolerFan(*map(int, string_table[0][5:10]))
    fan3 = SidecoolerFan(*map(int, string_table[0][10:15]))
    fan4 = SidecoolerFan(*map(int, string_table[0][15:20]))
    fan5 = SidecoolerFan(*map(int, string_table[0][20:25]))
    fan6 = SidecoolerFan(*map(int, string_table[0][25:30]))

    return SidecoolerFans(fan1, fan2, fan3, fan4, fan5, fan6)


def discover_sidecooler_fans(section):
    for fan in section.fans.keys():
        if section.fans[fan].status != 0:
            yield Service(item=fan)


def check_sidecooler_fans(item, params, section):
    fan_state = {
        0: "no fan",
        1: "off",
        2: "running ok",
        3: "error",
    }

    if item not in section.fans.keys():
        yield Result(state=State.UNKNOWN, summary="Item not found")

    if section.fans[item]:
        yield Result(state=State.OK, summary=f"Power setpoint: {section.fans[item].power_setpoint}%")
        yield Result(state=State.OK, summary=f"Power current: {section.fans[item].power_current}%")

        if "upper" in params.keys():
            warn, crit = params["upper"]
            if section.fans[item].rpm_current >= crit:
                yield Result(state=State.CRIT, summary=f"RPM current: {section.fans[item].rpm_current}U/min")
            elif section.fans[item].rpm_current >= warn:
                yield Result(state=State.WARN, summary=f"RPM current: {section.fans[item].rpm_current}U/min")
            else:
                yield Result(state=State.OK, summary=f"RPM current: {section.fans[item].rpm_current}U/min")
            yield Metric(name="fan", value=section.fans[item].rpm_current, levels=params["upper"])
        
        if "lower" in params.keys():
            warn, crit = params["lower"]
            if section.fans[item].rpm_current < crit:
                yield Result(state=State.CRIT, summary=f"RPM current: {section.fans[item].rpm_current}U/min")
            elif section.fans[item].rpm_current < warn:
                yield Result(state=State.WARN, summary=f"RPM current: {section.fans[item].rpm_current}U/min")
            else:
                yield Result(state=State.OK, summary=f"RPM current: {section.fans[item].rpm_current}U/min")
            yield Metric(name="fan", value=section.fans[item].rpm_current, levels=params["lower"])

        if "upper" not in params.keys() and "lower" not in params.keys():
            yield Result(state=State.OK, summary=f"RPM current: {section.fans[item].rpm_current}U/min")
            yield Metric(name="fan", value=section.fans[item].rpm_current)

        if section.fans[item].status in (1, 2):
            yield Result(state=State.OK, summary=f"State: {fan_state[section.fans[item].status]}")
        else:
            yield Result(state=State.CRIT, summary=f"State: {fan_state[section.fans[item].status]}")

        yield Result(state=State.OK, summary=f"Operating hours: {section.fans[item].operating_hours}")


snmp_section_sidecooler_fans = SimpleSNMPSection(
    name = "sidecooler_fans",
    parse_function = parse_sidecooler_fans,
    fetch = SNMPTree(
        base = ".1.3.6.1.4.1.46984.17.3",
        oids = [
            "20",   # SideCoolerMib::vent1PowerSetpoint
            "21",   # SideCoolerMib::vent1PowerCur
            "22",   # SideCoolerMib::vent1RPMCur
            "23",   # SideCoolerMib::vent1Status
            "24",   # SideCoolerMib::vent1OperatingHours

            "30",   # SideCoolerMib::vent2PowerSetpoint
            "31",   # SideCoolerMib::vent2PowerCur
            "32",   # SideCoolerMib::vent2RPMCur
            "33",   # SideCoolerMib::vent2Status
            "34",   # SideCoolerMib::vent2OperatingHours

            "40",   # SideCoolerMib::vent3PowerSetpoint
            "41",   # SideCoolerMib::vent3PowerCur
            "42",   # SideCoolerMib::vent3RPMCur
            "43",   # SideCoolerMib::vent3Status
            "44",   # SideCoolerMib::vent3OperatingHours

            "50",   # SideCoolerMib::vent4PowerSetpoint
            "51",   # SideCoolerMib::vent4PowerCur
            "52",   # SideCoolerMib::vent4RPMCur
            "53",   # SideCoolerMib::vent4Status
            "54",   # SideCoolerMib::vent4OperatingHours

            "60",   # SideCoolerMib::vent5PowerSetpoint
            "61",   # SideCoolerMib::vent5PowerCur
            "62",   # SideCoolerMib::vent5RPMCur
            "63",   # SideCoolerMib::vent5Status
            "64",   # SideCoolerMib::vent5OperatingHours

            "70",   # SideCoolerMib::vent6PowerSetpoint
            "71",   # SideCoolerMib::vent6PowerCur
            "72",   # SideCoolerMib::vent6RPMCur
            "73",   # SideCoolerMib::vent6Status
            "74",   # SideCoolerMib::vent6OperatingHours
        ],
    ),
    detect = exists(".1.3.6.1.4.1.46984.17.3.*"),
)


check_plugin_sidecooler_fans = CheckPlugin(
    name="sidecooler_fans",
    service_name="Sidecooler fan %s",
    discovery_function=discover_sidecooler_fans,
    check_function=check_sidecooler_fans,
    check_ruleset_name = "hw_fans",
    check_default_parameters = {},
)
