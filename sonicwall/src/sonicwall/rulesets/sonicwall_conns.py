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
    LevelDirection,
    Percentage,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _parameter_form_sonicwall_conns() -> Dictionary:
    return Dictionary(
        elements={
            "levels": DictElement(
                required=True,
                parameter_form=SimpleLevels(
                    title=Title("Levels on connection usage"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Percentage(),
                    prefill_fixed_levels=DefaultValue((80.0, 95.0)),
                ),
            ),
        },
    )


rule_spec_sonicwall_conns = CheckParameters(
    name="sonicwall_conns",
    title=Title("SonicWall Connections"),
    topic=Topic.NETWORKING,
    parameter_form=_parameter_form_sonicwall_conns,
    condition=HostAndItemCondition(item_title=Title("Connection table")),
)
