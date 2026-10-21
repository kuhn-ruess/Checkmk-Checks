#!/usr/bin/env python3
"""
DNF updates: agent plug-in deployment

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
    String,
    TimeMagnitude,
    TimeSpan,
)
from cmk.rulesets.v1.form_specs.validators import LengthInRange
from cmk.rulesets.v1.rule_specs import AgentConfig, Topic


def _agent_config_dnf_update() -> Dictionary:
    return Dictionary(
        help_text=Help(
            "Deploys the agent plug-in <tt>dnf_update</tt> for RHEL compatible hosts "
            "with dnf. It reports pending updates (<tt>dnf check-update</tt>, with and "
            "without <tt>--security</tt>), unreachable repositories, whether a reboot is "
            "required, the veto file and the last and next run of the dnf-automatic "
            "timer. dnf may take a while, so the plug-in should run asynchronously."
        ),
        elements={
            "deployment": DictElement(
                required=True,
                parameter_form=CascadingSingleChoice(
                    title=Title("Deployment type"),
                    elements=(
                        CascadingSingleChoiceElement(
                            name="cached",
                            title=Title("Deploy the plug-in and run it asynchronously"),
                            parameter_form=TimeSpan(
                                displayed_magnitudes=(TimeMagnitude.HOUR, TimeMagnitude.MINUTE),
                                prefill=DefaultValue(7200.0),
                            ),
                        ),
                        CascadingSingleChoiceElement(
                            name="sync",
                            title=Title("Deploy the plug-in and run it synchronously"),
                            parameter_form=FixedValue(value=None),
                        ),
                        CascadingSingleChoiceElement(
                            name="do_not_deploy",
                            title=Title("Do not deploy the plug-in"),
                            parameter_form=FixedValue(value=None),
                        ),
                    ),
                    prefill=DefaultValue("cached"),
                ),
            ),
            "veto_file": DictElement(
                parameter_form=String(
                    title=Title("Veto path"),
                    help_text=Help(
                        "If this file exists on the host, automatic updates are disabled. "
                        "The service then reports the veto instead of pending updates."
                    ),
                    custom_validate=(LengthInRange(min_value=1),),
                    prefill=DefaultValue("/etc/dnf.veto"),
                ),
            ),
        },
    )


rule_spec_dnf_update_bakery = AgentConfig(
    name="dnf_update",
    title=Title("DNF updates (Linux)"),
    topic=Topic.OPERATING_SYSTEM,
    parameter_form=_agent_config_dnf_update,
)
