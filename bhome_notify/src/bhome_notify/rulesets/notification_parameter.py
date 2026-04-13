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


class NotificationParameterBHome(NotificationParameter):
    @property
    def ident(self) -> str:
        return "bhome_notify"

    @property
    def spec(self) -> ValueSpecDictionary:
        return cast(ValueSpecDictionary, recompose(self._form_spec()).valuespec)

    def _form_spec(self):
        return Dictionary(
            title=Title("BHome Events API"),
            elements={
                "portal_domain": DictElement(
                    parameter_form=String(
                        title=Title("Portal Domain"),
                        help_text=Help("Domain of the BHome events portal (without https://)"),
                    ),
                    required=True,
                ),
                "id": DictElement(
                    parameter_form=String(
                        title=Title("Client ID"),
                        help_text=Help("Client ID for authentication"),
                    ),
                    required=True,
                ),
                "access": DictElement(
                    parameter_form=Password(
                        title=Title("Access Key"),
                        help_text=Help("Access key for authentication"),
                    ),
                    required=True,
                ),
                "secret": DictElement(
                    parameter_form=Password(
                        title=Title("Secret"),
                        help_text=Help("Secret for authentication"),
                    ),
                    required=True,
                ),
            }
        )


notification_parameter_registry.register(NotificationParameterBHome)
