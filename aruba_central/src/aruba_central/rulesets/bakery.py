#!/usr/bin/env python3
"""
Aruba Central - agent plugin deployment

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


def _agent_config_aruba_central() -> Dictionary:
    return Dictionary(
        help_text=Help(
            "Deploys the agent plug-in <tt>aruba_central</tt>, which calls "
            "<tt>cencli show aps -v --json</tt> and turns the result into one "
            "piggyback section per access point. The Linux and the Windows "
            "variant produce the same sections, cencli has to be installed and "
            "configured for the user the agent runs as. The call takes about 30 "
            "seconds, so it should be deployed asynchronously."
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
                                displayed_magnitudes=(
                                    TimeMagnitude.HOUR,
                                    TimeMagnitude.MINUTE,
                                ),
                                prefill=DefaultValue(900.0),
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
        },
    )


rule_spec_aruba_central_bakery = AgentConfig(
    name="aruba_central",
    title=Title("Aruba Central access points (cencli)"),
    topic=Topic.NETWORKING,
    parameter_form=_agent_config_aruba_central,
)
