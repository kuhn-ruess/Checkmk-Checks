#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

import json

def parse_section(string_table):
    data = {}

    for line in string_table:
        if json_raw := line[1].strip():
            data[line[0]] = json.loads(json_raw)

    return data
    
