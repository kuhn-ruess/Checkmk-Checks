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
    TimeSpan,
    TimeMagnitude,
    Integer,
    Percentage,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _parameter_valuespec_mssql_counters_memory():
    return Dictionary(
        title = Title("MSSQL memory usage"),
        elements = {
            "LazyWrites": DictElement(
                parameter_form = SimpleLevels(
                    title = Title("Lazy writes per second"),
                    level_direction = LevelDirection.UPPER,
                    form_spec_template = Float(),
                    prefill_fixed_levels = DefaultValue((20.0, 50.0)),
                ),
            ),
            "page_life_expectancy": DictElement(
                parameter_form = SimpleLevels(
                    title = Title("Page life expectancy"),
                    level_direction = LevelDirection.LOWER,
                    form_spec_template = TimeSpan(
                        displayed_magnitudes = [TimeMagnitude.SECOND, TimeMagnitude.MINUTE, TimeMagnitude.HOUR],
                    ),
                    prefill_fixed_levels = DefaultValue((300, 120)),
                ),
            ),
            "MemoryGrantsPending": DictElement(
                parameter_form = SimpleLevels(
                    title = Title("Memory grants pending"),
                    level_direction = LevelDirection.UPPER,
                    form_spec_template = Integer(),
                    prefill_fixed_levels = DefaultValue((3, 10)),
                ),
            ),
            "MemoryUsage": DictElement(
                parameter_form = SimpleLevels(
                    title = Title("Memory usage"),
                    level_direction = LevelDirection.UPPER,
                    form_spec_template = Percentage(),
                    prefill_fixed_levels = DefaultValue((80, 90))
                ),
            ),
        },
    )


rule_spec_mssql_counters_memory = CheckParameters(
    name = "mssql_counters_memory",
    topic = Topic.APPLICATIONS,
    condition = HostAndItemCondition(item_title = Title("Instance")),
    parameter_form = _parameter_valuespec_mssql_counters_memory,
    title = Title("MSSQL memory usage"),
)
