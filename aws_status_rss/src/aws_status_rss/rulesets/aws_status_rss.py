#!/usr/bin/env python3
"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de

Check parameters for the AWS Status RSS check.
"""
from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    String,
    TimeMagnitude,
    TimeSpan,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _parameter_form():
    magnitudes = [
        TimeMagnitude.SECOND,
        TimeMagnitude.MINUTE,
        TimeMagnitude.HOUR,
        TimeMagnitude.DAY,
    ]
    return Dictionary(
        elements={
            "event_age_warn": DictElement(
                parameter_form=TimeSpan(
                    title=Title("Warn if newest event is younger than"),
                    help_text=Help(
                        "Any AWS service event published within this window "
                        "raises a WARN state. Defaults to seven days."
                    ),
                    displayed_magnitudes=magnitudes,
                    prefill=DefaultValue(7.0 * 24 * 3600),
                ),
                required=False,
            ),
            "event_age_crit": DictElement(
                parameter_form=TimeSpan(
                    title=Title("Critical if newest event is younger than"),
                    help_text=Help(
                        "Any AWS service event published within this window "
                        "raises a CRIT state. Defaults to one day."
                    ),
                    displayed_magnitudes=magnitudes,
                    prefill=DefaultValue(24.0 * 3600),
                ),
                required=False,
            ),
        },
    )


rule_spec_aws_status_rss = CheckParameters(
    name="aws_status_rss",
    topic=Topic.CLOUD,
    condition=HostAndItemCondition(
        item_title=Title("AWS service name"),
        item_form=String(),
    ),
    parameter_form=_parameter_form,
    title=Title("AWS service status RSS"),
)
