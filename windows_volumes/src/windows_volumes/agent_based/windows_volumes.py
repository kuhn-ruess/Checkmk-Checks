#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from collections.abc import Mapping
from dataclasses import dataclass

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
    check_levels,
    render,
)


@dataclass(frozen=True)
class Volume:
    """One Windows volume that is mounted into a folder."""
    label: str
    health: str
    op_status: str
    size: int
    free: int
    fs_type: str
    access_path: str


Section = Mapping[str, Volume]


def parse_windows_volumes(string_table: StringTable) -> Section:
    """
    Parse the agent output (one pipe separated line per folder mount).

    Layout per line:
        label | health | operational status | size | free | fs type | access path

    The volume label is used as the service item. When the same label shows up
    more than once (a volume can be mounted into several folders), the repeated
    items are numbered ("<label>", "<label> 2", ...) so none get lost.
    """
    section: dict[str, Volume] = {}
    seen: dict[str, int] = {}
    for line in string_table:
        if len(line) < 7:
            continue
        label, health, op_status, size_raw, free_raw, fs_type, access_path = line[:7]
        try:
            size = int(size_raw)
            free = int(free_raw)
        except ValueError:
            continue

        name = label or access_path
        seen[name] = seen.get(name, 0) + 1
        item = name if seen[name] == 1 else f"{name} {seen[name]}"

        section[item] = Volume(
            label=label,
            health=health,
            op_status=op_status,
            size=size,
            free=free,
            fs_type=fs_type,
            access_path=access_path,
        )
    return section


def discover_windows_volumes(section: Section) -> DiscoveryResult:
    """One service per folder mounted volume."""
    for item in section:
        yield Service(item=item)


def _levels_upper(params: Mapping):
    """
    Read the upper usage levels (in percent) from the "filesystem" ruleset.

    Handles the current form-spec shape (("fixed", (warn, crit)) /
    ("no_levels", None)) as well as the legacy bare (warn, crit) tuple, so the
    standard filesystem rule can be used to configure this check.
    """
    levels = params.get("levels")
    if isinstance(levels, tuple) and len(levels) == 2:
        first, second = levels
        if first == "no_levels":
            return ("no_levels", None)
        if first == "fixed" and isinstance(second, tuple):
            return ("fixed", second)
        if isinstance(first, (int, float)) and isinstance(second, (int, float)):
            return ("fixed", (float(first), float(second)))
    return ("fixed", (80.0, 90.0))


def check_windows_volumes(item: str, params: Mapping, section: Section) -> CheckResult:
    volume = section.get(item)
    if volume is None:
        return

    # Health: anything that is not explicitly Healthy/OK is treated as CRIT.
    healthy = volume.health.lower() in ("healthy", "ok")
    op_ok = volume.op_status.lower() in ("ok", "")
    yield Result(
        state=State.OK if healthy and op_ok else State.CRIT,
        summary=f"Health: {volume.health or 'unknown'}, "
                f"Status: {volume.op_status or 'unknown'}",
    )

    if volume.fs_type:
        yield Result(state=State.OK, notice=f"Filesystem type: {volume.fs_type}")
    if volume.access_path:
        yield Result(state=State.OK, notice=f"Mount path: {volume.access_path}")

    if volume.size <= 0:
        yield Result(state=State.UNKNOWN, summary="No size information available")
        return

    used = volume.size - volume.free
    used_percent = used / volume.size * 100.0

    yield from check_levels(
        used_percent,
        levels_upper=_levels_upper(params),
        metric_name="windows_volume_used_percent",
        label="Used",
        render_func=render.percent,
        boundaries=(0.0, 100.0),
    )
    yield Result(
        state=State.OK,
        summary=f"{render.bytes(used)} of {render.bytes(volume.size)} used, "
                f"{render.bytes(volume.free)} free",
    )
    yield Metric("windows_volume_used", float(used), boundaries=(0.0, float(volume.size)))
    yield Metric("windows_volume_size", float(volume.size))


agent_section_windows_volumes = AgentSection(
    name="windows_volumes",
    parse_function=parse_windows_volumes,
)


check_plugin_windows_volumes = CheckPlugin(
    name="windows_volumes",
    service_name="Filesystem %s",
    discovery_function=discover_windows_volumes,
    check_function=check_windows_volumes,
    check_ruleset_name="windows_volumes",
    check_default_parameters={"levels": ("fixed", (80.0, 90.0))},
)
