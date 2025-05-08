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
    DefaultValue,
    InputHint,
    Password,
)
from cmk.rulesets.v1.form_specs.validators import LengthInRange

from cmk.rulesets.v1.rule_specs import (
        SpecialAgent,
        Topic,
)


def _valuespec_special_agent_as400():
    """
    Service Metric Counter Special Agent Konfiguration
    """

    return Dictionary(
        title = Title("AS400 Agent"),
        help_text = Help("This rule activates special agent for AS400. Make sure to set the ODBC Drivers on your system"),
        elements = {
            "driver": DictElement(
                parameter_form = String(
                    title = Title("ODBC Driver"),
                    prefill = DefaultValue("{IBM i Access ODBC Driver}"),
                    help_text = Help("This value is based on your installed ODBC Driver"),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required = True,
            ),
            "system": DictElement(
                parameter_form = String(
                    title = Title("System Name"),
                    help_text = Help("Name of System"),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required = True,
            ),
            "uid": DictElement(
                parameter_form = String(
                    title = Title("User id"),
                    help_text = Help("User ID of Database User"),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required = True,
            ),
            "password": DictElement(
                parameter_form = Password(
                    title = Title("Password"),
                    help_text = Help("Password of user"),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required = True,
            ),
        },
    )


rule_spec_as400_agent = SpecialAgent(
    name = "as400_agent",
    topic = Topic.APPLICATIONS,
    parameter_form = _valuespec_special_agent_as400,
    title = Title("AS400 Agent"),
)
