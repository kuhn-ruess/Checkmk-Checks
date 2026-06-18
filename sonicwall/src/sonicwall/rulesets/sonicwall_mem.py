"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    LevelDirection,
    Percentage,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostCondition, Topic


def _parameter_form_sonicwall_mem() -> Dictionary:
    return Dictionary(
        elements={
            "levels": DictElement(
                required=True,
                parameter_form=SimpleLevels(
                    title=Title("Levels on memory usage"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Percentage(),
                    prefill_fixed_levels=DefaultValue((80.0, 95.0)),
                ),
            ),
        },
    )


rule_spec_sonicwall_mem = CheckParameters(
    name="sonicwall_mem",
    title=Title("SonicWall Memory usage"),
    topic=Topic.NETWORKING,
    parameter_form=_parameter_form_sonicwall_mem,
    condition=HostCondition(),
)
