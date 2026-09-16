#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.agent_based.v2 import (
    Attributes,
    InventoryPlugin,
    TableRow,
)


def inventory_aruba_ap(section):
    """Inventory of the access point hardware, firmware and radios."""
    yield Attributes(
        path=["hardware", "system"],
        inventory_attributes={
            key: str(value)
            for key, value in (
                ("model", section.get("model")),
                ("serial", section.get("serial")),
                ("mac_address", section.get("mac")),
            )
            if value
        },
    )

    yield Attributes(
        path=["software", "os"],
        inventory_attributes={
            key: str(value)
            for key, value in (
                ("version", section.get("version")),
                ("vendor", "Aruba"),
            )
            if value
        },
    )

    yield Attributes(
        path=["software", "applications", "aruba", "central"],
        inventory_attributes={
            key: str(value)
            for key, value in (
                ("name", section.get("name")),
                ("group", section.get("group")),
                ("site", section.get("site")),
                ("mode", section.get("mode")),
                ("ip_address", section.get("ip")),
            )
            if value
        },
    )

    for name, radio in section.get("radios", {}).items():
        yield TableRow(
            path=["hardware", "networking", "wlan", "radios"],
            key_columns={"name": name},
            inventory_columns={
                "mac_address": str(radio.get("macaddr", "")),
                "type": str(radio.get("radio_type", "")),
                "channel": str(radio.get("channel", "")),
                "spatial_stream": str(radio.get("spatial_stream", "")),
            },
            status_columns={
                "status": str(radio.get("status", "")),
            },
        )


inventory_plugin_aruba_ap = InventoryPlugin(
    name = "aruba_ap",
    sections = ["aruba_ap"],
    inventory_function = inventory_aruba_ap,
)
