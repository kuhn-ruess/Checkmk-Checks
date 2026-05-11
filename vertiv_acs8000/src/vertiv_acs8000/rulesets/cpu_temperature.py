#!/usr/bin/env python3

"""
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
from cmk.rulesets.v1.rule_specs import CheckParameters, HostCondition, Topic


def _parameter_form_vertiv_acs8000_cpu_temperature():
    return Dictionary(
        title=Title("Vertiv ACS CPU temperature"),
        help_text=Help("Upper temperature levels for the internal CPU of a Vertiv Avocent ACS 8000 console server."),
        elements={
            "levels": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Upper levels for CPU temperature"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Float(unit_symbol="°C"),
                    prefill_fixed_levels=DefaultValue((70.0, 85.0)),
                ),
            ),
        },
    )


rule_spec_vertiv_acs8000_cpu_temperature = CheckParameters(
    name="vertiv_acs8000_cpu_temperature",
    topic=Topic.ENVIRONMENTAL,
    condition=HostCondition(),
    parameter_form=_parameter_form_vertiv_acs8000_cpu_temperature,
    title=Title("Vertiv ACS CPU temperature"),
)
