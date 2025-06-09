#!/usr/bin/python3
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
        Integer,
        LevelDirection,
        InputHint,
)

from cmk.rulesets.v1.rule_specs import (
        CheckParameters,
        HostCondition,
        Topic,
)

def _parameter_digital_signage() -> Dictionary:
    return Dictionary(
            elements={
                "GPU_Load_3D": DictElement(
                    parameter_form=SimpleLevels[int](
                        title=Title("GPU Load 3D"),
                        form_spec_template=Integer(unit_symbol="Units"),
                        level_direction=LevelDirection.UPPER,
                        prefill_fixed_levels=InputHint(value=(0, 0)),
                    )
                ),
                "GPU_Load_Copy": DictElement(
                    parameter_form=SimpleLevels[int](
                        title=Title("GPU Load Copy"),
                        form_spec_template=Integer(unit_symbol="Units"),
                        level_direction=LevelDirection.UPPER,
                        prefill_fixed_levels=InputHint(value=(0, 0)),
                    )
                ),
                "GPU_Load_VideoProcessing": DictElement(
                    parameter_form=SimpleLevels[int](
                        title=Title("GPU Load Video Processing"),
                        form_spec_template=Integer(unit_symbol="Units"),
                        level_direction=LevelDirection.UPPER,
                        prefill_fixed_levels=InputHint(value=(0, 0)),
                    )
                ),
                "GPU_Load_VideoDecode": DictElement(
                    parameter_form=SimpleLevels[int](
                        title=Title("GPU Load Video Decode"),
                        form_spec_template=Integer(unit_symbol="Units"),
                        level_direction=LevelDirection.UPPER,
                        prefill_fixed_levels=InputHint(value=(0, 0)),
                    )
                ),
            }
        )

rule_spec_digital_signae = CheckParameters(
    name="digital_signage",
    topic=Topic.APPLICATIONS,
    condition=HostCondition(),
    parameter_form=_parameter_digital_signage,
    title=Title("Digital Signage"),
)
