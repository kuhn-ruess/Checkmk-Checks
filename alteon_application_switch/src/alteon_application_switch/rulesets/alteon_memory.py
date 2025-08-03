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


def _parameter_valuespec_alteon_memory():
    return Dictionary(
        elements={
            "alteon_memory_tresholds": DictElement(
                parameter_form=Dictionary(
                    elements={
                        "percentVirtual": DictElement(
                            parameter_form=SimpleLevels(
                                title=Title("Thresholds (warn/crit) for Alteon Virtual Memory"),
                                help_text=Help("The provided thresholds are used for Virtual memory. The service is Warning/Critical if this value exceeds the threshold"),
                                level_direction=LevelDirection.UPPER,
                                form_spec_template=Float(unit_symbol="%"),
                                prefill_fixed_levels=DefaultValue((75.0, 90.0)),
                            ),
                            required=False,
                        ),
                        "percentRss": DictElement(
                            parameter_form=SimpleLevels(
                                title=Title("Thresholds (warn/crit) for Alteon RSS Memory"),
                                help_text=Help("The provided thresholds are used for RSS memory. The service is Warning/Critical if this value exceeds the threshold"),
                                level_direction=LevelDirection.UPPER,
                                form_spec_template=Float(unit_symbol="%"),
                                prefill_fixed_levels=DefaultValue((75.0, 90.0)),
                            ),
                            required=False,
                        ),
                        "CurrentSP": DictElement(
                            parameter_form=SimpleLevels(
                                title=Title("Thresholds (warn/crit) for Alteon Current Memory usage per Core"),
                                help_text=Help("The provided thresholds are used for Total Memory usage per Core. The service is Warning/Critical if the memory of one core exceeds the threshold"),
                                level_direction=LevelDirection.UPPER,
                                form_spec_template=Float(unit_symbol="%"),
                                prefill_fixed_levels=DefaultValue((75.0, 90.0)),
                            ),
                            required=False,
                        ),
                    }
                ),
                required=True,
            ),
        }
    )


rule_spec_alteon_memory = CheckParameters(
    name="alteon_memory",
    topic=Topic.APPLICATIONS,
    condition=HostAndItemCondition(
        item_title=Title("Memory for core"),
        item_form=String(),
    ),
    parameter_form=_parameter_valuespec_alteon_memory,
    title=Title("Alteon Memory"),
)
