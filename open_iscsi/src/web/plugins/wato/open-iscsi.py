
group = "agents/" + _("Agent Plugins")
register_rule(group,
    "agent_config:open_iscsi",
    DropdownChoice(
        title = _("Deploy Open-iSCSI  Plugin (Linux)"),
        help = _("The plugin allows monitoring of Open iSCSI Devices"),
        choices = [
            ( {},   _("Deploy plugin") ),
            ( None, _("Do not deploy plugin") ),
        ]
    )
)
