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
    Integer,
    DefaultValue,
)
from cmk.rulesets.v1.form_specs.validators import LengthInRange
from cmk.rulesets.v1.rule_specs import (
    NotificationParameters,
    Topic,
)


def _parameters_asterisk():
    return Dictionary(
        title=Title("Create notification with the following parameters"),
        elements={
            "host": DictElement(
                parameter_form=String(
                    title=Title("Asterisk Server IP"),
                    help_text=Help("Please specify Asterisk server IP."),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required=True,
            ),
            "port": DictElement(
                parameter_form=Integer(
                    title=Title("Port of AMI API"),
                    help_text=Help("Please specify port of AMI API."),
                    prefill=DefaultValue(5038),
                ),
                required=True,
            ),
            "timeout": DictElement(
                parameter_form=Integer(
                    title=Title("Timeout for calling"),
                    help_text=Help("Please specify timeout for call. It must be higher than call time"),
                    prefill=DefaultValue(180),
                ),
                required=True,
            ),
            "username": DictElement(
                parameter_form=String(
                    title=Title("Username"),
                    help_text=Help("The user, used for login, has to have at least the call, command and originate"),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required=True,
            ),
            "password": DictElement(
                parameter_form=Password(
                    title=Title("Password of the user"),
                ),
                required=True,
            ),
            "channel": DictElement(
                parameter_form=String(
                    title=Title("Channel used for calling"),
                    help_text=Help("Please specify the channel, which should be used for calling"),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required=True,
            ),
            "exten": DictElement(
                parameter_form=String(
                    title=Title("Extension used for calling"),
                    help_text=Help("Please specify th exten, which should be used for calling"),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required=True,
            ),
            "priority": DictElement(
                parameter_form=Integer(
                    title=Title("Priority used for calling"),
                    help_text=Help("Please specify the priority, which should be used for calling"),
                    prefill=DefaultValue(1),
                ),
                required=True,
            ),
            "context": DictElement(
                parameter_form=String(
                    title=Title("Context used for calling"),
                    help_text=Help("Please specify the contect, which should be used for calling"),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required=True,
            ),
            "callerid": DictElement(
                parameter_form=String(
                    title=Title("Caller ID used for calling"),
                    help_text=Help("Please specify the caller ID, which should be used for calling"),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required=True,
            ),
        },
    )


rule_spec_asterisk = NotificationParameters(
    title=Title("Asterisk notification"),
    topic=Topic.NOTIFICATIONS,
    parameter_form=_parameters_asterisk,
    name="asterisk",
)
