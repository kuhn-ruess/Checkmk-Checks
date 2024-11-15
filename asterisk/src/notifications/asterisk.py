#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.gui.i18n import _
from cmk.gui.plugins.wato.utils import (
    NotificationParameter,
    IndividualOrStoredPassword,
    notification_parameter_registry,
)
from cmk.gui.valuespec import (
    Dictionary,
    TextInput,
    Integer,
)


@notification_parameter_registry.register
class NotificationParamterAsterisk(NotificationParameter):
    @property
    def ident(self) -> str:
        return "asterisk"

    @property
    def spec(self) -> Dictionary:
        return Dictionary(
            title=_("Create notification with the following parameters"),
            optional_keys=[],
            elements=[
                (
                    "host",
                    TextInput(
                        title=_("Asterisk Server IP"),
                        help=_("Please specify Asterisk server IP."),
                        allow_empty=False,
                    ),
                ),
                (
                    "port",
                    Integer(
                        title=_("Port of AMI API"),
                        help=_("Please specify port of AMI API."),
                        default_value=5038,
                    ),
                ),
                (
                    "timeout",
                    Integer(
                        title=_("Timeout for calling"),
                        help=_("Please specify timeout for call. It must be higher than call time"),
                        default_value=180,
                    ),
                ),
                (
                    "username",
                    TextInput(
                        title=_("Username"),
                        help=_("The user, used for login, has to have at least the call, command and originate"),
                        allow_empty=False,
                    ),
                ),
                (
                    "password",
                    IndividualOrStoredPassword(
                        title=_("Password of the user"),
                        allow_empty=False,
                    ),
                ),
                (
                    "channel",
                    TextInput(
                        title=_("Channel used for calling"),
                        help=_("Please specify the channel, which should be used for calling"),
                        allow_empty=False,
                    ),
                ),
                (
                    "exten",
                    TextInput(
                        title=_("Extension used for calling"),
                        help=_("Please specify th exten, which should be used for calling"),
                        allow_empty=False,
                    ),
                ),
                (
                    "priority",
                    Integer(
                        title=_("Priority used for calling"),
                        help=_("Please specify the priority, which should be used for calling"),
                        default_value=1,
                    ),
                ),
                (
                    "context",
                    TextInput(
                        title=_("Context used for calling"),
                        help=_("Please specify the contect, which should be used for calling"),
                        allow_empty=False,
                    ),
                ),
                (
                    "callerid",
                    TextInput(
                        title=_("Caller ID used for calling"),
                        help=_("Please specify the caller ID, which should be used for calling"),
                        allow_empty=False,
                    ),
                ),

            ],
        )
