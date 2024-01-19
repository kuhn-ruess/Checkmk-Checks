"""
Exasol Monitoring
"""
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
    Tuple,
    Dictionary,
    Password,
    TextInput,
    Filesize,

)

from cmk.gui.plugins.wato.utils.simple_levels import SimpleLevels


from cmk.gui.plugins.wato.datasource_programs import (
    RulespecGroupDatasourceProgramsCustom,
)

from cmk.gui.plugins.wato.utils import (
    CheckParameterRulespecWithItem,
)

from cmk.gui.watolib.rulespec_groups import (
    RulespecGroupEnforcedServicesHardware
)

from cmk.gui.plugins.wato import (
    rulespec_registry,
    HostRulespec,
)

def _valuespec_special_agents_exasol():
    return Dictionary(
        title = _("Exasol via XMLApi"),
        help = _("This rule set selects the special agent for exasol"),
        elements = [
            ("user", TextInput(title = _("Username"), allow_empty = False)),
            ("password", Password(title = _("Password"), allow_empty = False)),
        ],
        optional_keys=[],
    )

rulespec_registry.register(
    HostRulespec(
        group=RulespecGroupDatasourceProgramsCustom,
        name="special_agents:exasol",
        valuespec=_valuespec_special_agents_exasol,
    )
)


def _parameter_valuespec_exasol():
    return Dictionary(
        elements = [
            ("levels", 
                Tuple(
                    title=_("Maximum size of Database"),
                    help=_("Please configure levels for maximum used filesystem size of Database."),
                    elements = [
                        Filesize(title=_("warning at")),
                        Filesize(title=_("critical at")),
                    ]
            )),
        ],
    )

rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="exasol_dbs",
        group=RulespecGroupEnforcedServicesHardware,
        match_type="dict",
        item_spec=lambda: TextInput(title=_("Database Name")),
        parameter_valuespec=_parameter_valuespec_exasol,
        title=lambda: _("Exasol db usage"),
    )
)
