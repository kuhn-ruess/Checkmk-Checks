#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from collections.abc import Mapping
from typing import Any

from cmk.agent_based.v2 import (
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Result,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    State,
    StringTable,
    check_levels,
    equals,
    render,
)


_STATE_NAMES = {
    1: "idle",
    2: "autofind",
    3: "typeNotMatch",
    4: "fault",
    5: "config",
    6: "configFailed",
    7: "download",
    8: "normal",
    9: "committing",
    10: "commitFailed",
    11: "standby",
    12: "verMismatch",
    13: "nameConflicted",
    14: "invalid",
}

_CRIT_STATES = {4, 6, 10, 13, 14}
_WARN_STATES = {11, 12}


class APInfo:
    def __init__(self, run_state, ip_address, up_traffic, down_traffic, num_users):
        self.run_state = run_state
        self.ip_address = ip_address
        self.up_traffic = up_traffic
        self.down_traffic = down_traffic
        self.num_users = num_users


Section = dict[str, APInfo]


def parse_huawei_wlc(string_table: StringTable) -> Section:
    section: Section = {}
    for line in string_table:
        name, run_state, ip_address, up_traffic, down_traffic, num_users = line
        section[name] = APInfo(
            run_state=int(run_state),
            ip_address=ip_address,
            up_traffic=int(up_traffic),
            down_traffic=int(down_traffic),
            num_users=int(num_users),
        )
    return section


snmp_section_huawei_wlc = SimpleSNMPSection(
    name="huawei_wlc",
    parse_function=parse_huawei_wlc,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.2011.6.139.13.3.3.1",
        oids=[
            "4",   # hwWlanApName
            "6",   # hwWlanApRunState
            "13",  # hwWlanApIpAddress
            "58",  # hwWlanApAirportUpTraffic
            "59",  # hwWlanApAirportDwTraffic
            "44",  # hwWlanApOnlineUserNum
        ],
    ),
    detect=equals(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.2011.2.240.6"),
)


def discover_huawei_wlc(section: Section) -> DiscoveryResult:
    for name in section:
        yield Service(item=name)


def check_huawei_wlc(item: str, params: Mapping[str, Any], section: Section) -> CheckResult:
    ap = section.get(item)
    if ap is None:
        return

    if ap.run_state in _CRIT_STATES:
        state = State.CRIT
    elif ap.run_state in _WARN_STATES:
        state = State.WARN
    else:
        state = State.OK

    state_name = _STATE_NAMES.get(ap.run_state, "unknown")

    yield Result(
        state=state,
        summary="State: {}, IP: {}, Traffic up/down {}/{}, User Online: {}".format(
            state_name,
            ap.ip_address,
            render.bytes(ap.up_traffic),
            render.bytes(ap.down_traffic),
            ap.num_users,
        ),
    )

    yield from check_levels(
        value=ap.num_users,
        levels_upper=params.get("levels_users"),
        metric_name="users",
        label="Users online",
        render_func=lambda v: str(int(v)),
        notice_only=True,
    )


check_plugin_huawei_wlc = CheckPlugin(
    name="huawei_wlc",
    sections=["huawei_wlc"],
    service_name="AP %s",
    discovery_function=discover_huawei_wlc,
    check_function=check_huawei_wlc,
    check_default_parameters={"levels_users": ("no_levels", None)},
    check_ruleset_name="huawei_wlc",
)
