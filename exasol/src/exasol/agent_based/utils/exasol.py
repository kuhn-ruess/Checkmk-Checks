#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from time import mktime, strptime

from cmk.agent_based.v2 import (
    Service,
)


def parse_exasol_database(string_table):
    databases = {}
    last_db = False
    start = False

    for line in string_table:
        if line[0].startswith('[[['):
            last_db = line[0][3:-3]
            continue

        if last_db:
            databases.setdefault(last_db, {})

            if not line[0].startswith("backup"):
                databases[last_db][line[0]] = line[1]
            else:
                databases[last_db].setdefault('backups', [])
                timestamp = mktime(strptime(line[1] +" "+line[2], "%Y-%m-%d %H:%M"))
                databases[last_db]['backups'].append(timestamp)

    return databases


def discover_exasol_database(section):
    for database in section.keys():
        yield Service(item=database)
