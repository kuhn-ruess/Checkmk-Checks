# 2021 created by Sven Rueß, sritd.de

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Dictionary,
    ListOfStrings,
    TextAscii,
    TextUnicode,
)
from cmk.gui.plugins.wato import (
    CheckParameterRulespecWithItem,
    rulespec_registry,
    RulespecGroupCheckParametersApplications,
)


def _item_cohesity_node_status():
    return TextAscii(
        title=_("Node"),
        help=_("Name of node"),
    )


def _parameter_valuespec_cohesity_node_status():
    return Dictionary(
        elements = [
            ('services', ListOfStrings(
                title=_("Services to ignore"),
                help=_("Specify all services to ignore"),
                valuespec=TextUnicode(),
                )
            ),
        ],
    )


rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="cohesity_node_status",
        group=RulespecGroupCheckParametersApplications,
        match_type="dict",
        item_spec=_item_cohesity_node_status,
        parameter_valuespec=_parameter_valuespec_cohesity_node_status,
        title=lambda: _("Cohesity node status ignored services"),
    )
)

