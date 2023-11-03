from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Dictionary,
    Password,
    TextInput,
)
from cmk.gui.plugins.wato import (
    rulespec_registry,
    HostRulespec,
)
from cmk.gui.plugins.wato.datasource_programs import (
    RulespecGroupDatasourceProgramsCustom,
)

def _valuespec_special_agents_csmon():
    return Dictionary(
        title = _("CSMON System via RestAPI"),
        help = _("This rule set selects the special agent for CSMON Servers"),
        elements = [
            ("username", TextInput(title = _("Username"), allow_empty = False)),
            ("password", Password(title = _("Password"), allow_empty = False)),
        ],
        optional_keys=[],
    )

rulespec_registry.register(
    HostRulespec(
        group=RulespecGroupDatasourceProgramsCustom,
        name="special_agents:csmon",
        valuespec=_valuespec_special_agents_csmon,
    )
)

