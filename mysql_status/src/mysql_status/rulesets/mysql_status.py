#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    Dictionary,
    DictElement,
    InputHint,
    Integer,
    LevelDirection,
    SimpleLevels,
    SingleChoice,
    SingleChoiceElement,
)
from cmk.rulesets.v1.rule_specs import (
    CheckParameters,
    HostAndItemCondition,
    Topic,
)


def _valuespec_mysql_status():
    return Dictionary(
        title = Title("Settings for MySQL status check"),
        elements = {
            "levels": DictElement(
                parameter_form = SimpleLevels(
                    title = Title("Rate/Unit levels"),
                    level_direction = LevelDirection.UPPER,
                    form_spec_template = Integer(),
                    prefill_fixed_levels = InputHint((5, 8)),
                ),
            ),
            "target_state": DictElement(
                parameter_form = SingleChoice(
                    title = Title("Target state"),
                    elements = [
                        SingleChoiceElement(
                            title=Title("ON is OK"),
                            name="on"
                        ),
                        SingleChoiceElement(
                            title=Title("OFF is OK"),
                            name="off"
                        ),
                    ],
                ),
            ),
        },
    )


rule_spec_mysql_status = CheckParameters(
    title = Title("Settings for MySQL status check"),
    name = "mysql_status",
    condition = HostAndItemCondition(item_title = Title("Variable name")),
    topic = Topic.APPLICATIONS,
    parameter_form = _valuespec_mysql_status,
)
