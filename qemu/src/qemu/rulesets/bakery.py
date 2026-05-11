#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
"""Agent bakery rule for the qemu plugin."""
from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    CascadingSingleChoice,
    CascadingSingleChoiceElement,
    DefaultValue,
    DictElement,
    Dictionary,
    FixedValue,
)
from cmk.rulesets.v1.rule_specs import AgentConfig, Topic


def _parameter_form_bakery() -> Dictionary:
    return Dictionary(
        help_text=Help(
            "The plugin 'qemu' allows monitoring of KVM and QEMU virtual machines "
            "via libvirt's virsh on Linux hosts."
        ),
        elements={
            "deployment": DictElement(
                required=True,
                parameter_form=CascadingSingleChoice(
                    title=Title("Deployment"),
                    elements=(
                        CascadingSingleChoiceElement(
                            name="deploy",
                            title=Title("Deploy the plug-in"),
                            parameter_form=FixedValue(value=None),
                        ),
                        CascadingSingleChoiceElement(
                            name="do_not_deploy",
                            title=Title("Do not deploy the plug-in"),
                            parameter_form=FixedValue(value=None),
                        ),
                    ),
                    prefill=DefaultValue("deploy"),
                ),
            ),
        },
    )


rule_spec_qemu_bakery = AgentConfig(
    name="qemu",
    title=Title("QEMU / KVM Monitoring (Linux)"),
    topic=Topic.APPLICATIONS,
    parameter_form=_parameter_form_bakery,
)
