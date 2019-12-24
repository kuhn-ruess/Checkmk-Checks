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
        ],
    ),
    None,
    'dict'
)
