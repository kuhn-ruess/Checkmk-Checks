#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from typing import cast
from cmk.rulesets.v1 import Help, Title
from cmk.gui.valuespec import Dictionary as ValueSpecDictionary
from cmk.rulesets.v1.form_specs import (
    DictElement,
    Dictionary,
    String,
    Password,
)
from cmk.gui.form_specs.vue.visitors.recomposers.unknown_form_spec import recompose
from cmk.gui.watolib.notification_parameter import notification_parameter_registry, NotificationParameter


class NotificationParameterServiceNow(NotificationParameter):
    """
    Notification parameter for ServiceNow
    """
    @property
    def ident(self) -> str:
        return "service_now_notify"

    @property
    def spec(self) -> ValueSpecDictionary:
        # TODO needed because of mixed Form Spec and old style setup
        return cast(ValueSpecDictionary, recompose(self._form_spec()).valuespec)

    def _form_spec(self):
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
            }
        )


notification_parameter_registry.register(NotificationParameterServiceNow)
