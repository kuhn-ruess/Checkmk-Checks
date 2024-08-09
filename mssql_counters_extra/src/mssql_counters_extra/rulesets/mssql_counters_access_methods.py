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
    Percentage,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _parameter_valuespec_mssql_counters_access_methods():
    return Dictionary(
            title = Title("MSSQL index usage"),
        elements = {
            "AccessFullScans": DictElement(
                parameter_form = SimpleLevels(
                    title = Title("Full scans per second"),
                    level_direction = LevelDirection.UPPER,
                    form_spec_template = Float(),
                    prefill_fixed_levels = DefaultValue((50.0, 100.0)),
                )
            ),
            "AccessIndexSearches": DictElement(
                parameter_form = SimpleLevels(
                    title = Title("Index searches per second"),
                    level_direction = LevelDirection.UPPER,
                    form_spec_template = Float(),
                    prefill_fixed_levels = DefaultValue((500.0, 1000.0)),
                )
            ),
            "index_hit_ratio": DictElement(
                parameter_form = SimpleLevels(
                    title = Title("Index hit ratio"),
                    level_direction = LevelDirection.UPPER,
                    form_spec_template = Percentage(),
                    prefill_fixed_levels = DefaultValue((5.0, 1.0)),
                )
            ),
        },
    )


rule_spec_mssql_counters_access_methods = CheckParameters(
    name = "mssql_counters_access_methods",
    topic = Topic.APPLICATIONS,
    condition = HostAndItemCondition(item_title = Title("Instance")),
    parameter_form = _parameter_valuespec_mssql_counters_access_methods,
    title = Title("MSSQL index usage"),
)
