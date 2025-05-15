#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DictElement,
    Dictionary,
    Password,
)
from cmk.rulesets.v1.form_specs.validators import LengthInRange
from cmk.rulesets.v1.rule_specs import (
    SpecialAgent,
    Topic,
)


def _valuespec_special_agent_pure():
    return Dictionary(
        title = Title("Pure via WebAPI"),
        help_text = Help("This rule set selects the special agent for Pure"),
        elements = {
            "token": DictElement(
                parameter_form = Password(
                    title = Title("Web API Token"),
                    custom_validate = (LengthInRange(min_value=1),),
                ),
                required = True,
            ),
        },
    )

rule_spec_pure = SpecialAgent(
    name = "pure",
    topic = Topic.STORAGE,
    parameter_form = _valuespec_special_agent_pure,
    title = Title("Pure via WebAPI"),
)
