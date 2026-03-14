#!/usr/bin/env python3

"""
Azure Extra Special Agent Ruleset
"""

from cmk.rulesets.v1 import Title, Help
from cmk.rulesets.v1.form_specs import (
    Dictionary,
    DictElement,
    String,
    Password,
)
from cmk.rulesets.v1.form_specs.validators import LengthInRange

from cmk.rulesets.v1.rule_specs import (
    SpecialAgent,
    Topic,
)


def _valuespec_special_agent_azure_extra():
    """
    Special Agent Konfiguration für Azure Extra
    """

    return Dictionary(
        title=Title("Azure Extra"),
        help_text=Help("This rule activates a special agent for Azure Extra monitoring"),
        elements={
            "tenant_id": DictElement(
                parameter_form=String(
                    title=Title("Tenant ID"),
                    help_text=Help("Azure Active Directory Tenant ID"),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required=True,
            ),
            "client_id": DictElement(
                parameter_form=String(
                    title=Title("Client ID"),
                    help_text=Help("Azure Application Client ID"),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required=True,
            ),
            "client_secret": DictElement(
                parameter_form=Password(
                    title=Title("Client Secret"),
                    help_text=Help("Azure Application Client Secret"),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required=True,
            ),
            "subscription_id": DictElement(
                parameter_form=String(
                    title=Title("Subscription ID"),
                    help_text=Help("Azure Subscription ID"),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required=True,
            ),
            "proxy_url": DictElement(
                parameter_form=String(
                    title=Title("Proxy URL"),
                    help_text=Help("Proxy server URL to use for HTTP(S) requests (e.g., http://proxy.example.com:8080)"),
                ),
                required=False,
            ),
        },
    )


rule_spec_azure_extra = SpecialAgent(
    name="azure_extra",
    topic=Topic.CLOUD,
    parameter_form=_valuespec_special_agent_azure_extra,
    title=Title("KR Azure Extra"),
)