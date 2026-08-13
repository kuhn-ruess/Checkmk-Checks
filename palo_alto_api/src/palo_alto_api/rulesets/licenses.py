#!/usr/bin/env python3
"""
Palo Alto XML API - License check ruleset

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import DefaultValue, DictElement, Dictionary, Integer
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _parameter_form():
    return Dictionary(
        title=Title("Palo Alto license expiry"),
        elements={
            "warn_days": DictElement(
                parameter_form=Integer(
                    title=Title("Warning threshold (days)"),
                    help_text=Help("Warn if a license expires within this many days"),
                    prefill=DefaultValue(30),
                ),
                required=True,
            ),
            "crit_days": DictElement(
                parameter_form=Integer(
                    title=Title("Critical threshold (days)"),
                    help_text=Help("Critical if a license expires within this many days"),
                    prefill=DefaultValue(14),
                ),
                required=True,
            ),
        },
    )


rule_spec_palo_alto_api_licenses = CheckParameters(
    name="palo_alto_api_licenses",
    topic=Topic.NETWORKING,
    parameter_form=_parameter_form,
    title=Title("Palo Alto license expiry"),
    condition=HostAndItemCondition(item_title=Title("License")),
)
