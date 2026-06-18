#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

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
)
from cmk.rulesets.v1.rule_specs import (
    NotificationParameters,
    Topic,
)


def _parameters_service_now_notify():
    return Dictionary(
        title=Title("ServiceNow Notify"),
        help_text=Help("Configure ServiceNow incident creation via API"),
        elements={
            "api_url": DictElement(
                parameter_form=String(
                    title=Title("API URL"),
                    help_text=Help("URL to the ServiceNow API"),
                ),
                required=True,
            ),
            "api_user": DictElement(
                parameter_form=String(
                    title=Title("Auth User"),
                    help_text=Help("User for Authentication"),
                ),
                required=True,
            ),
            "api_password": DictElement(
                parameter_form=Password(
                    title=Title("Auth Password"),
                    help_text=Help("Password for Authentication"),
                ),
                required=True,
            ),
            "proxy": DictElement(
                parameter_form=String(
                    title=Title("Proxy"),
                    help_text=Help("Proxy to be used (optional)"),
                ),
                required=False,
            ),
        },
    )


rule_spec_service_now_notify = NotificationParameters(
    title=Title("Service Now Notify"),
    topic=Topic.NOTIFICATIONS,
    parameter_form=_parameters_service_now_notify,
    name="service_now_notify",
)
