#!/usr/bin/env python3
# Copyright (C) 2017  Frank Fegert (fra.nospam.nk@gmx.de)
# Updates and refactoring 2020 by Bastian Kuhn (mail@bastian-kuhn.de)
# Migration to cmk.agent_based.v2 / cmk.rulesets.v1 by Kuhn & Ruess GmbH
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
"""Open-iSCSI session status check.

Example agent output:
  <<<open-iscsi_sessions>>>
  qla4xxx 10.0.0.4:3260,1 iqn.2001-05.com... qla4xxx.84:8f:69:35:fc:70.ipv4.0 none 10.0.0.52 LOGGED_IN Unknown Unknown
  bnx2i 10.0.1.2:3260,1 iqn.2001-05.com... bnx2i.d0:43:1e:51:98:c8 eth2 10.0.1.64 LOGGED_IN LOGGED_IN NO_CHANGE
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


def parse_open_iscsi_sessions(string_table: StringTable) -> StringTable:
    return string_table


def discover_open_iscsi_sessions(section: StringTable) -> DiscoveryResult:
    for line in section:
        if len(line) != 9:
            continue
        (transport, portal, target, ifname, ifnetdev, ifip,
         isessstate, iconnstate, iintstate) = line[:9]
        params = {}
        if isessstate:
            params["session_state"] = isessstate
        if iconnstate:
            params["connection_state"] = iconnstate
        if iintstate:
            params["internal_state"] = iintstate
        yield Service(item="%s / %s" % (ifname, target), parameters=params)


def check_open_iscsi_sessions(item: str, section: StringTable) -> CheckResult:
    for line in section:
        if len(line) != 9:
            continue
        (transport, portal, target, ifname, ifnetdev, ifip,
         isessstate, iconnstate, iintstate) = line[:9]
        if "%s / %s" % (ifname, target) != item:
            continue

        if iconnstate == "Unknown" or iintstate == "Unknown":
            if isessstate == "LOGGED_IN":
                yield Result(state=State.OK,
                             summary="Session is in status %s" % isessstate)
                return
            yield Result(
                state=State.CRIT,
                summary="Session is in status %s. Expected status LOGGED_IN"
                % isessstate)
            return

        if (isessstate == "LOGGED_IN" and iconnstate == "LOGGED_IN"
                and iintstate == "NO_CHANGE"):
            yield Result(
                state=State.OK,
                summary="Session is in status %s/%s/%s."
                % (isessstate, iconnstate, iintstate))
            return
        yield Result(
            state=State.CRIT,
            summary="Session is in status %s/%s/%s. "
            "Expected status LOGGED_IN/LOGGED_IN/NO_CHANGE"
            % (isessstate, iconnstate, iintstate))
        return

    yield Result(
        state=State.CRIT,
        summary="Session is missing. Check iSCSI logins or rerun inventory "
        "if target has been removed permanently")


agent_section_open_iscsi_sessions = AgentSection(
    name="open_iscsi_sessions",
    parse_function=parse_open_iscsi_sessions,
)

check_plugin_open_iscsi_sessions = CheckPlugin(
    name="open_iscsi_sessions",
    service_name="iSCSI Session Status %s",
    discovery_function=discover_open_iscsi_sessions,
    check_function=check_open_iscsi_sessions,
)
