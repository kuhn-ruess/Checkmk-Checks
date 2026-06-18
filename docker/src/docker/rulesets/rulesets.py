#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    BooleanChoice,
    DefaultValue,
    DictElement,
    Dictionary,
    List,
    String,
    TimeMagnitude,
    TimeSpan,
)
from cmk.rulesets.v1.rule_specs import AgentConfig, Topic


def _agent_config_check_docker() -> Dictionary:
    return Dictionary(
        help_text=Help("Hosts configured via this rule get the <tt>docker.py</tt> plugin"),
        elements={
            "activated": DictElement(
                parameter_form=BooleanChoice(
                    title=Title("Deploy docker plugin"),
                    prefill=DefaultValue(True),
                ),
            ),
            "interval": DictElement(
                parameter_form=TimeSpan(
                    title=Title("Interval for docker check"),
                    displayed_magnitudes=(
                        TimeMagnitude.DAY,
                        TimeMagnitude.HOUR,
                        TimeMagnitude.MINUTE,
                    ),
                    prefill=DefaultValue(120.0),
                ),
            ),
            "timeout": DictElement(
                parameter_form=TimeSpan(
                    title=Title("Connection timeout"),
                    displayed_magnitudes=(
                        TimeMagnitude.MINUTE,
                        TimeMagnitude.SECOND,
                    ),
                    prefill=DefaultValue(30.0),
                ),
            ),
            "label_whitelist": DictElement(
                parameter_form=List(
                    title=Title("Label Whitelist"),
                    element_template=String(title=Title("Label")),
                ),
            ),
            "label_replacements": DictElement(
                parameter_form=List(
                    title=Title("Label rewriting"),
                    element_template=Dictionary(
                        elements={
                            "original": DictElement(
                                required=True,
                                parameter_form=String(title=Title("Original Label")),
                            ),
                            "rewritten": DictElement(
                                required=True,
                                parameter_form=String(title=Title("Rewritten Label")),
                            ),
                        },
                    ),
                ),
            ),
            "piggyback": DictElement(
                parameter_form=BooleanChoice(
                    title=Title("Use service swarm name as piggyback hostname"),
                    prefill=DefaultValue(False),
                ),
            ),
        },
    )


rule_spec_check_docker = AgentConfig(
    name="check_docker",
    title=Title("Docker Agent Based (Linux)"),
    topic=Topic.GENERAL,
    parameter_form=_agent_config_check_docker,
)
