#!/usr/bin/env python3
"""
Palo Alto XML API - IPSec tunnel check ruleset

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import DefaultValue, DictElement, Dictionary, ServiceState
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _parameter_form():
    return Dictionary(
        title=Title("Palo Alto IPSec tunnel"),
        elements={
            "state_not_active": DictElement(
                parameter_form=ServiceState(
                    title=Title("State when tunnel is not active"),
                    help_text=Help(
                        "Monitoring state to report when an IPSec tunnel is in "
                        "any state other than 'active'."
                    ),
                    prefill=DefaultValue(ServiceState.CRIT),
                ),
                required=True,
            ),
        },
    )


rule_spec_palo_alto_api_ipsec = CheckParameters(
    name="palo_alto_api_ipsec",
    topic=Topic.NETWORKING,
    parameter_form=_parameter_form,
    title=Title("Palo Alto IPSec tunnel"),
    condition=HostAndItemCondition(item_title=Title("Tunnel")),
)
