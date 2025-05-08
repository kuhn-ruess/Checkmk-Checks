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
)
from cmk.rulesets.v1.form_specs.validators import LengthInRange

from cmk.rulesets.v1.rule_specs import (
        SpecialAgent,
        Topic,
)


def _valuespec_special_agent_semu():
    """
    SEMU Agent Configuration
    """

    return Dictionary(
        title = Title("SEMU Agent"),
        help_text = Help("This rule activates special agent for SEMU."),
        elements = {
            "username": DictElement(
                parameter_form = String(
                    title = Title("Username"),
                    help_text = Help("User to connect via Auth Basic"),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required = True,
            ),
            "password": DictElement(
                parameter_form = Password(
                    title = Title("Password"),
                    help_text = Help("Password of the user"),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required = True,
            ),
        },
    )


rule_spec_semu = SpecialAgent(
    name = "agent_semu",
    topic = Topic.APPLICATIONS,
    parameter_form = _valuespec_special_agent_semu,
    title = Title("SEMU Framerate"),
)
