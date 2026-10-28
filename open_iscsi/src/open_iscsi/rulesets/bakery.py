#!/usr/bin/env python3
"""
Open-iSCSI: agent plug-in deployment

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    CascadingSingleChoice,
    CascadingSingleChoiceElement,
    DefaultValue,
    DictElement,
    Dictionary,
    FixedValue,
    TimeMagnitude,
    TimeSpan,
)
from cmk.rulesets.v1.rule_specs import AgentConfig, Topic


def _agent_config_open_iscsi() -> Dictionary:
    return Dictionary(
        help_text=Help(
            "Deploys the agent plug-in <tt>open-iscsi</tt> for Linux hosts with "
            "<tt>iscsiadm</tt>. It reports the active iSCSI sessions, their statistics "
            "and the host statistics of iSOE adapters."
        ),
        elements={
            "deployment": DictElement(
                required=True,
                parameter_form=CascadingSingleChoice(
                    title=Title("Deployment type"),
                    elements=(
                        CascadingSingleChoiceElement(
                            name="sync",
                            title=Title("Deploy the plug-in and run it synchronously"),
                            parameter_form=FixedValue(value=None),
                        ),
                        CascadingSingleChoiceElement(
                            name="cached",
                            title=Title("Deploy the plug-in and run it asynchronously"),
                            parameter_form=TimeSpan(
                                displayed_magnitudes=(TimeMagnitude.HOUR, TimeMagnitude.MINUTE),
                                prefill=DefaultValue(300.0),
                            ),
                        ),
                        CascadingSingleChoiceElement(
                            name="do_not_deploy",
                            title=Title("Do not deploy the plug-in"),
                            parameter_form=FixedValue(value=None),
                        ),
                    ),
                    prefill=DefaultValue("sync"),
                ),
            ),
        },
    )


rule_spec_open_iscsi_bakery = AgentConfig(
    name="open_iscsi",
    title=Title("Open-iSCSI sessions (Linux)"),
    topic=Topic.STORAGE,
    parameter_form=_agent_config_open_iscsi,
)
