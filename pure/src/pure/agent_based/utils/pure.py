#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

def parse_pure_hardware(string_table):
    section = {}

    for row in string_table:
        (item, status, serial, speed, temp, voltage, slot)  = row

        if serial == "None":
            serial = None

        section[item] = {
            'status': status.lower(),
            'voltage': voltage,
            'slot': slot,
        }
        if temp != "None":
            section[item]['temperature'] = int(temp)

        elif 'ETH' in item:
            # is Network
            section[item]['nw_speed'] = int(speed)

        elif "FAN" in item:
            section[item]['FAN'] = True

        else:
            section[item]['default'] = True

    return section
