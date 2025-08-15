#!/usr/bin/env python3
"""
DF Inventory Plugin for CheckMK
Provides filesystem ownership information for inventory
"""

from collections.abc import Mapping
from typing import Any

from cmk.agent_based.v2 import (
    AgentSection,
    InventoryPlugin,
    InventoryResult,
    StringTable,
    TableRow,
)


def parse_inventorize_df(string_table: StringTable) -> StringTable:
    """
    Parse the inventorize_df section data
    Expected format: filesystem;owner;owner_name;owner_email
    """
    return string_table


def inventory_inventorize_df(section: StringTable) -> InventoryResult:
    """
    Return Inventory Information for filesystem ownership
    """
    for line in section:
        if len(line) >= 4:
            yield TableRow(
                path=["software", "applications", "filesystem_owners"],
                key_columns={
                    "filesystem": line[0],
                },
                inventory_columns={
                    "owner": line[1],
                    "owner_name": line[2],
                    "owner_email": line[3],
                },
            )


agent_section_inventorize_df = AgentSection(
    name="inventorize_df",
    parse_function=parse_inventorize_df,
)

inventory_plugin_inventorize_df = InventoryPlugin(
    name="inventorize_df",
    inventory_function=inventory_inventorize_df,
)
