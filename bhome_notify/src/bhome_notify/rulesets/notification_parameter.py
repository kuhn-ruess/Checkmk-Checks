from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DictElement,
    Dictionary,
    String,
    Password,
)
from cmk.rulesets.v1.rule_specs import NotificationParameters, Topic


def _form_spec_bhome() -> Dictionary:
    return Dictionary(
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


rule_spec_bhome_notify = NotificationParameters(
    name="bhome_notify",
    title=Title("BHome Events API"),
    topic=Topic.NOTIFICATIONS,
    parameter_form=_form_spec_bhome,
)
