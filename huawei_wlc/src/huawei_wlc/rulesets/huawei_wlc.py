#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    Dictionary,
    DictElement,
    Integer,
    LevelDirection,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _parameter_form_huawei_wlc():
    return Dictionary(
        title=Title("Huawei WLC access point"),
        elements={
            "levels_users": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Upper levels for online users"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Integer(),
                    prefill_fixed_levels=DefaultValue((50, 100)),
                ),
            ),
        },
    )


rule_spec_huawei_wlc = CheckParameters(
    name="huawei_wlc",
    topic=Topic.NETWORKING,
    condition=HostAndItemCondition(item_title=Title("Access point")),
    parameter_form=_parameter_form_huawei_wlc,
    title=Title("Huawei WLC access point"),
)
