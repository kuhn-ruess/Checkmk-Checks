#!/usr/bin/env python
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

group = "agents/" + _("Agent Plugins")
register_rule(group,
    "agent_config:qemu",
    DropdownChoice(
        title = _("QEMU/ KVM Monitoring (Linux)"),
        help = _("The plugin <tt>qemu</tt> allows monitoring of KVM and QEMU Virtual Machines."),
        choices = [
            ( {},   _("Deploy plugin") ),
            ( None, _("Do not deploy plugin") ),
        ]
    )
)

register_check_parameters(
    subgroup_applications,
    "qemu",
    _("Qemu/ KVM Check"),
    Dictionary(
        elements = [
            ( "cpu",
                Levels(
                    title = _("CPU Usage"),
                    unit = _("Percent"),
                    default_difference = (5, 8),
                    default_value = None,
                ),
            ),
            ( "mem",
                Levels(
                    title = _("Memory Usage"),
                    unit = _("Percent"),
                    default_difference = (5, 8),
                    default_value = None,
                ),
            ),
        ]
    ),
    TextAscii(
        title = _("VM Name"),
        allow_empty = False
    ),
    'dict'
)
