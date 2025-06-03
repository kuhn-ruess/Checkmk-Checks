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
                        title = Title("Username"),
                        help_text = Help("User to connect via Auth Basic"),
                    ),
                    required = True,
                ),
                "username": DictElement(
                    parameter_form = String(
                        title = Title("Username"),
                        help_text = Help("User to connect via Auth Basic"),
                    ),
                    required = True,
                ),
                "password": DictElement(
                    parameter_form = Password(
                        title = Title("Password"),
                        help_text = Help("Password of the user"),
                    ),
                    required = True,
                ),
            }
        )
notification_parameter_registry.register(NotificationParameterSMSEagle)
