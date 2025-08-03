#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    String,
    Float,
    LevelDirection,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _parameter_valuespec_alteon_cpu():
    return Dictionary(
        elements={
            "alteon_cpu_utilization_tresholds": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Thresholds (warn/crit) for Alteon CPU"),
                    help_text=Help("The provided thresholds are used for Averages of 1, 4 and 64 seconds. The service is Warning/Critical if one of these values exceeds the threshold"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Float(unit_symbol="%"),
                    prefill_fixed_levels=DefaultValue((80.0, 90.0)),
                ),
                required=True,
            ),
        }
    )


rule_spec_alteon_cpu = CheckParameters(
    name="alteon_cpu",
    topic=Topic.APPLICATIONS,
    condition=HostAndItemCondition(
        item_title=Title("CPU Name"),
        item_form=String(),
    ),
    parameter_form=_parameter_valuespec_alteon_cpu,
    title=Title("Alteon CPU"),
)
