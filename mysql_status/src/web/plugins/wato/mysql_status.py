#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
"""
Web configuration for mysql.status checks
"""
# pylint: disable=undefined-variable
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
from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Dictionary,
    TextAscii,
    DropdownChoice,
)
from cmk.gui.wato import (
    subgroup_applications,
)
from cmk.gui.plugins.wato.utils import (
    register_check_parameters,
    Levels,
)


register_check_parameters(
    subgroup_applications,
    "mysql_status",
    _("Settings for Mysql Status check"),
    Dictionary(
        elements=[
            ("levels", Levels(
                title=_("Rate/ Unit Levels"),
                default_difference=(5, 8),
                default_value=None,
            )),
            ("target_state", DropdownChoice(
                title=_("Target State"),
                choices=[
                    ("ON", "ON is OK"),
                    ("OFF", "OFF is OK"),
                ]
            )),
        ]),
    TextAscii(
        title=_("Variable Name"),
        allow_empty=True
    ),
    'dict'
)
