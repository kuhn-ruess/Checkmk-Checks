#!/usr/bin/env python3
"""
APC NetBotz motion sensors - check parameters

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import DefaultValue, DictElement, Dictionary, ServiceState
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _parameter_form() -> Dictionary:
    return Dictionary(
        elements={
            "motion_detected": DictElement(
                parameter_form=ServiceState(
                    title=Title("State if motion is detected"),
                    help_text=Help(
                        "Motion in a room where people work is normal, so the default is OK. "
                        "Set WARN or CRIT for rooms that should be empty."
                    ),
                    prefill=DefaultValue(ServiceState.OK),
                ),
                required=True,
            ),
        },
    )


rule_spec_netbotz_motion = CheckParameters(
    name="netbotz_motion",
    title=Title("APC NetBotz motion sensors"),
    topic=Topic.ENVIRONMENTAL,
    parameter_form=_parameter_form,
    condition=HostAndItemCondition(item_title=Title("Motion sensor id")),
)
