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
from cmk.rulesets.v1.rule_specs import CheckParameters, HostCondition, Topic


def _parameter_form_sidecooler_coldwater():
    return Dictionary(
        title = Title("Sidecooler coldwater"),
        elements = {
            "water_supply": DictElement(
                parameter_form = SimpleLevels(
                    title = Title("Temperature supply"),
                    level_direction = LevelDirection.UPPER,
                    form_spec_template = Float(),
                    prefill_fixed_levels = InputHint((20, 25)),
                )
            ),
            "water_return": DictElement(
                parameter_form = SimpleLevels(
                    title = Title("Temperature return"),
                    level_direction = LevelDirection.UPPER,
                    form_spec_template = Float(),
                    prefill_fixed_levels = InputHint((25, 30)),
                )
            ),
        },
    )


rule_spec_sidecooler_temp = CheckParameters(
    name = "sidecooler_coldwater",
    topic = Topic.ENVIRONMENTAL,
    condition = HostCondition(),
    parameter_form = _parameter_form_sidecooler_coldwater,
    title = Title("Sidecooler coldwater"),
)
