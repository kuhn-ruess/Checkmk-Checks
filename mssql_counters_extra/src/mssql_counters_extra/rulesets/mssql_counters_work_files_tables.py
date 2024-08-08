#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from cmk.gui.plugins.wato.utils import (
    CheckParameterRulespecWithItem,
    rulespec_registry,
    RulespecGroupCheckParametersApplications,
)
from cmk.gui.valuespec import (
    Dictionary,
    Tuple,
    Float,
    TextInput,
)

def _item_spec_mssql_counters_work_files_tables():
    return TextInput(
        title=_("Instance"),
    )


def _parameter_valuespec_mssql_counters_work_files_tables():
    return Dictionary(
        title="MSSQL Work Files and Tables",
        elements=[
            ("WorkFiles",
                Tuple(
                    title="Work files created per second",
                    elements=[
                        Float(title="Warning at", default_value=100),
                        Float(title="Critical at", default_value=200),
                    ],
                )),
            ("WorkTables",
                Tuple(
                    title="Work tables created per second",
                    elements=[
                        Float(title="Warning at", default_value=200),
                        Float(title="Critical at", default_value=400),
                    ],
                )),
        ],
    )

rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="mssql_counters_work_files_tables",
        group=RulespecGroupCheckParametersApplications,
        item_spec=_item_spec_mssql_counters_work_files_tables,
        parameter_valuespec=_parameter_valuespec_mssql_counters_work_files_tables,
        title=lambda: _("MSSQL Work Files and Tables"),
    )
)
