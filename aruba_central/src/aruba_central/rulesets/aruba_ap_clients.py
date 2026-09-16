#!/usr/bin/env python3
"""
Aruba Central - access point clients ruleset

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    Integer,
    LevelDirection,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostCondition, Topic


def _parameter_form():
    return Dictionary(
        title=Title("Aruba access point clients"),
        elements={
            "levels_clients": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Levels on the connected clients"),
                    help_text=Help(
                        "Number of wireless clients associated with this access "
                        "point. Without levels the check only records the metric."
                    ),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Integer(),
                    prefill_fixed_levels=DefaultValue((50, 80)),
                ),
                required=False,
            ),
        },
    )


rule_spec_aruba_ap_clients = CheckParameters(
    name="aruba_ap_clients",
    topic=Topic.NETWORKING,
    parameter_form=_parameter_form,
    title=Title("Aruba access point clients"),
    condition=HostCondition(),
)
