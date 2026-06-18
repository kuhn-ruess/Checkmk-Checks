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
    BooleanChoice,
    DefaultValue,
)
from cmk.rulesets.v1.rule_specs import (
    NotificationParameters,
    Topic,
)


def _parameters_sms_eagle():
    return Dictionary(
        title=Title("SMS Eagle SMS Appliance"),
        elements={
            "api_host": DictElement(
                parameter_form=String(
                    title=Title("API Host"),
                    help_text=Help("Address of EAGLE API"),
                ),
                required=True,
            ),
            "api_token": DictElement(
                parameter_form=Password(
                    title=Title("API Token"),
                    help_text=Help("API Access Token"),
                ),
                required=True,
            ),
            "svc_label": DictElement(
                parameter_form=String(
                    title=Title("Show matching Service Label"),
                    help_text=Help("Enter Key for the Service Label which you want to show in the sms"),
                ),
            ),
            "host_label": DictElement(
                parameter_form=String(
                    title=Title("Show matching Host Label"),
                    help_text=Help("Enter Key for the Host Label which you want to show in the sms"),
                ),
            ),
            "ssl_verify": DictElement(
                parameter_form=BooleanChoice(
                    title=Title("Verify SSL certificate"),
                    help_text=Help("Disable this only if the SMS Eagle appliance uses a self-signed or otherwise untrusted certificate."),
                    prefill=DefaultValue(True),
                ),
                required=False,
            ),
        },
    )


rule_spec_sms_eagle = NotificationParameters(
    title=Title("SMS Eagle SMS Appliance"),
    topic=Topic.NOTIFICATIONS,
    parameter_form=_parameters_sms_eagle,
    name="sms_eagle",
)
