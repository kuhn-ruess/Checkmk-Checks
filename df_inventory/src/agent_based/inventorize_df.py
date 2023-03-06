#!/usr/bin/env python3
#<<<inventorize_df:sep(59)>>>
#/;root;Michael Maier;uxos@firma.at
#/monitoring;root;Michael Maier;uxos@firma.at
#/opt/oracli;oracli;Daniel Duesentrieb;daniel.duesentriep@firma.at


from .agent_based_api.v1 import (
    register,
    TableRow,
)

def inventory_df(section):
    """
    Return Inventory Information
    """
    for line in section:
        yield TableRow(
            path=['filesystems', 'owners'],
            key_columns={
                "Filesystem": line[0],
            },
            inventory_columns={
                "Owner Name": line[2],
                "Owner E-Mail": line[3],
            }
        )

register.agent_section(
    name="inventorize_df",
)

register.inventory_plugin(
    name="inventorize_df",
    inventory_function=inventory_df,
)
