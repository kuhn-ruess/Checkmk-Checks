#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.gui.i18n import _
from cmk.gui.plugins.wato.utils import (
    notification_parameter_registry,
    NotificationParameter,
)
from cmk.gui.valuespec import (
    Dictionary,
    TextAscii,
    Password,
)

@notification_parameter_registry.register
class NotificationParameterCherwell(NotificationParameter):
    @property
    def ident(self) -> str:
        return "cherwell_notify.py"


    @property
    def spec(self):
        return Dictionary(
            title = _("Create notification with followingen parameters"),
            optional_keys = [],
            elements = [
                (
                    "api_url",
                    TextAscii(
                        title = _("API URL"),
                        help = _("Full API URL"),
                        allow_empty = False,
                    ),
                ),
                (
                    "token_url",
                    TextAscii(
                        title = _("Token API URL"),
                        help = _("Full Token API URL"),
                        allow_empty = False,
                    ),
                ),
                (
                    "client_id",
                    TextAscii(
                        title = _("Client ID"),
                        help = _("Client ID for Authentication"),
                        allow_empty = False,
                    ),
                ),
                (
                    "username",
                    TextAscii(
                        title = _("Username"),
                        help = _("Username for Authentication"),
                        allow_empty = False,
                    ),
                ),
                (
                    "password",
                    Password(
                        title = _("Auth Password"),
                        help = _("Password for Authentication"),
                        allow_empty = False,
                    ),
                ),
                (
                    "automation_secret",
                    Password(
                        title = _("Automation Secret of Checkmk"),
                        help = _("Used for the API Call"),
                        allow_empty = False,
                    ),
                ),
                (
                    "cmk_server",
                    TextAscii(
                        title = _("Checkmk Server"),
                        help = _("Server Address of Checkmk Server"),
                        allow_empty = False,
                    ),
                ),
                (
                    "cmk_site",
                    TextAscii(
                        title = _("Checkmk Site"),
                        help = _("Checkmk Site Name"),
                        allow_empty = False,
                    ),
                ),
            ],
        )
