#!/usr/bin/env python
"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""


from cmk.rulesets.v1 import (
        Title,
)

from cmk.rulesets.v1.form_specs import (
        Dictionary,
        DictElement,
        SimpleLevels,
        DataSize,
        IECMagnitude,
        LevelDirection,
        InputHint,
)

from cmk.rulesets.v1.rule_specs import (
        CheckParameters,
        HostAndItemCondition,
        Topic,
)


MAGNITUDES = tuple(IECMagnitude)[:5]

def _migrate(value):
    """
    Migration function to convert old parameter format to new format.
    """
    if 'levels_upper' in value:
        value = {
            "levels": ('fixed', value['levels_upper']),
        }
    return value


def _parameter_dir_size() -> Dictionary:
    return Dictionary(
            migrate=_migrate,
            elements={
                "levels": DictElement(
                    parameter_form=SimpleLevels[int](
                        title=Title("Limits for folder size"),
                        form_spec_template=DataSize(displayed_magnitudes=MAGNITUDES),
                        level_direction=LevelDirection.UPPER,
                        prefill_fixed_levels=InputHint(value=(0, 0)),
                    ),
                    required=True,
                ),
            }
        )

rule_spec_dir_size = CheckParameters(
    name="dir_size",
    topic=Topic.APPLICATIONS,
    condition=HostAndItemCondition(
        item_title=Title("Directory Path")
    ),
    parameter_form=_parameter_dir_size,
    title=Title("dir_size: Directory Parameters"),
)
