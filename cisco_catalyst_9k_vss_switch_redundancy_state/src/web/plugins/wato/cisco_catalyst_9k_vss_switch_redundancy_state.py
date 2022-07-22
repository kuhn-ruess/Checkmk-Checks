#!/usr/bin/env python3

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Dictionary,
    DropdownChoice,
)

from cmk.gui.plugins.wato import (
    CheckParameterRulespecWithItem,
    rulespec_registry,
    RulespecGroupCheckParametersNetworking,
)


def _parameter_valuespec_catalyst_switch_state():
    return Dictionary(
            elements=[
                ("switch_role",
                    DropdownChoice(
                        title=_("Expected switch role"),
                        choices=[
                            ("1", "master"),
                            ("2", "member"),
                            ("3", "not member"),
                            ("4", "standby"),
                        ],
                    )
                ),
            ],
        )

rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="cisco_catalyst_9k_vss_switch_redundancy_state",
        group=RulespecGroupCheckParametersNetworking,
        item_spec=lambda: TextAscii(title=_("Switch number")),
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_catalyst_switch_state,
        title=lambda: _("Cisco Catalyst 9k redundancy State"),
    )
)
