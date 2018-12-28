register_check_parameters(
    subgroup_environment,
    "tridium",
    _("Tridium Device"),
    Dictionary(
        elements = [
            ( "levels",
                Levels(
                    title = _("Check Levels"),
                    unit = _("Units"),
                    default_difference = (5, 8),
                    default_value = None,
                ),
            ),
            ( "allowed_strings",
                ListOfStrings(
                    title = _("Allow the following Strings in State"),
                    orientation = "horizontal"
                    )
            ),
            ( "use_discovery",
              Checkbox(
                  title = _("Monitor Discovery State"),
                  label = _("Check for State at time of discovery"),
                  help = "This overwrites the Allow the following String in State rule",
                ),
            ),
            ( "forced_strings",
                ListOfStrings(
                    title = _("Force Alarm on following States"),
                    help = "Makes only sense in compination with Monitor Discovery State",
                    orientation = "horizontal"
                    )
            ),
        ]
    ),
    TextAscii(
        title = _("Sensor Name"),
        allow_empty = False
    ),
    'dict'
)

register_check_parameters(
    subgroup_environment,
    "tridium_special",
    _("Tridium Special"),
    Dictionary(
        elements = [
            ( "rule",
                Dictionary(
                    title= _("Use Rulebased State"),
                    optional_keys = [],
                    elements = [
                        ('if_state', TextAscii(title="This state is allowed")),
                        ('if_field', TextAscii(title="If this Field")),
                        ('if_field_state', TextAscii(title="has this state")),
                        ('else_state', TextAscii(title="Otherwiese require this state")),
                    ]
                ),
            ),
            ( "states",
              ListOfStrings(
                  title = _("Allow the following Strings in State"),
                  orientation = "horizontal"
              )
            ),
        ],
    ),
    TextAscii(
        title = _("Sensor Name"),
        allow_empty = False
    ),
    'dict'
)

register_check_parameters(
    subgroup_environment,
    "tridium_fuel",
    _("Tridium Fuel"),
    Levels(
        title = _("Check Levels"),
        unit = _("Ltr"),
        default_difference = (5, 8),
        default_value = None,
    ),
    None,
    'first'
)
