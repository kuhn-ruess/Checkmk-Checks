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
    String,
    Password,
)
from cmk.rulesets.v1.form_specs.validators import LengthInRange
from cmk.rulesets.v1.rule_specs import (
    NotificationParameters,
    Topic,
)


def _parameters_cherwell_notify():
    return Dictionary(
        title = Title("Create notification with followingen parameters"),
        elements = {
            "api_url": DictElement(
                parameter_form = String(
                    title = Title("API URL"),
                    help_text = Help("Full API URL"),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required = True,
            ),
            "token_url": DictElement(
                parameter_form = String(
                    title = Title("Token API URL"),
                    help_text = Help("Full Token API URL"),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required = True,
            ),
            "client_id": DictElement(
                parameter_form = String(
                    title = Title("Client ID"),
                    help_text = Help("Client ID for Authentication"),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required = True,
            ),
            "username": DictElement(
                parameter_form = String(
                    title = Title("Username"),
                    help_text = Help("Username for Authentication"),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required = True,
            ),
            "password": DictElement(
                parameter_form = Password(
                    title = Title("Auth Password"),
                    help_text = Help("Password for Authentication"),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required = True,
            ),
            "automation_secret": DictElement(
                parameter_form = Password(
                    title = Title("Automation Secret of Checkmk"),
                    help_text = Help("Used for the API Call"),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required = True,
            ),
            "cmk_server": DictElement(
                parameter_form = String(
                    title = Title("Checkmk Server"),
                    help_text = Help("Server Address of Checkmk Server"),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required = True,
            ),
            "cmk_site": DictElement(
                parameter_form = String(
                    title = Title("Checkmk Site"),
                    help_text = Help("Checkmk Site Name"),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required = True,
            ),
        },
    )

rule_spec_cherwell_notify = NotificationParameters(
    title = Title("Cherwell notify"),
    topic = Topic.OPERATING_SYSTEM,
    parameter_form = _parameters_cherwell_notify,
    name = "cherwell_notify",
)
