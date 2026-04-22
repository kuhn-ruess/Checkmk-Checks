"""
ERA RX check parameters. Focuses on the garbled-Mode-S ratio since
absolute counter thresholds depend heavily on deployment.
"""
from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    Float,
    Integer,
    LevelDirection,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _parameters():
    return Dictionary(
        title=Title("ERA RX thresholds"),
        elements={
            "garbled_ratio": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Garbled Mode-S message ratio"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Float(unit_symbol="%"),
                    prefill_fixed_levels=DefaultValue((5.0, 10.0)),
                ),
            ),
            "ac_all": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("A/C codes upper levels"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Integer(),
                    prefill_fixed_levels=DefaultValue((0, 0)),
                ),
            ),
            "modes_all": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Mode-S total upper levels"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Integer(),
                    prefill_fixed_levels=DefaultValue((0, 0)),
                ),
            ),
            "modes_garbled": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Mode-S garbled upper levels"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Integer(),
                    prefill_fixed_levels=DefaultValue((0, 0)),
                ),
            ),
        },
    )


rule_spec_era_rx = CheckParameters(
    name="era_rx",
    topic=Topic.NETWORKING,
    condition=HostAndItemCondition(item_title=Title("RX site")),
    parameter_form=_parameters,
    title=Title("ERA RX receivers"),
)
