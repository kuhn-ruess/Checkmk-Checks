register_check_parameters(
    _("Operating System Resources"),
    "as400_cpu",
    _("AS/400 CPU Usage Levels"),
    Dictionary(
        title = _("CPU Parameters"),
        optional_keys = ["average"],
        elements = [
            ( "levels",
                Tuple (
                    title = _("Levels for cpu usage (%)"),
                    elements = [
                        Percentage(
                            title = _("Warning at:" ),
                            maxvalue = 1500.0,
                            unit = "percentage"
                        ),
                        Percentage(
                            title = _("Critical at:"),
                            maxvalue = 1500.0,
                            unit = "percentage"
                        ),
                    ]
                )
            ),
            ( "average",
                Integer(
                    title = _("Averaging on:"),
                    label = _("Averaging on"),
                    maxvalue = 144,
                    unit = "minutes",
                    default_value = 15
                )
            )
        ]
    ),
    None,"dict"
)

register_check_parameters(
    _("Operating System Resources"),
    "as400_jobs",
    _("AS/400 Job queue counters"),
    Dictionary(
        elements = [
            ("jobs_levels",
                Tuple(
                    title = _("Levels for Jobs"),
                    label = _("Levels for Jobs"),
                    elements = [
                        Integer(title = _("Warning at:" ), maxvalue = 1000000),
                        Integer(title = _("Critical at:"), maxvalue = 1000000),
                    ]
                )
            )
        ]
    ),
    None,"dict"
)

register_check_parameters(
    _("Operating System Resources"),
    "as400_users",
    _("AS/400 logged in users"),
    Dictionary(
        elements = [
            ("users_levels",
                Tuple(
                    title = _("Levels for Users"),
                    label = _("Levels for Users"),
                    elements = [
                        Integer(title = _("Warning at:" ), maxvalue = 1000000),
                        Integer(title = _("Critical at:"), maxvalue = 1000000),
                    ]
                )
            )
        ]
    ),
    None,"dict"
)

register_check_parameters(
    _("Operating System Resources"),
    "as400_tcp_connections",
    _("AS/400 logged in tcp_connections"),
    Dictionary(
        elements = [
            ("tcp_connections_levels",
                Tuple(
                    title = _("Levels for tcp_connections"),
                    label = _("Levels for tcp_connections"),
                    elements = [
                        Integer(title = _("Warning at:" ), maxvalue = 100000000),
                        Integer(title = _("Critical at:"), maxvalue = 100000000),
                    ]
                )
            )
        ]
    ),
    None,"dict"
)
