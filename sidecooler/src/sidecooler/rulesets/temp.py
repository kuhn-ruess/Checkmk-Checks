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
    Float,
    InputHint,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _parameter_form_sidecooler_temp():
    return Dictionary(
        title = Title("Sidecooler temperatures"),
        elements = {
            "mean": DictElement(
                parameter_form = SimpleLevels(
                    title = Title("Temperature mean"),
                    level_direction = LevelDirection.UPPER,
                    form_spec_template = Float(),
                    prefill_fixed_levels = InputHint((30, 35)),
                )
            ),
            "top": DictElement(
                parameter_form = SimpleLevels(
                    title = Title("Temperature top"),
                    level_direction = LevelDirection.UPPER,
                    form_spec_template = Float(),
                    prefill_fixed_levels = InputHint((30, 35)),
                )
            ),
            "center": DictElement(
                parameter_form = SimpleLevels(
                    title = Title("Temperature center"),
                    level_direction = LevelDirection.UPPER,
                    form_spec_template = Float(),
                    prefill_fixed_levels = InputHint((30, 35)),
                )
            ),
            "bottom": DictElement(
                parameter_form = SimpleLevels(
                    title = Title("Temperature bottom"),
                    level_direction = LevelDirection.UPPER,
                    form_spec_template = Float(),
                    prefill_fixed_levels = InputHint((30, 35)),
                )
            ),
        },
    )


rule_spec_sidecooler_temp = CheckParameters(
    name = "sidecooler_temp",
    topic = Topic.ENVIRONMENTAL,
    condition = HostAndItemCondition(item_title = Title("Side")),
    parameter_form = _parameter_form_sidecooler_temp,
    title = Title("Sidecooler temperatures"),
)
