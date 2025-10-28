from typing import cast # type: ignore
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

class NotificationParameterSMSEagle(NotificationParameter):
    """
    Notification parameter for SMS Eagle Configuration
    """
    @property
    def ident(self) -> str:
        return "sms_eagle"

    @property
    def spec(self) -> ValueSpecDictionary:
        # TODO needed because of mixed Form Spec and old style setup
        return cast(ValueSpecDictionary, recompose(self._form_spec()).valuespec)

    def _form_spec(self):
        return Dictionary(
            title=Title("SMS Eagle SMS Appliance"),
            elements={
                "api_host": DictElement(
                    parameter_form = String(
                        title = Title("API Host"),
                        help_text = Help("Address of EAGLE API"),
                    ),
                    required = True,
                ),
                "api_token": DictElement(
                    parameter_form = Password(
                        title = Title("API Token"),
                        help_text = Help("API Access Token"),
                    ),
                    required = True,
                ),
                "svc_label": DictElement(
                    parameter_form = String(
                        title=Title("Show matching Service Label"),
                        help_text = Help("Enter Key for the Service Label which you want to show in the sms"),
                    ),
                ),
                "host_label": DictElement(
                    parameter_form = String(
                        title = Title("Show matching Host Label"),
                        help_text = Help("Enter Key for the Host Label which you want to show in the sms"),
                    ),
                ),
            }
        )
notification_parameter_registry.register(NotificationParameterSMSEagle)
