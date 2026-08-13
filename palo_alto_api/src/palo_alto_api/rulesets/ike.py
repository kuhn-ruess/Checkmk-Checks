#!/usr/bin/env python3
"""
Palo Alto XML API - IKE gateway check ruleset

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import DefaultValue, DictElement, Dictionary, ServiceState
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _parameter_form():
    return Dictionary(
        title=Title("Palo Alto IKE gateway"),
        elements={
            "state_not_established": DictElement(
                parameter_form=ServiceState(
                    title=Title("State when IKE SA is not established"),
                    help_text=Help(
                        "Monitoring state to report when an IKE gateway has no "
                        "established security association."
                    ),
                    prefill=DefaultValue(ServiceState.WARN),
                ),
                required=True,
            ),
        },
    )


rule_spec_palo_alto_api_ike = CheckParameters(
    name="palo_alto_api_ike",
    topic=Topic.NETWORKING,
    parameter_form=_parameter_form,
    title=Title("Palo Alto IKE gateway"),
    condition=HostAndItemCondition(item_title=Title("Gateway")),
)
