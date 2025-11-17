#!/usr/bin/env python3
"""
This Helper converts an classic cli snmpwalk in the format to use it in checkmk for simulation
"""

import sys


file = sys.argv[1]


with open(file) as f:
    for line in f:
        oid_part, value_part = line.strip().split('=')
        oid = oid_part.strip()
        try:
            content_typ, content = [x.strip() for x in value_part.split(':')]
        except ValueError:
            continue

        if content_typ == "STRING":
            content = content[1:-1]
        print(f"{oid} {content}") 




