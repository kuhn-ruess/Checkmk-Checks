#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import (
    Dictionary,
    DictElement,
    SimpleLevels,
    LevelDirection,
    DefaultValue,
    Float,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _parameter_valuespec_mssql_counters_work_files_tables():
    return Dictionary(
        title = Title("MSSQL work files and tables"),
        elements = {
            "WorkFiles": DictElement(
                parameter_form = SimpleLevels(
                    title = Title("Work files created per second"),
                    level_direction = LevelDirection.UPPER,
                    form_spec_template = Float(),
                    prefill_fixed_levels = DefaultValue((100.0, 200.0)),
                ),
            ),
            "WorkTables": DictElement(
                parameter_form = SimpleLevels(
                    title = Title("Work tables created per second"),
                    level_direction = LevelDirection.UPPER,
                    form_spec_template = Float(),
                    prefill_fixed_levels = DefaultValue((200.0, 400,0)),
                ),
            ),
        },
    )


rule_spec_mssql_counters_work_files_tables = CheckParameters(
    name = "mssql_counters_work_files_tables",
    topic = Topic.APPLICATIONS,
    condition = HostAndItemCondition(item_title = Title("Instance")),
    parameter_form = _parameter_valuespec_mssql_counters_work_files_tables,
    title = Title("MSSQL work files and tables"),
)
