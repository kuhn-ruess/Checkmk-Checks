#!/usr/bin/env python3
# Copyright (C) 2017  Frank Fegert (fra.nospam.nk@gmx.de)
# Updates and refactoring 2020 by Bastian Kuhn (mail@bastian-kuhn.de)
# Migration to cmk.agent_based.v2 / cmk.rulesets.v1 by Kuhn & Ruess GmbH
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
"""Open-iSCSI session statistics check.

Example agent output:
  <<<open-iscsi_session_stats>>>
  [session stats d0:43:1e:51:98:c8 iqn.2001-05.com.equallogic:0-fe83b6-6a4bb57cc-782004ecbf25784d]
  txdata_octets: 337207169024
  rxdata_octets: 881317587
  ...
"""

import time

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Metric,
    Result,
    Service,
    State,
    StringTable,
    get_rate,
    get_value_store,
    render,
)

# Ordered list of (description, counter) pairs (PDU stats, see RFC 3720).
SESSION_STATS_COUNTERS = [
    ('In', 'rxdata_octets'),
    ('Out', 'txdata_octets'),
    ('TX NOP', 'noptx_pdus'),
    ('TX SCSI Command Request', 'scsicmd_pdus'),
    ('TX Task Management Function Command', 'tmfcmd_pdus'),
    ('TX Login Request', 'login_pdus'),
    ('TX Text Request', 'text_pdus'),
    ('TX Data Out', 'dataout_pdus'),
    ('TX Logout Request', 'logout_pdus'),
    ('TX Single Negative ACK', 'snack_pdus'),
    ('RX NOP', 'noprx_pdus'),
    ('RX SCSI Command Response', 'scsirsp_pdus'),
    ('RX Task Management Function Response', 'tmfrsp_pdus'),
    ('RX Text Response', 'textrsp_pdus'),
    ('RX Data In', 'datain_pdus'),
    ('RX Logout Response', 'logoutrsp_pdus'),
    ('RX Ready To Transfer', 'r2t_pdus'),
    ('RX Asynchronous Message', 'async_pdus'),
    ('RX Reject', 'rjt_pdus'),
    ('Error CRC', 'digest_err'),
    ('Error Timeout', 'timeout_err'),
]

MESSAGE_LINE_COUNTERS = {'rxdata_octets', 'txdata_octets'}
ERROR_COUNTERS = {'digest_err', 'timeout_err'}


def parse_open_iscsi_session_stats(string_table: StringTable) -> dict:
    sessions: dict = {}
    mac_target = None
    for line in string_table:
        if len(line) >= 4 and line[0] == "[session" and line[1] == "stats":
            mac_target = " ".join(line[2:4])[:-1]
            sessions[mac_target] = {}
        elif len(line) == 2 and mac_target is not None:
            counter = line[0].replace(":", "")
            sessions[mac_target][counter] = line[1]
    return sessions


def discover_open_iscsi_session_stats(section: dict) -> DiscoveryResult:
    for session in section:
        yield Service(item=session)


def check_open_iscsi_session_stats(item: str, params: dict, section: dict) -> CheckResult:
    if item not in section:
        return
    counters = section[item]
    session_id = item.replace(" ", "_")
    value_store = get_value_store()
    this_time = time.time()

    message = ""
    status = State.OK
    sum_errors = 0

    for descr, counter in SESSION_STATS_COUNTERS:
        if counter not in counters:
            continue
        try:
            t_value = int(counters[counter])
        except ValueError:
            continue
        value_rate = get_rate(
            value_store,
            "%s.%s" % (counter, session_id),
            this_time,
            t_value,
        )

        if counter in MESSAGE_LINE_COUNTERS:
            if message:
                message += ", "
            message += "%s: %s/s" % (descr, render.bytes(value_rate))

        levels = params.get(counter)
        warn = crit = None
        if isinstance(levels, tuple) and levels[0] == "fixed":
            warn, crit = levels[1]

        if crit is not None and crit > 0 and value_rate >= crit:
            message += ", %s: %s/s (!!)" % (descr, value_rate)
            status = State.worst(status, State.CRIT)
        elif warn is not None and warn > 0 and value_rate >= warn:
            message += ", %s: %s/s (!)" % (descr, value_rate)
            status = State.worst(status, State.WARN)
        elif counter in ERROR_COUNTERS:
            sum_errors += value_rate
            if value_rate > 0:
                message += ", %s: %s/s" % (descr, value_rate)

        yield Metric(counter, value_rate)

    if sum_errors == 0:
        message += ", no protocol errors"

    yield Result(state=status, summary="Session Stats: " + message)


agent_section_open_iscsi_session_stats = AgentSection(
    name="open_iscsi_session_stats",
    parse_function=parse_open_iscsi_session_stats,
)

check_plugin_open_iscsi_session_stats = CheckPlugin(
    name="open_iscsi_session_stats",
    service_name="iSCSI Session Stats %s",
    discovery_function=discover_open_iscsi_session_stats,
    check_function=check_open_iscsi_session_stats,
    check_default_parameters={},
    check_ruleset_name="open_iscsi_session_stats",
)
