# 2021 created by Sven Rueß, sritd.de

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Dictionary,
    Password,
    TextAscii,
)
from cmk.gui.plugins.wato import (
    rulespec_registry,
    HostRulespec,
)
from cmk.gui.plugins.wato.datasource_programs import (
    RulespecGroupDatasourceProgramsHardware,
)


def _valuespec_special_agents_cohesity():
    return Dictionary(
        title = _("Cohesity via WebAPI"),
        help = _("This rule set selects the special agent for Cohesity"),
        elements = [
            ("user", TextAscii(title = _("Username"), allow_empty = False)),
            ("password", Password(title = _("Password"), allow_empty = False)),
            ("domain", TextAscii(title = _("Domain"), default_value = "LOCAL", allow_empty = False)),
        ],
        optional_keys=[],
    )


rulespec_registry.register(
    HostRulespec(
        group=RulespecGroupDatasourceProgramsHardware,
        name="special_agents:cohesity",
        valuespec=_valuespec_special_agents_cohesity,
    )
)

