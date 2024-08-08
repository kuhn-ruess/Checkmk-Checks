#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from cmk.gui.plugins.wato.utils import (
    CheckParameterRulespecWithItem,
    rulespec_registry,
    RulespecGroupCheckParametersApplications,
)
from cmk.gui.valuespec import (
    Age,
    Dictionary,
    Tuple,
    Integer,
    Float,
    Percentage,
    TextInput,
)

def _item_spec_mssql_counters_memory():
    return TextInput(
        title=_("Instance"),
    )


def _parameter_valuespec_mssql_counters_memory():
    return Dictionary(
        title="MSSQL Memory Usage",
        elements=[
            ("LazyWrites",
                Tuple(
                    title="Lazy writes per second",
                    elements=[
                        Float(title="Warning at", default_value=20),
                        Float(title="Critical at", default_value=50),
                    ],
                )),
            ("page_life_expectancy",
                Tuple(
                    title="Page life expectancy",
                    elements=[
                        Age(title="Warning below", default_value=300),
                        Age(title="Critical below", default_value=120),
                    ],
                )),
            ("MemoryGrantsPending",
                Tuple(
                    title="Memory grants pending",
                    elements=[
                        Integer(title="Warning at", default_value=3),
                        Integer(title="Critical at", default_value=10),
                    ],
                )),
            ("MemoryUsage",
                Tuple(
                    title="Memory usage",
                    elements=[
                        Percentage(title="Warning at", default_value=80),
                        Percentage(title="Critical at", default_value=90),
                    ],
                )),
        ],
    )

rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="mssql_counters_memory",
        group=RulespecGroupCheckParametersApplications,
        item_spec=_item_spec_mssql_counters_memory,
        parameter_valuespec=_parameter_valuespec_mssql_counters_memory,
        title=lambda: _("MSSQL Memory Usage"),
    )
)
