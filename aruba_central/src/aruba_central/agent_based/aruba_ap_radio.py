#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.agent_based.v2 import (
    check_levels,
    CheckPlugin,
    Metric,
    render,
    Result,
    Service,
    State,
)


def discover_aruba_ap_radio(section):
    """Discovery"""
    for name in section.get("radios", {}):
        yield Service(item=name)


def check_aruba_ap_radio(item, params, section):
    """Check"""
    if not (radio := section.get("radios", {}).get(item)):
        return

    status = radio.get("status")
    if status == "Up":
        state = State.OK
    elif status == "Down":
        state = State(params["state_down"])
    else:
        state = State(params["state_other"])
    yield Result(state=state, summary=f"Status: {status}")

    if (utilization := radio.get("utilization")) is not None:
        yield from check_levels(
            float(utilization),
            levels_upper=params["levels_utilization"],
            metric_name="aruba_radio_utilization",
            label="Utilization",
            render_func=render.percent,
            boundaries=(0.0, 100.0),
        )

    if (tx_power := radio.get("tx_power")) is not None:
        yield Result(state=State.OK, summary=f"TX power: {tx_power} dBm")
        yield Metric("aruba_radio_tx_power", float(tx_power))

    for label, key in (
        ("Channel", "channel"),
        ("Type", "radio_type"),
        ("Spatial stream", "spatial_stream"),
        ("MAC", "macaddr"),
    ):
        if (value := radio.get(key)) is not None:
            yield Result(state=State.OK, notice=f"{label}: {value}")


check_plugin_aruba_ap_radio = CheckPlugin(
    name = "aruba_ap_radio",
    sections = ["aruba_ap"],
    service_name = "AP %s",
    discovery_function = discover_aruba_ap_radio,
    check_function = check_aruba_ap_radio,
    check_default_parameters = {
        "state_down": State.WARN.value,
        "state_other": State.WARN.value,
        "levels_utilization": ("fixed", (80.0, 90.0)),
    },
    check_ruleset_name = "aruba_ap_radio",
)
