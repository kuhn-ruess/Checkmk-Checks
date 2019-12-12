group = "agents/" + _("Agent Plugins")
register_rule(group,
    "agent_config:postgres_replication",
    DropdownChoice(
        title = _("Postgres Replication (Linux)"),
        help = _("The plugin <tt>postgres_replication.sh</tt> allows monitoring of Postgres Replication"),
        choices = [
            ( {},   _("Deploy plugin") ),
            ( None, _("Do not deploy plugin") ),
        ]
    )
)

register_check_parameters(
    subgroup_applications,
    "postgres_replication",
    _("PostgreSQL Replication"),
    Dictionary(
        elements = [
            ( "levels",
                Tuple(
                    title = _("Max Size"),
                    elements = [
                        Filesize(title=_("Warning at")),
                        Filesize(title=_("Critical at")),
                    ]
                ),
            ),
        ],
        optional_keys= False,
    ),
    TextAscii(
        title = _("Slot Name"),
        allow_empty = False
    ),
    'dict'
)
