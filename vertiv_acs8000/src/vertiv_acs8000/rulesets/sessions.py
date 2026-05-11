#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    Integer,
    LevelDirection,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostCondition, Topic


def _parameter_form_vertiv_acs8000_sessions():
    return Dictionary(
        title=Title("Vertiv ACS active sessions"),
        help_text=Help("Levels on the number of active sessions on a Vertiv Avocent ACS 8000 console server."),
        elements={
            "levels": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Upper levels for active sessions"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Integer(unit_symbol="sessions"),
                    prefill_fixed_levels=DefaultValue((50, 100)),
                ),
            ),
        },
    )


rule_spec_vertiv_acs8000_sessions = CheckParameters(
    name="vertiv_acs8000_sessions",
    topic=Topic.NETWORKING,
    condition=HostCondition(),
    parameter_form=_parameter_form_vertiv_acs8000_sessions,
    title=Title("Vertiv ACS active sessions"),
)
