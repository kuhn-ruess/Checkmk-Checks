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


def _parameter_valuespec_mssql_counters_latches():
    return Dictionary(
        title = Title("MSSQL latches"),
        elements = {
            "LatchWaits": DictElement(
                parameter_form = SimpleLevels(
                    title = Title("Latch waits per second"),
                    level_direction = LevelDirection.UPPER,
                    form_spec_template = Float(),
                    prefill_fixed_levels = DefaultValue((100.0, 200.0)),
                ),
            ),
            "LatchWaitTime": DictElement(
                parameter_form = SimpleLevels(
                    title = Title("Total latch wait time (ms)"),
                    level_direction = LevelDirection.UPPER,
                    form_spec_template = Float(),
                    prefill_fixed_levels = DefaultValue((200.0, 400.0)),
                ),
            ),
            "LatchAverage": DictElement(
                parameter_form = SimpleLevels(
                    title = Title("Average latch wait time (ms)"),
                    level_direction = LevelDirection.UPPER,
                    form_spec_template = Float(),
                    prefill_fixed_levels = DefaultValue((20.0, 40.0)),
                ),
            ),
        },
    )


rule_spec_mssql_counters_latches = CheckParameters(
    name = "mssql_counters_latches",
    topic = Topic.APPLICATIONS,
    condition = HostAndItemCondition(item_title = Title("Instance")),
    parameter_form = _parameter_valuespec_mssql_counters_latches,
    title = Title("MSSQL latches"),
)
