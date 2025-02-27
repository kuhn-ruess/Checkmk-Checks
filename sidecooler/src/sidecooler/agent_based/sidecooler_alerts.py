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

class SidecoolerAlerts():
    num_alerts: int
    alerts: dict

    def __init__(self, num_alerts, alert1, alert2, alert3, alert4, alert5, alert6, alert7, alert8, alert9, alert10):
        self.num_alerts = int(num_alerts)
        self.alerts = {
            "1": alert1,
            "2": alert2,
            "3": alert3,
            "4": alert4,
            "5": alert5,
            "6": alert6,
            "7": alert7,
            "8": alert8,
            "9": alert9,
            "10": alert10,
        }


def parse_sidecooler_alerts(string_table):
    if not string_table:
        return None

    snmp_data = [s for s in string_table[0]]

    return SidecoolerAlerts(*snmp_data)


def discover_sidecooler_alerts(section):
    yield Service()


def check_sidecooler_alerts(section):
    yield Metric("alerts", section.num_alerts)

    summary = f"Current amount of failures: {section.num_alerts}"
    details = ""
    for alert in section.alerts.keys():
        if section.alerts[alert] is not None:
            details += f"{section.alerts[alert]}\n"

    if len(details) == 0:
        details = None

    if section.num_alerts > 0:
        yield Result(state=State.CRIT, summary=summary, details=details)
    else:
        yield Result(state=State.OK, summary=summary, details=details)


snmp_section_sidecooler_alerts = SimpleSNMPSection(
    name = "sidecooler_alerts",
    parse_function = parse_sidecooler_alerts,
    fetch = SNMPTree(
        base = ".1.3.6.1.4.1.46984.17.1",
        oids = [
            "10",   # SideCoolerMib::numAlert
            "11",   # SideCoolerMib::alert1
            "12",   # SideCoolerMib::alert2
            "13",   # SideCoolerMib::alert3
            "14",   # SideCoolerMib::alert4
            "15",   # SideCoolerMib::alert5
            "16",   # SideCoolerMib::alert6
            "17",   # SideCoolerMib::alert7
            "18",   # SideCoolerMib::alert8
            "19",   # SideCoolerMib::alert9
            "20",   # SideCoolerMib::alert10
        ],
    ),
    detect = exists(".1.3.6.1.4.1.46984.17.1.*"),
)


check_plugin_sidecooler_alerts = CheckPlugin(
    name = "sidecooler_alerts",
    service_name = "Sidecooler alerts",
    discovery_function = discover_sidecooler_alerts,
    check_function = check_sidecooler_alerts,
)
