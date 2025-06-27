#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    Dictionary,
    DictElement,
    SimpleLevels,
    LevelDirection,
    TimeSpan,
    TimeMagnitude,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostCondition, Topic


def _valuespec_palo_alto_antivirus():
    return Dictionary(
        title = Title("Age for antivirus updates"),
        help_text = Help("Please configure levels for maximum age of last antivirus update."),
        elements = {
            "age": DictElement(
                parameter_form = SimpleLevels(
                    title = Title("Age for antivirus updates"),
                    level_direction = LevelDirection.UPPER,
                    form_spec_template = TimeSpan(
                        #title = Title("Signature age"),
                        displayed_magnitudes=[TimeMagnitude.DAY, TimeMagnitude.HOUR],
                    ),
                    prefill_fixed_levels = DefaultValue((86400, 104400)),
                ),
            ),
        },
    )

rule_spec_palo_alto_antivirus = CheckParameters(
    name = "palo_alto_antivirus",
    topic = Topic.APPLICATIONS,
    condition = HostCondition(),
    parameter_form = _valuespec_palo_alto_antivirus,
    title = Title("Palo Alto antivirus age"),
)
