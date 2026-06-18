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
    String,
    Password,
    MultilineText,
)
from cmk.rulesets.v1.form_specs.validators import LengthInRange
from cmk.rulesets.v1.rule_specs import (
    NotificationParameters,
    Topic,
)


def _parameters_kentix():
    return Dictionary(
        title=Title("Create notification with the following parameters"),
        elements={
            "ipaddress": DictElement(
                parameter_form=String(
                    title=Title("IP address of the AlarmManager"),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required=True,
            ),
            "password": DictElement(
                parameter_form=Password(
                    title=Title("SMS gateway password"),
                ),
                required=True,
            ),
            "template_text": DictElement(
                parameter_form=MultilineText(
                    title=Title("Message content"),
                ),
                required=True,
            ),
        },
    )


rule_spec_kentix = NotificationParameters(
    title=Title("Kentix SMS Gateway notification"),
    topic=Topic.NOTIFICATIONS,
    parameter_form=_parameters_kentix,
    name="kentix",
)
