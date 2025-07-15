#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    Dictionary,
    DictElement,
    CascadingSingleChoice,
    CascadingSingleChoiceElement,
    FixedValue,
    DefaultValue,
)
from cmk.rulesets.v1.rule_specs import AgentConfig, Topic


def _valuespec_agent_lnx_sensors():
    return Dictionary(
        title = Title("Sensors"),
        help_text = Help("This will deploy the agent plugin <tt>lnx_sensors</tt> for monitoring the status of sensors."),
        elements = {
            "deploy": DictElement(
                parameter_form = CascadingSingleChoice(
                    title = Title("Deployment type"),
                    elements = (
                        CascadingSingleChoiceElement(
                            name = "sync",
                            title = Title("Deploy plug-in and run it synchronously"),
                            parameter_form=FixedValue(value=True),
                        ),
                        CascadingSingleChoiceElement(
                            name="no_deploy",
                            title=Title("Do not deploy the plug-in"),
                            parameter_form=FixedValue(value=None),
                        ),
                    ),
                    prefill=DefaultValue("sync"),
                ),
                required=True,
            ),
        }
    )


rule_spec_agent_lnx_sensors = AgentConfig(
    name = "lnx_sensors",
    title = Title("Sensors"),
    topic=Topic.OPERATING_SYSTEM,
    parameter_form = _valuespec_agent_lnx_sensors,
)
