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
# | Copyright Bastian Kuhn 2020                mail@bastian-kuhn.de |
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
    "agent_config:puppet_agent",
    DropdownChoice(
        title = _("Deploy puppet agent Monitoring (Linux, Windows)"),
        help = _("The plugin allows monitoring of Puppet Agent Status for Windows and Linux"),
        choices = [
            ( {},   _("Deploy plugin") ),
            ( None, _("Do not deploy plugin") ),
        ]
    )
)

register_check_parameters(
    subgroup_applications,
    "puppet_agent",
    _("Puppet Agent"),
    Dictionary(
        elements = [
            ( "last_run",
                Tuple(
                    title = _("Time since last run"),
                    elements = [
                        Age(title=_("Warning at")),
                        Age(title=_("Critical at")),
                    ]
                ),
            ),
            ( "events_failure",
                Levels(
                    title = _("Event Failures"),
                    default_value = (10, 15),
                ),
            ),
            ( "resources_changed",
                Levels(
                    title = _("Resources Changed"),
                    default_value = (10, 15),
                ),
            ),
            ( "resources_failed",
                Levels(
                    title = _("Resources Failed"),
                    default_value = (10, 15),
                ),
            ),
            ( "resources_failed_to_restart",
                Levels(
                    title = _("Resources Failed to restart"),
                    default_value = (10, 15),
                ),
            ),
            ( "resources_out_of_sync",
                Levels(
                    title = _("Resources out of Sync"),
                    default_value = (10, 15),
                ),
            ),
            ( "resources_restarted",
                Levels(
                    title = _("Resources Restarted"),
                    default_value = (10, 15),
                ),
            ),
            ( "resources_scheduled",
                Levels(
                    title = _("Resources Scheduled"),
                    default_value = (10, 15),
                ),
            ),
            ( "resources_skipped",
                Levels(
                    title = _("Resources Skipped"),
                    default_value = (10, 15),
                ),
            ),
        ],
    ),
    None,
    'dict'
)
