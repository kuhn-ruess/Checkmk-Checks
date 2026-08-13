#!/usr/bin/env python3
"""
Palo Alto XML API - BGP peer check ruleset

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import DefaultValue, DictElement, Dictionary, ServiceState
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _parameter_form():
    return Dictionary(
        title=Title("Palo Alto BGP peer"),
        elements={
            "state_not_established": DictElement(
                parameter_form=ServiceState(
                    title=Title("State when the BGP peer is not established"),
                    prefill=DefaultValue(ServiceState.CRIT),
                ),
                required=True,
            ),
        },
    )


rule_spec_palo_alto_api_bgp = CheckParameters(
    name="palo_alto_api_bgp",
    topic=Topic.NETWORKING,
    parameter_form=_parameter_form,
    title=Title("Palo Alto BGP peer"),
    condition=HostAndItemCondition(item_title=Title("Peer")),
)
