#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    CascadingSingleChoice,
    CascadingSingleChoiceElement,
    DataSize,
    DefaultValue,
    DictElement,
    Dictionary,
    IECMagnitude,
    InputHint,
    LevelDirection,
    Percentage,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _valuespec_exasol_database():
    return Dictionary(
        title = Title("Set levels for Exasol database size"),
        help_text = Help("Set levels for Exasol database size"),
        elements = {
            "levels": DictElement(
                parameter_form = CascadingSingleChoice(
                    title = Title("Used space"),
                    prefill = DefaultValue("absolute"),
                    elements = [
                        CascadingSingleChoiceElement(
                            name = "absolute",
                            title = Title("Absolute"),
                            parameter_form = SimpleLevels(
                                title = Title("Levels"),
                                level_direction = LevelDirection.UPPER,
                                form_spec_template = DataSize(displayed_magnitudes=[IECMagnitude.MEBI,IECMagnitude.GIBI,IECMagnitude.TEBI]),
                                prefill_fixed_levels = InputHint((1024 * 1024 * 1024, 2 * 1024 * 1024 * 1024)),
                            ),
                        ),
                        CascadingSingleChoiceElement(
                            name = "percentage",
                            title = Title("Percentage"),
                            parameter_form = SimpleLevels(
                                title = Title("Levels"),
                                level_direction = LevelDirection.UPPER,
                                form_spec_template = Percentage(),
                                prefill_fixed_levels = InputHint((80, 90)),
                            ),
                        ),
                    ],
                ),
                required = True,
            ),
        },
    )


rule_spec_exasol = CheckParameters(
    title = Title("Exasol DB usage"),
    name = "exasol_database",
    condition = HostAndItemCondition(item_title = Title("Database name")),
    topic = Topic.DATABASES,
    parameter_form = _valuespec_exasol_database,
)
