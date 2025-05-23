#!/usr/bin/env python3

from cmk.gui.i18n import _
from cmk.gui.plugins.wato.utils import (
    notification_parameter_registry,
    NotificationParameter,
)
from cmk.gui.valuespec import (
    Age,
    Alternative,
    CascadingDropdown,
    DEF_VALUE,
    Dictionary,
    DropdownChoice,
    EmailAddress,
    FixedValue,
    HTTPUrl,
    Integer,
    IPv4Address,
    ListChoice,
    ListOfStrings,
    Password,
    TextAreaUnicode,
    TextInput,
    Transform,
    Tuple,
)

@notification_parameter_registry.register
class NotificationParameterRediscoverService(NotificationParameter):
    @property
    def ident(self) -> str:
        return "rediscover_service.py"

    @property
    def spec(self):
        return Dictionary(
            title=_("Create notification with the following parameters"),
            help=_("Parameters are used to connect to Checkmk site for using RestAPI."),
            optional_keys=["url_prefix", "proxy_url", "priority", "sound"],
            elements=[
                (
                    "proto",
                    DropdownChoice(
                        title=_("Protocol"),
                        help=_("Which protocol is used for connecting to Checkmk server"),
                        choices=[
                            ("http", _("HTTP")),
                            ("https", _("HTTPS")),
                        ]
                    ),
                ),
                (
                    "hostname",
                    TextInput(
                        title=_("Hostname"),
                        help=_("Give the Checkmk hostname, where the site is running on"),
                        size=40,
                        allow_empty=False,
                    ),
                ),
                (
                    "sitename",
                    TextInput(
                        title=_("Sitename"),
                        help=_("Enter the name of the Checkmk site"),
                        size=40,
                        allow_empty=False,
                    ),
                ),
            ],
        )
