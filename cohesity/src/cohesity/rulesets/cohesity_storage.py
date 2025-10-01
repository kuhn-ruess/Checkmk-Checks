# 2021 created by Sven Rueß, sritd.de

from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    SimpleLevels,
    DictElement,
    Dictionary,
    LevelDirection,
    Percentage,
    InputHint,
    SIMagnitude,
    DataSize,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostCondition, Topic

MAGNITUDES = [SIMagnitude.MEGA, SIMagnitude.GIGA, SIMagnitude.TERA]


def _formspec_cohesity_storage():
    return Dictionary(
        elements = {
            "levels": DictElement(
                parameter_form = SimpleLevels(
                    title = Title("Maximum size of cluster filesystem"),
                    help_text = Help("Please configure levels for maximum used filesystem size of cluster."),
                    level_direction = LevelDirection.UPPER,
                    form_spec_template = DataSize(
                        displayed_magnitudes = MAGNITUDES,
                    ),
                    prefill_fixed_levels = InputHint((1000000000000, 2000000000000)),
                ),
            ),
            "levels_pct": DictElement(
                parameter_form = SimpleLevels(
                    title = Title("Maximum percent size of cluster filesystem"),
                    help_text = Help("Please configure levels for maximum percent used filesystem size of cluster."),
                    level_direction = LevelDirection.UPPER,
                    form_spec_template = Percentage(),
                    prefill_fixed_levels = InputHint((80, 90)),
                ),
            ),
        }
    )


rule_spec_cohesity_storage = CheckParameters(
    name = "cohesity_storage",
    topic = Topic.STORAGE,
    condition = HostCondition(),
    parameter_form = _formspec_cohesity_storage,
    title = Title("Cohesity filesystem size"),
)

