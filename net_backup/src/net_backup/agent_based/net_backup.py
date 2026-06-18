#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Result,
    Service,
    State,
    StringTable,
)


def parse_net_backup(string_table: StringTable) -> dict:
    devices: dict = {}
    last_device = ""
    start = False
    for line in string_table:
        if line == ["Host", "DrivePath", "Status"]:
            start = True
            continue

        if start:
            if len(line) >= 5:
                last_device = line[0]
            elif len(line) == 3:
                devices.setdefault(last_device, [])
                devices[last_device].append(
                    {
                        "client": line[0],
                        "path": line[1],
                        "status": line[2],
                    }
                )
    return devices


agent_section_net_backup = AgentSection(
    name="net_backup",
    parse_function=parse_net_backup,
)


def discovery_net_backup(section: dict) -> DiscoveryResult:
    for device in section:
        yield Service(item=device)


def check_net_backup(item: str, section: dict) -> CheckResult:
    device = section.get(item)
    if not device:
        return

    messages = []
    state = State.OK
    for sub in device:
        append = ""
        if sub["status"] not in ["SCAN-TLD", "TLD", "ACTIVE"]:
            state = State.CRIT
            append = " %s(!!)" % sub["status"]
        messages.append("%s (%s)%s" % (sub["client"], sub["path"], append))

    yield Result(state=state, summary=", ".join(messages))


check_plugin_net_backup = CheckPlugin(
    name="net_backup",
    service_name="Device %s",
    discovery_function=discovery_net_backup,
    check_function=check_net_backup,
)
