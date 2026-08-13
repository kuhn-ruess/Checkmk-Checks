#!/usr/bin/env python3
"""
Palo Alto XML API - Environment check ruleset

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
from cmk.rulesets.v1 import Help, Title
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
        title=Title("Palo Alto environment"),
        help_text=Help(
            "In addition to the firewall's own alarm flag, optional temperature "
            "thresholds can be configured for temperature sensors."
        ),
        elements={
            "levels": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Temperature levels"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Float(unit_symbol="°C"),
                    prefill_fixed_levels=DefaultValue((70.0, 80.0)),
                ),
                required=False,
            ),
        },
    )


rule_spec_palo_alto_api_environment = CheckParameters(
    name="palo_alto_api_environment",
    topic=Topic.NETWORKING,
    parameter_form=_parameter_form,
    title=Title("Palo Alto environment"),
    condition=HostAndItemCondition(item_title=Title("Sensor")),
)
