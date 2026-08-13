#!/usr/bin/env python3
"""
Palo Alto XML API - CPU check ruleset

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    Float,
    LevelDirection,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _parameter_form():
    return Dictionary(
        title=Title("Palo Alto CPU utilization"),
        elements={
            "levels": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Utilization"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Float(unit_symbol="%"),
                    prefill_fixed_levels=DefaultValue((80.0, 90.0)),
                ),
                required=False,
            ),
        },
    )


rule_spec_palo_alto_api_cpu = CheckParameters(
    name="palo_alto_api_cpu",
    topic=Topic.NETWORKING,
    parameter_form=_parameter_form,
    title=Title("Palo Alto CPU utilization"),
    condition=HostAndItemCondition(item_title=Title("Plane")),
)
