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


def _parameters_alarms():
    return Dictionary(
        title = Title("Create notification with the following parameters"),
        help_text = Help("Parameters are used to connect to API to play alarms."),
        elements = {
            "proto": DictElement(
                parameter_form = SingleChoice(
                    title = Title("Protocol"),
                    help_text = Help("Which protocol is used for connecting to API"),
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
                    help_text = Help("Give the hostname, where the API is running on"),
                    field_size = 40,
                    prefill = DefaultValue("localhost"),
                ),
                required = True,
            ),
            "url": DictElement(
                parameter_form = String(
                    title = Title("URL"),
                    help_text = Help("Enter the URI of the API"),
                    field_size=40,
                    prefill = DefaultValue("api.php"),
                ),
                required = True,
            ),
            "alarm": DictElement(
                parameter_form = SingleChoice(
                    title = Title("Alarm"),
                    help_text = Help("Which alarm should be played"),
                    elements = [
                        SingleChoiceElement(
                            name = "alarm1",
                            title=Title("Alarm 1")
                        ),
                        SingleChoiceElement(
                            name="alarm2",
                            title=Title("Alarm 2")
                        ),
                        SingleChoiceElement(
                            name="alarm3",
                            title=Title("Alarm 3")
                        ),
                        SingleChoiceElement(
                            name="alarm4",
                            title=Title("Alarm 4")
                        ),
                        SingleChoiceElement(
                            name="horse",
                            title=Title("Horse")
                        ),
                    ],
                    prefill = DefaultValue("alarm1"),
                ),
                required = True,
            ),
        },
    )

rule_spec_alarms = NotificationParameters(
    title = Title("Play alarms"),
    topic = Topic.OPERATING_SYSTEM,
    parameter_form = _parameters_alarms,
    name = "alarms",
)
