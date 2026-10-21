#!/usr/bin/env python3
"""
XFS project quotas

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

import time
from collections import Counter
from dataclasses import dataclass

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    GetRateError,
    Metric,
    Result,
    Service,
    State,
    StringTable,
    check_levels,
    get_average,
    get_rate,
    get_value_store,
    render,
)

GIB = 1024**3


@dataclass(frozen=True)
class Quota:
    """One project quota, block values in bytes."""

    mountpoint: str
    device: str
    project: str
    used: int
    soft: int
    hard: int
    inodes_used: int
    inodes_soft: int
    inodes_hard: int


Section = dict[str, Quota]


def parse_xfs_quota(string_table: StringTable) -> Section:
    """Parse lines mountpoint:device:project:used:soft:hard:iused:isoft:ihard (blocks in KiB)."""
    quotas = []
    for line in string_table:
        fields = " ".join(line).split(":")
        if len(fields) != 9:
            continue
        mountpoint, device, project = fields[:3]
        try:
            used, soft, hard, inodes_used, inodes_soft, inodes_hard = (int(v) for v in fields[3:])
        except ValueError:
            continue
        quotas.append(
            Quota(
                mountpoint,
                device,
                project,
                used * 1024,
                soft * 1024,
                hard * 1024,
                inodes_used,
                inodes_soft,
                inodes_hard,
            )
        )
    names = Counter(quota.project for quota in quotas)
    return {
        (
            f"{quota.project} ({quota.mountpoint})"
            if names[quota.project] > 1 and quota.mountpoint
            else quota.project
        ): quota
        for quota in quotas
    }


agent_section_xfs_quota = AgentSection(
    name="xfs_quota",
    parse_function=parse_xfs_quota,
)


def discover_xfs_quota(section: Section) -> DiscoveryResult:
    """One service per project with a block or inode limit."""
    for item, quota in section.items():
        if quota.soft or quota.hard or quota.inodes_soft or quota.inodes_hard:
            yield Service(item=item)


def effective_limit(soft: int, hard: int, basis: str) -> int:
    """The limit that counts as 100 percent, falling back to the other one if unset."""
    if basis == "soft":
        return soft or hard
    return hard or soft


def magic_percent(level: float, factor: float, size: float, params: dict) -> float:
    """Adjust a used space level in percent by the magic factor, like the df check."""
    relative = size / (params.get("normsize", 20) * GIB)
    true_factor = relative**factor / relative
    return 100 - (100 - level) * true_factor


def used_levels(params: dict, size: int) -> tuple[tuple[float, float] | None, bool]:
    """Warn and crit for the used bytes, and whether the magic factor changed them."""
    kind, levels = params["levels"]
    if levels[0] != "fixed":
        return None, False
    warn, crit = levels[1]
    if kind in ("used_absolute", "free_absolute"):
        if kind == "free_absolute":
            return (size - warn, size - crit), False
        return (warn, crit), False

    if kind == "free_percent":
        warn, crit = 100 - warn, 100 - crit
    magic = params.get("magic")
    if magic and magic["factor"] != 1.0:
        warn = max(magic_percent(warn, magic["factor"], size, magic), magic["minimum_warn"])
        crit = max(magic_percent(crit, magic["factor"], size, magic), magic["minimum_crit"])
    return (size * warn / 100, size * crit / 100), bool(magic and magic["factor"] != 1.0)


def check_space(params: dict, quota: Quota, size: int) -> CheckResult:
    """Used space against the levels, plus the df like metrics."""
    levels, magic_applied = used_levels(params, size)
    used_percent = quota.used * 100 / size
    state = State.OK
    if levels:
        if quota.used >= levels[1]:
            state = State.CRIT
        elif quota.used >= levels[0]:
            state = State.WARN

    summary = f"Used: {render.percent(used_percent)} ({render.bytes(quota.used)} of {render.bytes(size)})"
    if levels and (state is not State.OK or magic_applied):
        summary += (
            f" (warn/crit at {render.bytes(levels[0])}/{render.bytes(levels[1])},"
            f" {render.percent(levels[0] * 100 / size)}/{render.percent(levels[1] * 100 / size)})"
        )
    yield Result(state=state, summary=summary)
    yield Metric("fs_used", quota.used, levels=levels, boundaries=(0, size))
    yield Metric("fs_free", max(size - quota.used, 0), boundaries=(0, None))
    yield Metric("fs_size", size, boundaries=(0, None))
    yield Metric(
        "fs_used_percent",
        used_percent,
        levels=(levels[0] * 100 / size, levels[1] * 100 / size) if levels else None,
        boundaries=(0.0, 100.0),
    )


def check_limits(params: dict, quota: Quota) -> CheckResult:
    """State for a reached hard limit or an exceeded soft limit."""
    for label, used, soft, hard, render_func in (
        ("Block", quota.used, quota.soft, quota.hard, render.bytes),
        ("Inode", quota.inodes_used, quota.inodes_soft, quota.inodes_hard, str),
    ):
        if hard and used >= hard:
            yield Result(
                state=State(params["state_hard"]),
                summary=f"{label} hard limit of {render_func(hard)} reached",
            )
        elif soft and used > soft:
            yield Result(
                state=State(params["state_soft"]),
                summary=f"{label} soft limit of {render_func(soft)} exceeded",
            )
    yield Result(
        state=State.OK,
        notice=(
            f"Block limits: soft {render.bytes(quota.soft) if quota.soft else 'none'},"
            f" hard {render.bytes(quota.hard) if quota.hard else 'none'}"
        ),
    )
    yield Result(
        state=State.OK,
        notice=(
            f"Inode limits: soft {quota.inodes_soft or 'none'},"
            f" hard {quota.inodes_hard or 'none'}"
        ),
    )


def check_inodes(params: dict, quota: Quota) -> CheckResult:
    """Used inodes in percent of the inode limit."""
    limit = effective_limit(quota.inodes_soft, quota.inodes_hard, params["limit"])
    if not limit:
        yield Result(state=State.OK, notice=f"Inodes used: {quota.inodes_used}")
        yield Metric("inodes_used", quota.inodes_used)
        return
    levels = params["inode_levels"]
    yield from check_levels(
        quota.inodes_used * 100 / limit,
        levels_upper=levels,
        render_func=render.percent,
        label=f"Inodes used ({quota.inodes_used} of {limit})",
        notice_only=True,
    )
    absolute = (
        (limit * levels[1][0] / 100, limit * levels[1][1] / 100) if levels[0] == "fixed" else None
    )
    yield Metric("inodes_used", quota.inodes_used, levels=absolute, boundaries=(0, limit))


def check_trend(params: dict, quota: Quota, size: int, now: float) -> CheckResult:
    """Growth per trend range and time left until the limit is reached."""
    range_hours = params.get("trend_range")
    if not range_hours:
        return
    range_sec = range_hours * 3600
    value_store = get_value_store()
    try:
        rate = get_rate(value_store, "trend.delta", now, quota.used)
    except GetRateError:
        yield Result(state=State.OK, notice="Trend: not enough data yet")
        return
    average = get_average(value_store, "trend.average", now, rate, range_sec / 60)
    in_range = average * range_sec

    yield Metric("fs_growth", rate)
    yield Metric("fs_trend", average)
    yield from check_levels(
        in_range,
        levels_upper=params.get("trend_bytes"),
        render_func=lambda x: ("+" if x >= 0 else "") + render.bytes(x),
        label=f"Trend per {render.timespan(range_sec)}",
        notice_only=True,
    )
    yield from check_levels(
        in_range * 100 / size,
        levels_upper=params.get("trend_perc"),
        render_func=lambda x: ("+" if x >= 0 else "") + render.percent(x),
        label=f"Trend per {render.timespan(range_sec)}",
        notice_only=True,
    )
    free = max(size - quota.used, 0)
    if in_range > 0:
        seconds_left = free / in_range * range_sec
        if seconds_left < 10 * 365 * 86400:
            yield from check_levels(
                seconds_left,
                levels_lower=params.get("trend_timeleft"),
                metric_name="trend_hoursleft",
                render_func=render.timespan,
                label="Time left until quota full",
                notice_only=True,
            )


def check_xfs_quota(item: str, params: dict, section: Section) -> CheckResult:
    """Used space and inodes of one project quota against levels, limits and trend."""
    if (quota := section.get(item)) is None:
        return

    size = effective_limit(quota.soft, quota.hard, params["limit"])
    if size:
        yield from check_space(params, quota, size)
    else:
        yield Result(state=State.OK, summary=f"Used: {render.bytes(quota.used)}, no block limit set")
        yield Metric("fs_used", quota.used, boundaries=(0, None))

    yield from check_limits(params, quota)
    yield from check_inodes(params, quota)
    if quota.mountpoint:
        yield Result(
            state=State.OK,
            notice=f"Filesystem: {quota.mountpoint}" + (f" ({quota.device})" if quota.device else ""),
        )
    if size:
        yield from check_trend(params, quota, size, time.time())


check_plugin_xfs_quota = CheckPlugin(
    name="xfs_quota",
    service_name="XFS Quota on %s",
    discovery_function=discover_xfs_quota,
    check_function=check_xfs_quota,
    check_ruleset_name="xfs_quota",
    check_default_parameters={
        "levels": ("used_percent", ("fixed", (80.0, 90.0))),
        "limit": "hard",
        "state_soft": 1,
        "state_hard": 2,
        "inode_levels": ("fixed", (80.0, 90.0)),
        "trend_range": 24,
    },
)
