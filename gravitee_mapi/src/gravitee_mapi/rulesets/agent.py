#!/usr/bin/env python3

"""
Gravitee MAPI Special Agent Ruleset

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.rulesets.v1 import Title, Help
from cmk.rulesets.v1.form_specs import (
    BooleanChoice,
    Dictionary,
    DictElement,
    Integer,
    Password,
    String,
)
from cmk.rulesets.v1.form_specs.validators import LengthInRange, NumberInRange
from cmk.rulesets.v1.rule_specs import SpecialAgent, Topic


def _valuespec_special_agent_gravitee_mapi():
    """
    Special Agent Konfiguration fuer Gravitee MAPI
    """
    return Dictionary(
        title=Title("Gravitee API Management"),
        help_text=Help(
            "This rule activates a special agent for Gravitee API Management monitoring. "
            "It monitors all APIs including response times, error rates and health availability."
        ),
        elements={
            "token": DictElement(
                parameter_form=Password(
                    title=Title("Bearer Token"),
                    help_text=Help("Bearer token for authentication against the Gravitee MAPI"),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required=True,
            ),
            "environment": DictElement(
                parameter_form=String(
                    title=Title("Environment"),
                    help_text=Help("Gravitee environment name (default: DEFAULT)"),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required=False,
            ),
            "interval": DictElement(
                parameter_form=Integer(
                    title=Title("Monitoring Interval (seconds)"),
                    help_text=Help(
                        "Time range in seconds used for analytics queries. "
                        "Should match the Checkmk check interval (default: 60)."
                    ),
                    custom_validate=(NumberInRange(min_value=10),),
                ),
                required=False,
            ),
            "no_verify_ssl": DictElement(
                parameter_form=BooleanChoice(
                    title=Title("Disable SSL verification"),
                    help_text=Help("Disable SSL certificate verification (not recommended)"),
                ),
                required=False,
            ),
        },
    )


rule_spec_gravitee_mapi = SpecialAgent(
    name="gravitee_mapi",
    topic=Topic.APPLICATIONS,
    parameter_form=_valuespec_special_agent_gravitee_mapi,
    title=Title("Gravitee API Management"),
)
