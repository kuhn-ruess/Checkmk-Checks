#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

import json
import re

from cmk.agent_based.v2 import (
    AgentSection,
    check_levels,
    CheckPlugin,
    HostLabel,
    Metric,
    render,
    Result,
    Service,
    State,
)

SIZE_UNITS = {
    "B": 1,
    "KB": 1024,
    "MB": 1024 ** 2,
    "GB": 1024 ** 3,
    "TB": 1024 ** 4,
}

UPTIME_UNITS = {
    "w": 604800,
    "d": 86400,
    "h": 3600,
    "m": 60,
    "s": 1,
}

UPTIME_TOKEN = re.compile(r"(\d+)\s*([wdhms])")


def parse_size(value):
    """Turn a size like '920.39 MB' into bytes."""
    if not value:
        return None
    match = re.match(r"\s*([\d.]+)\s*([KMGT]?B)\s*$", str(value), re.IGNORECASE)
    if not match:
        return None
    return int(float(match.group(1)) * SIZE_UNITS[match.group(2).upper()])


def parse_percent(value):
    """Turn a percentage like '10%' into a float."""
    if value is None:
        return None
    try:
        return float(str(value).strip().rstrip("%"))
    except ValueError:
        return None


def parse_uptime(value):
    """Turn an uptime like '15w 3d 15m' into seconds."""
    if not value:
        return None
    seconds = sum(
        int(amount) * UPTIME_UNITS[unit] for amount, unit in UPTIME_TOKEN.findall(str(value))
    )
    return seconds or None


def parse_aruba_ap(string_table):
    """Parse the JSON cencli reports for a single access point."""
    if not string_table:
        return None

    try:
        raw = json.loads("".join(line[0] for line in string_table))
    except ValueError:
        return None

    total = parse_size(raw.get("mem_total"))
    free = parse_size(raw.get("mem_free"))

    return {
        "name": raw.get("name"),
        "status": raw.get("status"),
        "down_reason": raw.get("down_reason"),
        "notes": raw.get("notes"),
        "model": raw.get("model"),
        "serial": raw.get("serial"),
        "mac": raw.get("mac"),
        "ip": raw.get("ip"),
        "version": raw.get("version"),
        "group": raw.get("group"),
        "site": raw.get("site"),
        "mode": raw.get("mode"),
        "swarm_master": raw.get("swarm_master"),
        "ssid_count": raw.get("ssid_count"),
        "clients": raw.get("clients", raw.get("client1", 0)),
        "cpu": parse_percent(raw.get("cpu_%")),
        "mem_total": total,
        "mem_used": total - free if total is not None and free is not None else None,
        "uptime": parse_uptime(raw.get("uptime")),
        "radios": {
            radio["radio_name"]: radio
            for radio in raw.get("radios") or []
            if isinstance(radio, dict) and radio.get("radio_name")
        },
    }


def host_label_aruba_ap(section):
    """Host labels for the Aruba group and site of the access point.

    Labels:
        aruba/group:
            The group the access point belongs to in Aruba Central.
        aruba/site:
            The site the access point belongs to in Aruba Central.
        aruba/model:
            The access point model.
    """
    for key in ("group", "site", "model"):
        if value := section.get(key):
            yield HostLabel(f"aruba/{key}", str(value))


def discover_aruba_ap(section):
    """Discovery"""
    if section.get("status"):
        yield Service()


def check_aruba_ap(params, section):
    """Check"""
    status = section["status"]
    if status == "Up":
        state = State.OK
    elif status == "Down":
        state = State(params["state_down"])
    else:
        state = State(params["state_other"])

    yield Result(state=state, summary=f"Status: {status}")

    if status != "Up" and (reason := section.get("down_reason")):
        yield Result(state=State.OK, summary=f"Reason: {reason}")

    for label, key in (("Model", "model"), ("Version", "version")):
        if value := section.get(key):
            yield Result(state=State.OK, summary=f"{label}: {value}")

    for label, key in (
        ("Serial", "serial"),
        ("MAC", "mac"),
        ("IP", "ip"),
        ("Group", "group"),
        ("Site", "site"),
        ("Mode", "mode"),
        ("SSIDs", "ssid_count"),
        ("Notes", "notes"),
    ):
        if (value := section.get(key)) is not None:
            yield Result(state=State.OK, notice=f"{label}: {value}")

    if section.get("swarm_master"):
        yield Result(state=State.OK, notice="Swarm master")


