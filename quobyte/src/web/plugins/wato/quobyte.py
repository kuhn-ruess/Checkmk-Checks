# 2021 created by Sven Rueß, sritd.de

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
    RulespecGroupDatasourceProgramsHardware,
)


def _valuespec_special_agents_quobyte():
    return Dictionary(
        title = _("Quobyte via WebAPI"),
        help = _("This rule set selects the special agent for Quobyte"),
        elements = [
            ("api_url", TextInput(title = _("API Url"), allow_empty = False)),
            ("username", TextInput(title = _("Username"), allow_empty = False)),
            ("password", Password(title = _("Password"), allow_empty = False)),
        ],
        optional_keys=[],
    )


rulespec_registry.register(
    HostRulespec(
        group=RulespecGroupDatasourceProgramsHardware,
        name="special_agents:quobyte",
        valuespec=_valuespec_special_agents_quobyte,
    )
)

