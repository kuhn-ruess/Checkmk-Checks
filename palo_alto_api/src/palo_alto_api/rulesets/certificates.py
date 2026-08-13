#!/usr/bin/env python3
"""
Palo Alto XML API - Certificate check ruleset

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import DefaultValue, DictElement, Dictionary, Integer
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _parameter_form():
    return Dictionary(
        title=Title("Palo Alto certificate expiry"),
        elements={
            "warn_days": DictElement(
                parameter_form=Integer(
                    title=Title("Warning threshold (days)"),
                    help_text=Help("Warn if a certificate expires within this many days"),
                    prefill=DefaultValue(30),
                ),
                required=True,
            ),
            "crit_days": DictElement(
                parameter_form=Integer(
                    title=Title("Critical threshold (days)"),
                    help_text=Help("Critical if a certificate expires within this many days"),
                    prefill=DefaultValue(14),
                ),
                required=True,
            ),
        },
    )


rule_spec_palo_alto_api_certificates = CheckParameters(
    name="palo_alto_api_certificates",
    topic=Topic.NETWORKING,
    parameter_form=_parameter_form,
    title=Title("Palo Alto certificate expiry"),
    condition=HostAndItemCondition(item_title=Title("Certificate")),
)
