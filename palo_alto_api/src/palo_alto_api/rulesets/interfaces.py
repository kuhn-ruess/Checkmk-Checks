#!/usr/bin/env python3
"""
Palo Alto XML API - Interface check ruleset

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
    ServiceState,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _parameter_form():
    return Dictionary(
        title=Title("Palo Alto interface"),
        elements={
            "state_down": DictElement(
                parameter_form=ServiceState(
                    title=Title("State when the interface is not up"),
                    prefill=DefaultValue(ServiceState.CRIT),
                ),
                required=True,
            ),
            "levels_errors": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Error / discard rate"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Float(unit_symbol="/s"),
                    prefill_fixed_levels=DefaultValue((1.0, 10.0)),
                ),
                required=False,
            ),
        },
    )


rule_spec_palo_alto_api_interfaces = CheckParameters(
    name="palo_alto_api_interfaces",
    topic=Topic.NETWORKING,
    parameter_form=_parameter_form,
    title=Title("Palo Alto interface"),
    condition=HostAndItemCondition(item_title=Title("Interface")),
)
