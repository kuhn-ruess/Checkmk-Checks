"""
ERA output channel check parameters.
"""
from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    Integer,
    LevelDirection,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _bps_levels(direction, title, defaults):
    return SimpleLevels(
        title=Title(title),
        level_direction=direction,
        form_spec_template=Integer(unit_symbol="B/s"),
        prefill_fixed_levels=DefaultValue(defaults),
    )


def _parameters():
    return Dictionary(
        title=Title("ERA output channel thresholds"),
        elements={
            "bps_upper": DictElement(parameter_form=_bps_levels(LevelDirection.UPPER, "Upper throughput", (0, 0))),
            "bps_lower": DictElement(parameter_form=_bps_levels(LevelDirection.LOWER, "Lower throughput", (0, 0))),
        },
    )


rule_spec_era_outchann = CheckParameters(
    name="era_outchann",
    topic=Topic.NETWORKING,
    condition=HostAndItemCondition(item_title=Title("Output channel")),
    parameter_form=_parameters,
    title=Title("ERA output channels"),
)
