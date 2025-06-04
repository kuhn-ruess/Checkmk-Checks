#!/usr/bin/env python3
"""
Inventory Plugin for complet automatic parsing of all Sina Workstation Data

2022-08-23 Inital Version (Bastian Kuhn, mail@bastian-kuhn.de)
2025-05-23 Updates for Checkmk 2.3/2.4 (Bastian Kuhn, bastian.kuhn@kuhn-ruess.de)

"""
import json, time

from cmk.agent_based.v2 import Attributes, TableRow, InventoryPlugin, AgentSection


def create_inventory(path, attribute, value):
    """
    """
    if type(value) == list:
        path.append(attribute)
        for idx, sub_object in enumerate(value):
            if not sub_object:
                continue
            yield TableRow(
                path=path,
                key_columns={'object_id': f"{attribute}-{idx}"},
                inventory_columns=sub_object,
            )
        return
    if type(value) == dict:
        path.append(attribute)
        yield Attributes(
                path=path,
                inventory_attributes=value,
        )
        return
    yield Attributes(
            path=path,
            inventory_attributes={attribute: value},
    )
    return



def parse_sina_ws(string_table):
    """
    Parse Agent Json into dict
    """
    return json.loads(string_table[0][0])

def read_timeold(timestamp):
    return time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(timestamp/1000.0))

def inventory_sina(section):
    """"
    Fill Inventory Table
    """

    yield Attributes(
            path=['software', 'os'],
            inventory_attributes={
                "type": "SINA OS",
                "vendor": "secunet",
                "name": "SINA OS",
                "version": section["hwinfo"]["sinaVersion"].split("-")[0]\
                    .replace(" ", "").replace("000", ""),
            })

    yield Attributes(
            path=['hardware', 'system'],
            inventory_attributes={
                "manufacturer": section["hwinfo"]["systemVendor"],
                "uuid": section["hwinfo"]["systemUuid"],
                "serial": section["hwinfo"]["systemSerial"],
                "model": section["hwinfo"]["systemVersion"],
            })

    yield Attributes(
            path=['hardware', 'bios'],
            inventory_attributes={
                "version": section["hwinfo"]["biosVersion"]
            })

    yield Attributes(
            path=['sina'],
            inventory_attributes={
                "dialin": read_timeold(section["timestamp"])
            })

    # Dynamic Collectors
    
    ## hwinfo and hardware
    hwinfo_excludes = ['systemVendor', 'systemUuid', 'systemSerial', 
                       'systemVersion', 'biosVersion']
    node_hw = {}
    sub_node_hw = {}

    # hwinfo: Collect all items which not in excludelist
    for key, value in section['hwinfo'].items():
        if key not in hwinfo_excludes:
            yield from create_inventory(['sina', 'workstation'], key, value)

    # hardware: Collect all items which not in include list
    for key, value in section.get('hardware', {}).items():
        yield from create_inventory(['sina', 'workstation'], key, value)

    ## User (sina Token)
    for user in section['users']:
        username = user['user'].split('@')[0]
        for key, value in user.items():
            if key != 'user':
                yield from create_inventory(['sina', 'token', username], key, value)

agent_section_sina_ws = AgentSection(
    name="sina_ws",
    parse_function=parse_sina_ws,
)

inventory_plugin_sina = InventoryPlugin(
    name="sina_ws",
    inventory_function = inventory_sina
)
