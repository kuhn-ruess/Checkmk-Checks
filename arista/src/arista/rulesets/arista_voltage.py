#!/usr/bin/env python3

from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    Integer,
    SimpleLevels,
    LevelDirection,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _parameter_form_arista_voltage() -> Dictionary:
    return Dictionary(
        elements={
            "levels_lower": DictElement(
                required=True,
                parameter_form=SimpleLevels[int](
                    title=Title("Lower voltage levels"),
                    help_text=Help(
                        "Warn/crit when the measured voltage falls to or below "
                        "the configured thresholds."
                    ),
                    form_spec_template=Integer(unit_symbol="V"),
                    level_direction=LevelDirection.LOWER,
                    prefill_fixed_levels=DefaultValue((50, 50)),
                ),
            ),
        },
    )


rule_spec_arista_voltage = CheckParameters(
    name="arista_voltage",
    title=Title("Arista Voltage"),
    topic=Topic.ENVIRONMENTAL,
    parameter_form=_parameter_form_arista_voltage,
    condition=HostAndItemCondition(item_title=Title("Sensor name")),
)
