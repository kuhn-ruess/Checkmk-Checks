#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
https://kuhn-ruess.de
"""

from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    Dictionary,
    DictElement,
    SingleChoice,
    SingleChoiceElement,
    String,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _formspec_catalyst_switch_state():
    return Dictionary(
        elements={
            "switch_role": DictElement(
                required=False,
                parameter_form=SingleChoice(
                    title=Title("Expected switch role"),
                    help_text=Help(
                        "If set, the service goes CRIT when the device reports a "
                        "different role than the one selected here."
                    ),
                    elements=[
                        SingleChoiceElement(name="master", title=Title("master")),
                        SingleChoiceElement(name="member", title=Title("member")),
                        SingleChoiceElement(name="not_member", title=Title("not member")),
                        SingleChoiceElement(name="standby", title=Title("standby")),
                    ],
                ),
            ),
        },
    )


rule_spec_catalyst_switch_state = CheckParameters(
    name="catalyst_switch_state",
    topic=Topic.NETWORKING,
    condition=HostAndItemCondition(
        item_title=Title("Switch number"),
        item_form=String(),
    ),
    parameter_form=_formspec_catalyst_switch_state,
    title=Title("Catalyst Switch State"),
)
