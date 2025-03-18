#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.rulesets.v1 import Title, Help
from cmk.rulesets.v1.form_specs import (
    Dictionary,
    DictElement,
    String,
    Password,
    TimeSpan,
    TimeMagnitude,
    DefaultValue,
)
from cmk.rulesets.v1.form_specs.validators import LengthInRange
from cmk.rulesets.v1.rule_specs import SpecialAgent, Topic


def _parameter_form_special_agents_veritas():
    return Dictionary(
        title = Title("veritas via WebAPI"),
        help_text = Help("This rule set selects the special agent for veritas"),
        elements = {
            "api_url": DictElement(
                parameter_form = String(
                    title = Title("API URL"),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required = True,
            ),
            "username": DictElement(
                parameter_form = String(
                    title = Title("Username"),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required = True,
            ),
            "password": DictElement(
                parameter_form = Password(
                    title = Title("Password"),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required = True,
            ),
        },
    )


rule_spec_veritas = SpecialAgent(
    name = "veritas",
    topic = Topic.STORAGE,
    parameter_form = _parameter_form_special_agents_veritas,
    title = Title("Veritas Flex Appliance"),
)
