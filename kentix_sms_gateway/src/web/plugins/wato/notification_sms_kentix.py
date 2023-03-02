#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from cmk.gui.valuespec import (
    IPv4Address,
    TextAreaUnicode,
)

from cmk.gui.plugins.wato.utils import (
    IndividualOrStoredPassword,
    notification_parameter_registry,
    NotificationParameter,
)

@notification_parameter_registry.register
class NotificationParameterKentix(NotificationParameter):

    @property
    def ident(self):
        return "kentix"

    @property
    def spec(self):
        return Dictionary(
            title=_("Create notification with the following parameters"),
            elements=self._parameter_elements,
            optional_keys=[],
        )
    
    def _parameter_elements(self):
        return self._api_params + self._notification_params + self._bulk_params

    @property
    def _api_params(self):
        return [
            ( "ipaddress",
                IPv4Address(
                    title=_("IP address of the AlarmManager"),
                )
            ),
            ( "password",
                IndividualOrStoredPassword(
                    title=_("SMS gateway password")
                )
            ),
            ( "template_text",
                TextAreaUnicode(
                    title=_("Message content"),
                )
            ),
        ]

    @property
    def _notification_params(self):
        return []

    @property
    def _bulk_params(self):
        return []
