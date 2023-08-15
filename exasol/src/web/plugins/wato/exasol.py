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



group = "datasource_programs"

register_rule(
    group,
    "special_agents:exasol",
    Dictionary(
        elements = [
            ("user", TextAscii(title = _("Username"), allow_empty = False)),
            ("password", Password(title = _("Password"), allow_empty = False)),
        ],
    ),
    title = _("Check EXASOL DB Cluster"),
    help = _("This rule set selects the special agent for EXASOL Cluster"),
    match = "first",
)

def get_free_used_dynamic_valuespec(
    what,
    name,
    default_value=(80.0, 90.0),
    *,
    maxvalue: Union[None, int, float] = 101.0,
):
    if what == "used":
        title = _("used space")
        course = _("above")

    else:
        title = _("free space")
        course = _("below")

    vs_subgroup: List[ValueSpec] = [
        Tuple(
            title=_("Percentage %s") % title,
            elements=[
                Percentage(
                    title=_("Warning if %s") % course,
                    unit="%",
                    minvalue=0.0 if what == "used" else 0.0001,
                    maxvalue=maxvalue,
                ),
                Percentage(
                    title=_("Critical if %s") % course,
                    unit="%",
                    minvalue=0.0 if what == "used" else 0.0001,
                    maxvalue=maxvalue,
                ),
            ],
        ),
        Tuple(
            title=_("Absolute %s") % title,
            elements=[
                Integer(
                    title=_("Warning if %s") % course,
                    unit=_("MB"),
                    minvalue=0 if what == "used" else 1,
                ),
                Integer(
                    title=_("Critical if %s") % course,
                    unit=_("MB"),
                    minvalue=0 if what == "used" else 1,
                ),
            ],
        ),
    ]

    def validate_dynamic_levels(value, varprefix):
        if [v for v in value if v[0] < 0]:
            raise MKUserError(varprefix, _("You need to specify levels of at least 0 bytes."))

    return Alternative(
        title=_("Levels for %s %s") % (name, title),
        show_alternative_title=True,
        default_value=default_value,
        elements=vs_subgroup
        + [
            ListOf(
                Tuple(
                    orientation="horizontal",
                    elements=[
                        Filesize(title=_("%s larger than") % name.title()),
                        Alternative(elements=vs_subgroup),
                    ],
                ),
                title=_("Dynamic levels"),
                allow_empty=False,
                validate=validate_dynamic_levels,
            )
        ],
    )


register_check_parameters(
    subgroup_storage,
    "exasol_dbs",
    _("Exasol db usage"),
    get_free_used_dynamic_valuespec("used", "Space"),
    TextAscii(
        title = _("Database Name"),
        allow_empty = False
    ),
    'first'
)
