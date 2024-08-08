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
    Percentage,
)

def _item_spec_mssql_counters_access_methods():
    return TextInput(
        title=_("Instance"),
    )


def _parameter_valuespec_mssql_counters_access_methods():
    return Dictionary(
        title="MSSQL Index Usage",
        elements=[
            ("AccessFullScans",
                Tuple(
                    title="Full scans per second",
                    elements=[
                        Float(title="Warning at", default_value=50),
                        Float(title="Critical at", default_value=100),
                    ],
                )),
            ("AccessIndexSearches",
                Tuple(
                    title="Index searches per second",
                    elements=[
                        Float(title="Warning at", default_value=500),
                        Float(title="Critical at", default_value=1000),
                    ],
                )),
            ("index_hit_ratio",
                Tuple(
                    title="Index hit ratio",
                    elements=[
                        Percentage(title="Warning below", default_value=5),
                        Percentage(title="Critical below", default_value=1),
                    ],
                )),
        ],
    )


rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="mssql_counters_access_methods",
        group=RulespecGroupCheckParametersApplications,
        item_spec=_item_spec_mssql_counters_access_methods,
        parameter_valuespec=_parameter_valuespec_mssql_counters_access_methods,
        title=lambda: _("MSSQL Index Usage"),
    )
)
