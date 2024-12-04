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
# | Copyright Bastian Kuhn 2011                mail@bastian-kuhn.de | 
# +-----------------------------------------------------------------+
#
# This file is for check_mk
# Information about me can be found at http://bastian-kuhn.de
# Information about check_mk at http://mathias-kettner.de/check_mk.
#
# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

# Perf-O-Meter for mysql_status

# issue #24
try:
    from cmk.gui.plugins.views.perfometers.utils import (
        perfometers,
        perfometer_logarithmic,
    )
except:
    from cmk.gui.views.perfometer.legacy_perfometers.utils import (
        perfometers,
        perfometer_logarithmic,
    )


def perfometer_mysql_status(row, check_command, perf_data):
    color = { 0: "#a4f", 1: "#ff2", 2: "#f22", 3: "#fa2" }[row["service_state"]]
    try:
        value = perf_data[0].value
    except AttributeError:
        value = perf_data[0][1]
    return "%d" % int(value), perfometer_logarithmic(value, 400, 2, color)

perfometers['check_mk-mysql_status'] = perfometer_mysql_status
