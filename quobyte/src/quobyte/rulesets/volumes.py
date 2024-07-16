#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import (
    Dictionary,
    DictElement,
    SimpleLevels,
    LevelDirection,
    InputHint,
    DataSize,
    Integer,
    SIMagnitude,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic

MAGNITUDES = [SIMagnitude.GIGA, SIMagnitude.TERA, SIMagnitude.PETA]


def _parameter_form_quobyte_volumes():
    return Dictionary(
        title = Title("Quobyte volume levels"),
        elements = {
            "used_allocated_space": DictElement(
                parameter_form = SimpleLevels(
                    title = Title("Allocated space"),
                    level_direction = LevelDirection.UPPER,
                    form_spec_template = DataSize(
                        displayed_magnitudes = MAGNITUDES,
                    ),
                    prefill_fixed_levels = InputHint((1000000000000, 2000000000000)),
                )
            ),
            "used_logical_space": DictElement(
                parameter_form = SimpleLevels(
                    title = Title("Used logical space "),
                    level_direction = LevelDirection.UPPER,
                    form_spec_template = DataSize(
                        displayed_magnitudes=MAGNITUDES,
                    ),
                    prefill_fixed_levels = InputHint((1000000000000, 2000000000000)),
                )
            ),
            "used_disk_space": DictElement(
                parameter_form = SimpleLevels(
                    title = Title("Used disk space"),
                    level_direction = LevelDirection.UPPER,
                    form_spec_template = DataSize(
                        displayed_magnitudes=MAGNITUDES,
                    ),
                    prefill_fixed_levels = InputHint((1000000000000, 2000000000000)),
                )
            ),
            "file_count": DictElement(
                parameter_form = SimpleLevels(
                    title = Title("Total count of files"),
                    level_direction = LevelDirection.UPPER,
                    form_spec_template = Integer(),
                    prefill_fixed_levels = InputHint((0, 0)),
                )
            ),
            "directory_count": DictElement(
                parameter_form = SimpleLevels(
                    title = Title("Total count of directories"),
                    level_direction = LevelDirection.UPPER,
                    form_spec_template = Integer(),
                    prefill_fixed_levels = InputHint((0, 0)),
                )
            ),
        },
    )


rule_spec_quobyte_volumes = CheckParameters(
    name = "quobyte_volumes",
    topic = Topic.OPERATING_SYSTEM,
    condition = HostAndItemCondition(item_title = Title("Volume name")),
    parameter_form = _parameter_form_quobyte_volumes,
    title = Title("Quobyte volumes"),
)
