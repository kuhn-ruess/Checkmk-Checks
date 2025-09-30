# 2021 created by Sven Rueß, sritd.de

from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import Dictionary, DictElement, String, BooleanChoice, DefaultValue, Password, migrate_to_password
from cmk.rulesets.v1.rule_specs import SpecialAgent, Topic, Help


def _formspec():
    return Dictionary(
        title=Title("Cohesity via WebAPI"),
        help_text=Help("This rule set selects the special agent for Cohesity"),
        elements = {
            "user": DictElement(
                required=True,
                parameter_form=String(
                    title=Title("Username"),
                ),
            ),
            "password": DictElement(
                required=True,
                parameter_form=Password(
                    title=Title("Password for this user"),
                    migrate=migrate_to_password,
                ),
            ),
            "domain": DictElement(
                required=True,
                parameter_form=String(
                    title=Title("Domain"),
                    prefill=DefaultValue("LOCAL"),
                ),
            ),
            "verify_cert": DictElement(
                required=True,
                parameter_form=BooleanChoice(
                    title=Title("Verify SSL Certificate"),
                    prefill=DefaultValue(True),
                ),
            ),
        },
    )


rule_spec_cohesity = SpecialAgent(
    topic=Topic.STORAGE,
    name="cohesity",
    title=Title("Cohesity via WebAPI"),
    help_text=Help(
        "Collects information from Cohesity via the WebAPI. "
        "Configure connection parameters here."
    ),
    parameter_form=_formspec
)

