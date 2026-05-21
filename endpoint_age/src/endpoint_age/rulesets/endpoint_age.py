#!/usr/bin/env python3
"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de

Check parameters for the endpoint freshness check.
"""
from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    LevelDirection,
    SimpleLevels,
    String,
    TimeMagnitude,
    TimeSpan,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _parameter_form():
    return Dictionary(
        elements={
            "max_age": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Maximum allowed age"),
                    help_text=Help(
                        "Raise WARN / CRIT when the extracted age "
                        "exceeds the configured thresholds."
                    ),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=TimeSpan(
                        displayed_magnitudes=(
                            TimeMagnitude.SECOND,
                            TimeMagnitude.MINUTE,
                            TimeMagnitude.HOUR,
                            TimeMagnitude.DAY,
                        ),
                    ),
                    prefill_fixed_levels=DefaultValue((15.0 * 60, 60.0 * 60)),
                ),
                required=True,
            ),
        },
    )


rule_spec_endpoint_age = CheckParameters(
    name="endpoint_age",
    topic=Topic.GENERAL,
    condition=HostAndItemCondition(
        item_title=Title("Endpoint name"),
        item_form=String(),
    ),
    parameter_form=_parameter_form,
    title=Title("Endpoint age (HTTP freshness)"),
)
