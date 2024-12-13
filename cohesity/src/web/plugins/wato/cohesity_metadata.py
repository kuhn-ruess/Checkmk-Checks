# 2021 created by Sven Rueß, sritd.de

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Dictionary,
    Tuple,
    Percentage
)
from cmk.gui.plugins.wato import (
    CheckParameterRulespecWithoutItem,
    rulespec_registry,
    RulespecGroupCheckParametersApplications,
)


def _parameter_valuespec_cohesity_metadata():
    return Dictionary(
        elements = [
            ("levels %", Tuple(
                title=_("Maximum percent usage of cluster metadata"),
                help=_("Please configure levels for maximum percent used metadata of cluster."),
                elements=[
                    Percentage(title=_("Warning at")),
                    Percentage(title=_("Critical at")),
                ],
            )),
        ],
    )


rulespec_registry.register(
    CheckParameterRulespecWithoutItem(
        check_group_name="cohesity_metadata",
        group=RulespecGroupCheckParametersApplications,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_cohesity_metadata,
        title=lambda: _("Cohesity metadata usage"),
    )
)