def discover_aruba_ap_clients(section):
    """Discovery"""
    if section.get("clients") is not None:
        yield Service()


def check_aruba_ap_clients(params, section):
    """Check"""
    if (clients := section.get("clients")) is None:
        yield Result(state=State.OK, summary="No client count reported")
        return

    yield from check_levels(
        clients,
        levels_upper=params.get("levels_clients"),
        metric_name="aruba_ap_clients",
        label="Clients",
        render_func=lambda v: f"{int(v)}",
        boundaries=(0, None),
    )


def discover_aruba_ap_cpu(section):
    """Discovery"""
    if section.get("cpu") is not None:
        yield Service()


def check_aruba_ap_cpu(params, section):
    """Check"""
    if (cpu := section.get("cpu")) is None:
        yield Result(state=State.OK, summary="No CPU utilization reported")
        return

    yield from check_levels(
        cpu,
        levels_upper=params["levels_util"],
        metric_name="util",
        label="Utilization",
        render_func=render.percent,
        boundaries=(0.0, 100.0),
    )


def discover_aruba_ap_memory(section):
    """Discovery"""
    if section.get("mem_used") is not None:
        yield Service()


def check_aruba_ap_memory(params, section):
    """Check"""
    used = section.get("mem_used")
    total = section.get("mem_total")
    if used is None or not total:
        yield Result(state=State.OK, summary="No memory usage reported")
        return

    yield from check_levels(
        100.0 * used / total,
        levels_upper=params["levels_used"],
        metric_name="mem_used_percent",
        label="Used",
        render_func=render.percent,
        boundaries=(0.0, 100.0),
    )
    yield Result(
        state=State.OK,
        summary=f"{render.bytes(used)} of {render.bytes(total)}",
    )
    yield Metric("mem_used", used, boundaries=(0, total))


def discover_aruba_ap_uptime(section):
    """Discovery"""
    if section.get("uptime") is not None:
        yield Service()


def check_aruba_ap_uptime(section):
    """Check"""
    if (uptime := section.get("uptime")) is None:
        yield Result(state=State.OK, summary="No uptime reported")
        return

    yield from check_levels(
        uptime,
        metric_name="uptime",
        label="Up since",
        render_func=render.timespan,
    )


agent_section_aruba_ap = AgentSection(
    name = "aruba_ap",
    parse_function = parse_aruba_ap,
    host_label_function = host_label_aruba_ap,
)

check_plugin_aruba_ap = CheckPlugin(
    name = "aruba_ap",
    service_name = "AP Status",
    discovery_function = discover_aruba_ap,
    check_function = check_aruba_ap,
    check_default_parameters = {
        "state_down": State.CRIT.value,
        "state_other": State.WARN.value,
    },
    check_ruleset_name = "aruba_ap",
)

check_plugin_aruba_ap_clients = CheckPlugin(
    name = "aruba_ap_clients",
    sections = ["aruba_ap"],
    service_name = "AP Clients",
    discovery_function = discover_aruba_ap_clients,
    check_function = check_aruba_ap_clients,
    check_default_parameters = {},
    check_ruleset_name = "aruba_ap_clients",
)

check_plugin_aruba_ap_cpu = CheckPlugin(
    name = "aruba_ap_cpu",
    sections = ["aruba_ap"],
    service_name = "AP CPU utilization",
    discovery_function = discover_aruba_ap_cpu,
    check_function = check_aruba_ap_cpu,
    check_default_parameters = {
        "levels_util": ("fixed", (80.0, 90.0)),
    },
    check_ruleset_name = "aruba_ap_cpu",
)

check_plugin_aruba_ap_memory = CheckPlugin(
    name = "aruba_ap_memory",
    sections = ["aruba_ap"],
    service_name = "AP Memory",
    discovery_function = discover_aruba_ap_memory,
    check_function = check_aruba_ap_memory,
    check_default_parameters = {
        "levels_used": ("fixed", (80.0, 90.0)),
    },
    check_ruleset_name = "aruba_ap_memory",
)

check_plugin_aruba_ap_uptime = CheckPlugin(
    name = "aruba_ap_uptime",
    sections = ["aruba_ap"],
    service_name = "AP Uptime",
    discovery_function = discover_aruba_ap_uptime,
    check_function = check_aruba_ap_uptime,
)
