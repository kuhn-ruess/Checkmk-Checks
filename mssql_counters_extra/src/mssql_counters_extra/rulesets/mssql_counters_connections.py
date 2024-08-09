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
    Integer,
    Float,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _parameter_valuespec_mssql_counters_connections():
    return Dictionary(
        title = Title("MSSQL user connections"),
        elements = {
            "user_connections": DictElement(
                parameter_form = SimpleLevels(
                    title = Title("User connections"),
                    level_direction = LevelDirection.UPPER,
                    form_spec_template = Integer(),
                    prefill_fixed_levels = DefaultValue((100, 200)),
                )
            ),
            "LogInConnects": DictElement(
                parameter_form = SimpleLevels(
                    title = Title("Logins per second"),
                    level_direction = LevelDirection.UPPER,
                    form_spec_template = Float(),
                    prefill_fixed_levels = DefaultValue((2.0, 10.0)),
                ),
            ),
            "LogOutConnects": DictElement(
                parameter_form = SimpleLevels(
                    title = Title("Logouts per second"),
                    level_direction = LevelDirection.UPPER,
                    form_spec_template = Float(),
                    prefill_fixed_levels = DefaultValue((2.0, 10.0)),
                ),
            ),
        },
    )


rule_spec_mssql_counters_connections = CheckParameters(
    name = "mssql_counters_connections",
    topic = Topic.APPLICATIONS,
    condition = HostAndItemCondition(item_title = Title("Instance")),
    parameter_form = _parameter_valuespec_mssql_counters_connections,
    title = Title("MSSQL user connections"),
)
