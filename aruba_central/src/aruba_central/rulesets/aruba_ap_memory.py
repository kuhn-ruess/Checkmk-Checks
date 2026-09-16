#!/usr/bin/env python3
"""
Aruba Central - access point memory ruleset

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    LevelDirection,
    Percentage,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostCondition, Topic


def _parameter_form():
    return Dictionary(
        title=Title("Aruba access point memory"),
        elements={
            "levels_used": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Levels on the used memory"),
                    help_text=Help(
                        "The used memory is derived from the total and the free "
                        "memory Aruba Central reports for the access point."
                    ),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Percentage(),
                    prefill_fixed_levels=DefaultValue((80.0, 90.0)),
                ),
                required=True,
            ),
        },
    )


rule_spec_aruba_ap_memory = CheckParameters(
    name="aruba_ap_memory",
    topic=Topic.NETWORKING,
    parameter_form=_parameter_form,
    title=Title("Aruba access point memory"),
    condition=HostCondition(),
)
