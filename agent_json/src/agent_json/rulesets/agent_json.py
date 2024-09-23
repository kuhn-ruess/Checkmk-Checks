#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consuling and Development
https://kuhn-ruess.de
"""

from cmk.rulesets.v1 import Title, Help
from cmk.rulesets.v1.form_specs import (
    Dictionary,
    DictElement,
    String,
    Password,
)
from cmk.rulesets.v1.form_specs.validators import LengthInRange
from cmk.rulesets.v1.rule_specs import SpecialAgent, Topic


def _parameter_form_special_agent_json():
    return Dictionary(
        title = Title("Agent JSON"),
        help_text = Help("This rule set selects the special agent who parses json"),
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
                required = False,
            ),
            "password": DictElement(
                parameter_form = Password(
                    title = Title("Password"),
                ),
                required = False,
            ),
        },
    )


rule_spec_agent_json = SpecialAgent(
    name = "json",
    topic = Topic.SERVER_HARDWARE,
    parameter_form = _parameter_form_special_agent_json,
    title = Title("Agent JSON"),
)
