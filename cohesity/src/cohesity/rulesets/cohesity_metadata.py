# 2021 created by Sven Rueß, sritd.de

from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    Percentage,
    DictElement,
    Dictionary,
    InputHint,
    LevelDirection,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostCondition, Topic


def _formspec_cohesity_metadata():
    return Dictionary(
        elements = {
            "levels_pct": DictElement(
                parameter_form = SimpleLevels(
                    title = Title("Maximum percent usage of cluster metadata"),
                    help_text = Help("Please configure levels for maximum percent used metadata of cluster."),
                    level_direction = LevelDirection.UPPER,
                    form_spec_template = Percentage(),
                    prefill_fixed_levels = InputHint((80, 90)),
                ),
            ),
        },
    )


rule_spec_cohesity_metadata = CheckParameters(
    name = "cohesity_metadata",
    topic = Topic.STORAGE,
    condition = HostCondition(),
    parameter_form = _formspec_cohesity_metadata,
    title = Title("Cohesity metadata usage"),
)

