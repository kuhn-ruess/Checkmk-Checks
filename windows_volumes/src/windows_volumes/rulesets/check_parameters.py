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
    Percentage,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _parameter_form_windows_volumes() -> Dictionary:
    return Dictionary(
        help_text=Help(
            "Upper levels for the used space (in percent) of a folder mounted "
            "Windows volume."
        ),
        elements={
            "levels": DictElement(
                required=True,
                parameter_form=SimpleLevels(
                    title=Title("Levels for used space"),
                    form_spec_template=Percentage(),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=DefaultValue((80.0, 90.0)),
                ),
            ),
        },
    )


rule_spec_windows_volumes = CheckParameters(
    name="windows_volumes",
    title=Title("Windows Volumes (folder mount points)"),
    topic=Topic.STORAGE,
    parameter_form=_parameter_form_windows_volumes,
    condition=HostAndItemCondition(item_title=Title("Volume")),
)
