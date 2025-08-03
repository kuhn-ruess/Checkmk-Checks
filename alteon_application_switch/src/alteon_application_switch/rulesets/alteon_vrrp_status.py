#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    String,
    SingleChoice,
    SingleChoiceElement,
    migrate_to_password,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _parameter_valuespec_alteon_vrrp_status():
    return Dictionary(
        elements={
            "inventory_alteon_vrrp_state": DictElement(
                parameter_form=SingleChoice(
                    title=Title("Desired State for Cluster Status in this context"),
                    help_text=Help("The Virtual Interfaces must provide the configured state, otherwise the check is warning. Configure the desired state of all Instances in WATO using regex. If the cluster is switched, change the WATO config accordingly."),
                    elements=[
                        SingleChoiceElement(name="init", title=Title("Init")),
                        SingleChoiceElement(name="master", title=Title("Master")),
                        SingleChoiceElement(name="backup", title=Title("Backup")),
                        SingleChoiceElement(name="holdoff", title=Title("Holdoff")),
                    ],
                ),
                required=True,
            ),
        }
    )


rule_spec_alteon_vrrp_status = CheckParameters(
    name="alteon_global",
    topic=Topic.APPLICATIONS,
    condition=HostAndItemCondition(
        item_title=Title("Item"),
        item_form=String(),
    ),
    parameter_form=_parameter_valuespec_alteon_vrrp_status,
    title=Title("Alteon VRRP Status"),
)
