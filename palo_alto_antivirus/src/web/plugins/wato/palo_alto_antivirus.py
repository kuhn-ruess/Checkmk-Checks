from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Dictionary,
    Tuple,
    Age,
)
from cmk.gui.plugins.wato import (
    CheckParameterRulespecWithoutItem,
    rulespec_registry,
    RulespecGroupCheckParametersApplications,
)

def _parameter_valuespec_palo_alto_antivirus():
    return Dictionary(
        elements = [
            ("age", Tuple(
                title=_("Age for antivirus updates"),
                help=_("Please configure levels for maximum age of last antivirus update."),
                elements=[
                    Age(title=_("Warning if older than"), display=["days", "hours"], default_value=86400),
                    Age(title=_("Critical if older than"), display=["days", "hours"], default_value=104400),
                ],
            )),
        ],
        optional_keys=[],
    )

rulespec_registry.register(
    CheckParameterRulespecWithoutItem(
        check_group_name="palo_alto_antivirus",
        group=RulespecGroupCheckParametersApplications,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_palo_alto_antivirus,
        title=lambda: _("Palo Alto AntiVirus Age"),
    )
)
