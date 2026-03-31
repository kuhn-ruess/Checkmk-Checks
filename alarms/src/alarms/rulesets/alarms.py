#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from typing import cast

from cmk.gui.form_specs.vue.visitors.recomposers.unknown_form_spec import recompose
from cmk.gui.valuespec import Dictionary as ValueSpecDictionary
from cmk.gui.watolib.notification_parameter import notification_parameter_registry, NotificationParameter

from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    Dictionary,
    DictElement,
    SingleChoice,
    SingleChoiceElement,
    DefaultValue,
    String,
)


class NotificationParameterAlarms(NotificationParameter):
    @property
    def ident(self) -> str:
        return "alarms"

    @property
    def spec(self) -> ValueSpecDictionary:
        return cast(ValueSpecDictionary, recompose(self._form_spec()).valuespec)

    def _form_spec(self) -> Dictionary:
        return Dictionary(
            title = Title("Play alarms (using API)"),
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


notification_parameter_registry.register(NotificationParameterAlarms)
