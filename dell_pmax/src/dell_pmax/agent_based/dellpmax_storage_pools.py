#!/usr/bin/env python
"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.agent_based.v2 import (
    Result,
    Service,
    State,
    CheckPlugin,
)

"""
Subscribed Allocated (TB)           18.0
Subscribed Total (TB)               50.3
Usable Used (TB)                    12.61
Usable Total (TB)                   36.67
Effective Used Capacity %           31

subscribed_allocated_tb = SRP Host allocated plus eNas allocated capacity in TBs
subscribed_total_tb = SRP Host subscribed capacity plus eNas subscribed capacity in TBs

usable_used_tb = SRP Total Capacity in TBs used by Host, eNas and System after Data reduction is applied
usable_total_tb = SRP Total system usable capacity in TBs
effective_used_capacity_percen = Total allocated(used) capacity percent of configured (usable) space on the VMAX

Example output:
<<<dellpmax_storage_pools:sep(124)>>>
SRP_1|18.0|50.3|0|0|12.61|36.67|31

Storage Ressource Pool ID|{subscribed_allocated_tb}|{subscribed_total_tb}|{snapshot_modified_tb}|{snapshot_total_tb}|{usable_used_tb}|{usable_total_tb}|{effective_used_capacity_percent}
"""


def discover_dellpmax_storage_pools(section):
    for line in section:
        yield Service(item=line[0])


def check_dellpmax_storage_pools_subscribed(item, section):
    for line in section:
        if line[0] == item:
            subscribed_used_percent = 100 * float(line[1]) / float(line[2])
            if subscribed_used_percent > 90:
                state = State.CRIT
            elif subscribed_used_percent > 80:
                state = State.WARN
            else:
                state = State.OK
            summary = "Subscribed Allocated (TB): {0}, Subscribed Total (TB): {1}, Subscribed Used: {2}%".format(
                line[1], line[2], "{:0.1f}".format(subscribed_used_percent)
            )
        yield Result(state=state, summary=summary)


check_plugin_dell_pmax_storage_pools_subscripted = CheckPlugin(
    name="dellpmax_storage_pools_subscribed",
    sections=["dellpmax_storage_pools"],
    service_name="Subscribed Capacity %s",
    discovery_function=discover_dellpmax_storage_pools,
    check_function=check_dellpmax_storage_pools_subscribed,
)


def check_dellpmax_storage_pools_snapshot(item, section):
    for line in section:
        if line[0] == item:
            summary = "Snapshot Modified (TB): {3}, Snapshot Total (TB): {4}".format(*line)
            yield Result(state=State.OK, summary=summary)


check_plugin_dell_pmax_storage_pools_snapshot = CheckPlugin(
    name="dellpmax_storage_pools_snapshot",
    sections=["dellpmax_storage_pools"],
    service_name="Snapshot Capacity %s",
    discovery_function=discover_dellpmax_storage_pools,
    check_function=check_dellpmax_storage_pools_snapshot,
)


def check_dellpmax_storage_pools_usable(item, section):
    for line in section:
        if line[0] == item:
            effective_used_capacity_percent = int(line[7])
            if effective_used_capacity_percent > 90:
                state = State.CRIT
            elif effective_used_capacity_percent > 80:
                state = State.WARN
            else:
                state = State.OK
            summary = "Usable Used (TB): {5}, Usable Total (TB): {6}, Effective Used: {7}%".format(
                *line
            )
            yield Result(state=state, summary=summary)


check_plugin_dell_pmax_storage_pools = CheckPlugin(
    name="dellpmax_storage_pools",
    service_name="Usable Capacity %s",
    discovery_function=discover_dellpmax_storage_pools,
    check_function=check_dellpmax_storage_pools_usable,
)
