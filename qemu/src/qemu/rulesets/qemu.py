#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
"""Check parameters for the qemu check plugin."""
from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    Float,
    LevelDirection,
    SimpleLevels,
    String,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _parameter_form_qemu() -> Dictionary:
    return Dictionary(
        elements={
            "cpu": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("CPU usage"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Float(unit_symbol="%"),
                    prefill_fixed_levels=DefaultValue((80.0, 90.0)),
                ),
            ),
            "mem": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Memory usage"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Float(unit_symbol="%"),
                    prefill_fixed_levels=DefaultValue((80.0, 90.0)),
                ),
            ),
        },
    )


rule_spec_qemu = CheckParameters(
    name="qemu",
    topic=Topic.APPLICATIONS,
    condition=HostAndItemCondition(
        item_title=Title("VM name"),
        item_form=String(),
    ),
    parameter_form=_parameter_form_qemu,
    title=Title("Qemu / KVM"),
)
