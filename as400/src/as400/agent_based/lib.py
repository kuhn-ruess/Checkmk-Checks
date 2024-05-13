#!/usr/bin/env python3

from cmk.agent_based.v2 import startswith

DETECT_AS400 = startswith(".1.3.6.1.2.1.1.1.0", "IBM OS/400")

def parse_as400(string_table):
    """ Parse Function """
    return int(string_table[0][0])
