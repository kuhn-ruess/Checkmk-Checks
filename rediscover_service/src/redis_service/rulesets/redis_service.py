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
    SingleChoice,
    SingleChoiceElement,
    DefaultValue,
    String,
)
from cmk.rulesets.v1.rule_specs import (
    NotificationParameters,
    Topic,
)


def _parameters_redis_service():
    return Dictionary(
        title = Title("Create notification with the following parameters"),
        help_text = Help("Parameters are used to connect to Checkmk site for using RestAPI."),
        elements = {
            "proto": DictElement(
                parameter_form = SingleChoice(
                    title = Title("Protocol"),
                    help_text = Help("Which protocol is used for connecting to Checkmk server"),
                    elements = [
                        SingleChoiceElement(
                            name = "http",
                            title=Title("HTTP")
                        ),
                        SingleChoiceElement(
                            name="https",
                            title=Title("HTTPS")
                        ),
                    ],
                    prefill = DefaultValue("http"),
                ),
                required = True,
            ),
            "hostname": DictElement(
                parameter_form = String(
                    title = Title("Hostname"),
                    help_text = Help("Give the Checkmk hostname, where the site is running on"),
                    field_size = 40,
                ),
                required = True,
            ),
            "sitename": DictElement(
                parameter_form = String(
                    title = Title("Sitename"),
                    help_text = Help("Enter the name of the Checkmk site"),
                    field_size=40,
                ),
                required = True,
            ),
        },
    )

rule_spec_redis_service = NotificationParameters(
    title = Title("Rediscover service"),
    topic = Topic.OPERATING_SYSTEM,
    parameter_form = _parameters_redis_service,
    name = "rediscover_service",
)
