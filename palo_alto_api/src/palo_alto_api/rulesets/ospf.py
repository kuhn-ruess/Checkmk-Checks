#!/usr/bin/env python3
"""
Palo Alto XML API - OSPF neighbor check ruleset

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import DefaultValue, DictElement, Dictionary, ServiceState
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _parameter_form():
    return Dictionary(
        title=Title("Palo Alto OSPF neighbor"),
        elements={
            "state_changed": DictElement(
                parameter_form=ServiceState(
                    title=Title("State when the neighbor state changed since discovery"),
                    help_text=Help(
                        "The neighbor state seen at discovery is stored as the target "
                        "state. As long as it stays the same (e.g. full or 2way), the "
                        "service is OK; this state applies once it changes. Re-run the "
                        "service discovery to accept a new state as target."
                    ),
                    prefill=DefaultValue(ServiceState.CRIT),
                ),
                required=True,
            ),
        },
    )


rule_spec_palo_alto_api_ospf = CheckParameters(
    name="palo_alto_api_ospf",
    topic=Topic.NETWORKING,
    parameter_form=_parameter_form,
    title=Title("Palo Alto OSPF neighbor"),
    condition=HostAndItemCondition(item_title=Title("Neighbor")),
)
