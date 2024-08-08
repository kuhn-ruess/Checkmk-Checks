#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from cmk.gui.plugins.wato.utils import (
    CheckParameterRulespecWithItem,
    rulespec_registry,
    RulespecGroupCheckParametersApplications,
)
from cmk.gui.valuespec import (
    TextInput,
    Dictionary,
    Tuple,
    Float,
    Integer,
)

def _item_spec_mssql_counters_connections():
    return TextInput(
        title=_("Instance"),
    )

def _parameter_valuespec_mssql_counters_connections():
    return Dictionary(
        title="MSSQL Connections",
        elements=[
            ("user_connections",
                Tuple(
                    title="User connections",
                    elements=[
                        Integer(title="Warning at", default_value=100),
                        Integer(title="Critical at", default_value=200),
                    ],
                )),
            ("LogInConnects",
                Tuple(
                    title="Logins per second",
                    elements=[
                        Float(title="Warning at", default_value=2),
                        Float(title="Critical at", default_value=10),
                    ],
                )),
            ("LogOutConnects",
                Tuple(
                    title="Logouts per second",
                    elements=[
                        Float(title="Warning at", default_value=2),
                        Float(title="Critical at", default_value=10),
                    ],
                )),
        ],
    )

rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="mssql_counters_connections",
        group=RulespecGroupCheckParametersApplications,
        item_spec=_item_spec_mssql_counters_connections,
        parameter_valuespec=_parameter_valuespec_mssql_counters_connections,
        title=lambda: _("MSSQL Connections"),
    )
)
