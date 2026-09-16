#!/usr/bin/env python3
"""
Aruba Central - collector status ruleset

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
        title=Title("Aruba Central status"),
        elements={
            "levels_down": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Levels on the access points that are down"),
                    help_text=Help(
                        "cencli reports the number of access points as "
                        "'ap: 393 (386:7)', the second number in the brackets "
                        "being the access points that are down."
                    ),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Integer(),
                    prefill_fixed_levels=DefaultValue((1, 10)),
                ),
                required=True,
            ),
            "levels_rate_remaining": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Lower levels on the remaining API calls"),
                    help_text=Help(
                        "Aruba Central limits the number of API calls per day. "
                        "Running out of calls means no fresh data until the limit "
                        "is reset, so it pays to be warned early."
                    ),
                    level_direction=LevelDirection.LOWER,
                    form_spec_template=Integer(),
                    prefill_fixed_levels=DefaultValue((1000, 100)),
                ),
                required=True,
            ),
        },
    )


rule_spec_aruba_central = CheckParameters(
    name="aruba_central",
    topic=Topic.NETWORKING,
    parameter_form=_parameter_form,
    title=Title("Aruba Central status"),
    condition=HostCondition(),
)
