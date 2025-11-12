#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.rulesets.v1 import (
        Title,
)

from cmk.rulesets.v1.form_specs import (
        Dictionary,
        DictElement,
        SimpleLevels,
        Integer,
        LevelDirection,
        InputHint,
)

from cmk.rulesets.v1.rule_specs import (
        CheckParameters,
        HostCondition,
        Topic,
)


def as400_cpu() -> Dictionary:
    return Dictionary(
        elements={
            "cpu_levels": DictElement(
                parameter_form=SimpleLevels[int](
                    title=Title("CPU"),
                    form_spec_template=Integer(),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=InputHint(value=(80, 90)),
                )
            ),
        }
    )


rule_spec_as400_cpu = CheckParameters(
    name="as400_cpu",
    topic=Topic.APPLICATIONS,
    condition=HostCondition(),
    parameter_form=as400_cpu,
    title=Title("AS400 CPU"),
)
