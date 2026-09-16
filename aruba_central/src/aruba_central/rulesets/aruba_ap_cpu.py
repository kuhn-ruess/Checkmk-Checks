#!/usr/bin/env python3
"""
Aruba Central - access point CPU ruleset

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
        title=Title("Aruba access point CPU utilization"),
        elements={
            "levels_util": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Levels on the CPU utilization"),
                    help_text=Help(
                        "Aruba Central reports the CPU utilization of the access "
                        "point as a single percentage value."
                    ),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Percentage(),
                    prefill_fixed_levels=DefaultValue((80.0, 90.0)),
                ),
                required=True,
            ),
        },
    )


rule_spec_aruba_ap_cpu = CheckParameters(
    name="aruba_ap_cpu",
    topic=Topic.NETWORKING,
    parameter_form=_parameter_form,
    title=Title("Aruba access point CPU utilization"),
    condition=HostCondition(),
)
