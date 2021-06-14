group = "datasource_programs"

register_rule(
    group,
    "special_agents:cohesity",
    Dictionary(
        elements = [
            ("user", TextAscii(title = _("Username"), allow_empty = False)),
            ("password", Password(title = _("Password"), allow_empty = False)),
        ],
    ),
    title = _("Check a Cohesity System"),
    help = _("This rule set selects the special agent for Cohesity"),
    match = "first",
)
