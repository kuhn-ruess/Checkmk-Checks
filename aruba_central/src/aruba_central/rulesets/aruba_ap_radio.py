#!/usr/bin/env python3
"""
Aruba Central - access point radio ruleset

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    LevelDirection,
    Percentage,
    ServiceState,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _parameter_form():
    return Dictionary(
        title=Title("Aruba access point radios"),
        elements={
            "state_down": DictElement(
                parameter_form=ServiceState(
                    title=Title("State when the radio is down"),
                    help_text=Help(
                        "A radio can be down because it is administratively "
                        "disabled, which is why this is a warning by default."
                    ),
                    prefill=DefaultValue(ServiceState.WARN),
                ),
                required=True,
            ),
            "state_other": DictElement(
                parameter_form=ServiceState(
                    title=Title("State for any other status"),
                    prefill=DefaultValue(ServiceState.WARN),
                ),
                required=True,
            ),
            "levels_utilization": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Levels on the channel utilization"),
                    help_text=Help(
                        "How busy the radio channel is. High utilization on the "
                        "2.4 GHz band is common in dense environments, so it can "
                        "make sense to set different levels per radio."
                    ),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Percentage(),
                    prefill_fixed_levels=DefaultValue((80.0, 90.0)),
                ),
                required=True,
            ),
        },
    )


rule_spec_aruba_ap_radio = CheckParameters(
    name="aruba_ap_radio",
    topic=Topic.NETWORKING,
    parameter_form=_parameter_form,
    title=Title("Aruba access point radios"),
    condition=HostAndItemCondition(item_title=Title("Radio")),
)
