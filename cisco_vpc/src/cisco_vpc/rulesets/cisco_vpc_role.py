#!/usr/bin/env python3

from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import (
    Dictionary,
    DictElement,
    SingleChoice,
    SingleChoiceElement,
)
from cmk.rulesets.v1.rule_specs import (
    CheckParameters,
    HostCondition,
    Topic,
)


ROLE_VALUE_MIGRATION = {
    "1": "primary_secondary",
    "2": "primary_primary",
    "3": "secondary_primary",
    "4": "secondary_secondary",
    "5": "no_peer_device",
}


def _migrate_cisco_vpc_role(value):
    if not isinstance(value, dict):
        return value

    switch_role = value.get("switch_role")
    if switch_role in ROLE_VALUE_MIGRATION:
        value = dict(value)
        value["switch_role"] = ROLE_VALUE_MIGRATION[switch_role]

    return value


def _parameter_valuespec_cisco_vpc_role():
    return Dictionary(
        migrate=_migrate_cisco_vpc_role,
        elements={
            "switch_role": DictElement(
                parameter_form=SingleChoice(
                    title=Title("Expected switch role"),
                    elements=[
                        SingleChoiceElement(name="primary_secondary", title=Title("primary, and operational secondary")),
                        SingleChoiceElement(name="primary_primary", title=Title("primary, and operational primary")),
                        SingleChoiceElement(name="secondary_primary", title=Title("secondary, and operational primary")),
                        SingleChoiceElement(name="secondary_secondary", title=Title("secondary, and operational secondary")),
                        SingleChoiceElement(name="no_peer_device", title=Title("no peer device")),
                    ],
                ),
            ),
        },
    )


rule_spec_cisco_vpc_role = CheckParameters(
    name="cisco_vpc_role",
    topic=Topic.NETWORKING,
    condition=HostCondition(),
    parameter_form=_parameter_valuespec_cisco_vpc_role,
    title=Title("Cisco VPC Role"),
)
