# 2021 created by Sven Rueß, sritd.de

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Dictionary,
    Tuple,
    Filesize,
    Percentage,
)
from cmk.gui.plugins.wato import (
    CheckParameterRulespecWithoutItem,
    rulespec_registry,
    RulespecGroupCheckParametersApplications,
)


def _parameter_valuespec_cohesity_storage():
    return Dictionary(
        elements = [
            ("levels", Tuple(
                title=_("Maximum size of cluster filesystem"),
                help=_("Please configure levels for maximum used filesystem size of cluster."),
                elements=[
                    Filesize(title=_("Warning at")),
                    Filesize(title=_("Critical at")),
                ],
            )),
            ("levels %", Tuple(
                title=_("Maximum percent size of cluster filesystem"),
                help=_("Please configure levels for maximum percent used filesystem size of cluster."),
                elements=[
                    Percentage(title=_("Warning at")),
                    Percentage(title=_("Critical at")),
                ],
            )),
        ],
    )


rulespec_registry.register(
    CheckParameterRulespecWithoutItem(
        check_group_name="cohesity_storage",
        group=RulespecGroupCheckParametersApplications,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_cohesity_storage,
        title=lambda: _("Cohesity filesystem size"),
    )
)

