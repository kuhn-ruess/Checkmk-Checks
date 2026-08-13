#!/usr/bin/env python3
"""
Palo Alto XML API - High availability check ruleset

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import DefaultValue, DictElement, Dictionary, ServiceState
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _parameter_form():
    return Dictionary(
        title=Title("Palo Alto high availability"),
        elements={
            "state_local_unhealthy": DictElement(
                parameter_form=ServiceState(
                    title=Title("State when local HA state is not active/passive"),
                    prefill=DefaultValue(ServiceState.CRIT),
                ),
                required=True,
            ),
            "state_not_synced": DictElement(
                parameter_form=ServiceState(
                    title=Title("State when the configuration is not synchronized"),
                    prefill=DefaultValue(ServiceState.WARN),
                ),
                required=True,
            ),
            "state_link_down": DictElement(
                parameter_form=ServiceState(
                    title=Title("State when an HA link is not up"),
                    help_text=Help("Applies to the 'Palo Alto HA Link ...' services."),
                    prefill=DefaultValue(ServiceState.CRIT),
                ),
                required=True,
            ),
        },
    )


rule_spec_palo_alto_api_ha = CheckParameters(
    name="palo_alto_api_ha",
    topic=Topic.NETWORKING,
    parameter_form=_parameter_form,
    title=Title("Palo Alto high availability"),
    condition=HostAndItemCondition(item_title=Title("HA component")),
)
