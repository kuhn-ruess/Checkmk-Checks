#!/usr/bin/env python3

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Dictionary,
    DropdownChoice,
)

from cmk.gui.plugins.wato import (
    CheckParameterRulespecWithoutItem,
    rulespec_registry,
    RulespecGroupCheckParametersNetworking,
)


def _parameter_valuespec_cisco_vpc_role():
    return Dictionary(
            elements=[
                ("switch_role",
                    DropdownChoice(
                        title=_("Expected switch role"),
                        choices=[
                            ("1", "primary, and operational secondary"),   # primarySecondary(1),
                            ("2", "primary, and operational primary"),     # primary(2),
                            ("3", "secondary, and operational primary"),   # secondaryPrimary(3),
                            ("4", "secondary, and operational secondary"), # secondary(4),
                            ("5", "no peer device"),                       # noneEstablished(5),
                        ],
                    )
                ),
            ],
        )

rulespec_registry.register(
    CheckParameterRulespecWithoutItem(
        check_group_name="cisco_vpc_role",
        group=RulespecGroupCheckParametersNetworking,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_cisco_vpc_role,
        title=lambda: _("Cisco VPC Role"),
    )
)
