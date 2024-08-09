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
            optional_keys=["url_prefix", "proxy_url", "priority", "sound"],
            elements=[
                (
                    "proto",
                    DropdownChoice(
                        title=_("Protocol"),
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
                        size=40,
                        allow_empty=False,
                    ),
                ),
                (
                    "sitename",
                    TextInput(
                        title=_("Sitename"),
                        size=40,
                        allow_empty=False,
                    ),
                ),
            ],
        )
