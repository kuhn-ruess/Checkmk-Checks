#!/usr/bin/env python3
"""
Aruba Central - access point status ruleset

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import DefaultValue, DictElement, Dictionary, ServiceState
from cmk.rulesets.v1.rule_specs import CheckParameters, HostCondition, Topic


def _parameter_form():
    return Dictionary(
        title=Title("Aruba access point status"),
        elements={
            "state_down": DictElement(
                parameter_form=ServiceState(
                    title=Title("State when the access point is down"),
                    help_text=Help(
                        "Aruba Central reports an access point as down when it has "
                        "lost its connection to the cloud."
                    ),
                    prefill=DefaultValue(ServiceState.CRIT),
                ),
                required=True,
            ),
            "state_other": DictElement(
                parameter_form=ServiceState(
                    title=Title("State for any other status"),
                    help_text=Help(
                        "Covers states such as a sleeping access point or a value "
                        "Aruba Central introduces later on."
                    ),
                    prefill=DefaultValue(ServiceState.WARN),
                ),
                required=True,
            ),
        },
    )


rule_spec_aruba_ap = CheckParameters(
    name="aruba_ap",
    topic=Topic.NETWORKING,
    parameter_form=_parameter_form,
    title=Title("Aruba access point status"),
    condition=HostCondition(),
)
