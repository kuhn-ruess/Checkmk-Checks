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


def as400_jobs() -> Dictionary:
    return Dictionary(
        elements={
            "job_levels": DictElement(
                parameter_form=SimpleLevels[int](
                    title=Title("Job"),
                    form_spec_template=Integer(unit_symbol="Jobs"),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=InputHint(value=(9000, 9500)),
                )
            ),
        }
    )


rule_spec_as400_jobs = CheckParameters(
    name="as400_jobs",
    topic=Topic.APPLICATIONS,
    condition=HostCondition(),
    parameter_form=as400_jobs,
    title=Title("AS400 Jobs"),
)
