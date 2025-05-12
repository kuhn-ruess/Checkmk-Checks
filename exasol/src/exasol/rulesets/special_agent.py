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
    List,
    Password,
    String,
)
from cmk.rulesets.v1.form_specs.validators import LengthInRange
from cmk.rulesets.v1.rule_specs import (
    SpecialAgent,
    Topic,
)


def _valuespec_special_agent_exasol():
    return Dictionary(
        title = Title("Exasol via XMLApi"),
        help_text = Help("This rule set selects the special agent for exasol"),
        elements = {
            "username": DictElement(
                parameter_form = String(
                    title = Title("Username"),
                    custom_validate = (LengthInRange(min_value=1),),
                ),
                required = True,
            ),
            "password": DictElement(
                parameter_form = Password(
                    title = Title("Password"),
                    custom_validate = (LengthInRange(min_value=1),),
                ),
                required = True,
            ),
            "ignore_dbs": DictElement(
                parameter_form = List(
                    title = Title("Databases to ignore"),
                    element_template = String(custom_validate = (LengthInRange(min_value=1),),),
                    custom_validate = (LengthInRange(min_value=1),),
                ),
            ),
        },
    )

rule_spec_exasol = SpecialAgent(
    name = "exasol",
    topic = Topic.DATABASES,
    parameter_form = _valuespec_special_agent_exasol,
    title = Title("Exasol via XMLAPI"),
)
