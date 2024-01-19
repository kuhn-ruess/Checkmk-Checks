#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
# +-----------------------------------------------------------------+
# |                                                                 |
# |        (  ___ \     | \    /\|\     /||\     /|( (    /|        |
# |        | (   ) )    |  \  / /| )   ( || )   ( ||  \  ( |        |
# |        | (__/ /     |  (_/ / | |   | || (___) ||   \ | |        |
# |        |  __ (      |   _ (  | |   | ||  ___  || (\ \) |        |
# |        | (  \ \     |  ( \ \ | |   | || (   ) || | \   |        |
# |        | )___) )_   |  /  \ \| (___) || )   ( || )  \  |        |
# |        |/ \___/(_)  |_/    \/(_______)|/     \||/    )_)        |
# |                                                                 |
# | Copyright Bastian Kuhn 2018                mail@bastian-kuhn.de |
# +-----------------------------------------------------------------+
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.


def parse_exasol_database(info):
    databases = {}
    last_db = False
    start = False
    for line in info:
        if line[0].startswith('[[['):
            last_db = line[0][3:-3]
            continue

        if last_db:
            databases.setdefault(last_db, {})
            if not line[0].startswith("backup"):
                databases[last_db][line[0]] = line[1]
            else:
                databases[last_db].setdefault('backups', [])
                timestamp = time.mktime(time.strptime(line[1] +" "+line[2], "%Y-%m-%d %H:%M"))
                databases[last_db]['backups'].append(timestamp)
    return databases


def inventory_exasol_database(parsed):
    for database in parsed.keys():
        yield database, {}

def check_exasol_database(item, params, parsed):
    data = parsed.get(item)
    if data:
        usage = float(data['usage']) * 1024 * 1024 * 1024
        free = float(data['free']) * 1024 * 1024 * 1024
        total = free + usage
        perc_used = round((usage/total) * 100.0, 2)
        usage = int(usage)
        total = int(total)
        state = 0
        warn, crit = None, None
        if params:
            warn, crit = params['levels']
            if type(warn) == float:
                # percent levels
                if perc_used >= crit:
                    state = 2
                elif perc_used >= warn:
                    state = 1
            else:
                # absolute levels
                # levels to gb
                warn = warn
                crit = crit
                if usage >= crit:
                    state = 2
                elif usage >= warn:
                    state = 1

        perfdata = [('bytes', int(usage), warn, crit, 0, int(total))]
        usage_read = get_bytes_human_readable(usage)
        total_read = get_bytes_human_readable(total)
        return state, "Usage: %s of %s (%s %%)" % (usage_read, total_read, perc_used), perfdata


check_info["exasol_database"] = {
    'group' : "exasol_dbs",
    'check_function': check_exasol_database,
    'inventory_function': inventory_exasol_database,
    'service_description': "Database %s Usage",
    'parse_function' : parse_exasol_database,
    'has_perfdata' : True,
}


def inventory_exasol_database_backup(parsed):
    for database in parsed.keys():
        yield database, {}

def check_exasol_database_backup(item, _no_params, parsed):
    data = parsed.get(item)
    if data:
        for last_id, backup in enumerate(data['backups'][1:]):
            if data['backups'][last_id] < backup:
                return 1, "Remote Base Backup expires before its dependency"
        if data['backups']:
            return 0, "Valid Backup found"
        return 2, "No valid Backup found"


check_info["exasol_database.backup"] = {
    'check_function': check_exasol_database_backup,
    'inventory_function': inventory_exasol_database_backup,
    'service_description': "Database %s Backups",
    'parse_function' : parse_exasol_database,

}
