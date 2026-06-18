#!/usr/bin/env python3

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
    List,
    Percentage,
    SimpleLevels,
    String,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _parameter_form_quobyte_devices() -> Dictionary:
    return Dictionary(
        title=Title("Quobyte device levels"),
        elements={
            "usage_levels": DictElement(
                required=True,
                parameter_form=SimpleLevels(
                    title=Title("Disk usage levels"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Percentage(),
                    prefill_fixed_levels=DefaultValue((90.0, 95.0)),
                ),
            ),
            "modes": DictElement(
                required=True,
                parameter_form=Dictionary(
                    title=Title("Device status to monitoring state mapping"),
                    elements={
                        "warning": DictElement(
                            required=True,
                            parameter_form=List(
                                title=Title("Device states resulting in WARN"),
                                element_template=String(),
                            ),
                        ),
                        "critical": DictElement(
                            required=True,
                            parameter_form=List(
                                title=Title("Device states resulting in CRIT"),
                                element_template=String(),
                            ),
                        ),
                    },
                ),
            ),
        },
    )


rule_spec_quobyte_devices = CheckParameters(
    name="quobyte_devices",
    topic=Topic.OPERATING_SYSTEM,
    condition=HostAndItemCondition(item_title=Title("Device ID")),
    parameter_form=_parameter_form_quobyte_devices,
    title=Title("Quobyte devices"),
)
