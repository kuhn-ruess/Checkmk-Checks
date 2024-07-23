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
    String,
    RegularExpression,
    DefaultValue,
    MatchingScope,
    TimeSpan,
    TimeMagnitude,
)
from cmk.rulesets.v1.rule_specs import ActiveCheck, Topic


def _form_active_check_videotext():
    return Dictionary(
        title = Title("Videotext timestamp monitoring"),
        elements = {
            "url": DictElement(
                parameter_form = String(
                    title = Title("URL"),
                    help_text = Help("Complete URL for monitoring"),
                ),
                required = True,
            ),
            "pattern": DictElement(
                parameter_form = RegularExpression(
                    title = Title("RegEx search pattern"),
                    help_text = Help("Regular expressio for searching timestamp. Timestamp must be saved as group."),
                    prefill = DefaultValue("Stand:.*?(\d+:\d+)"),
                    predefined_help_text = MatchingScope.INFIX,
                ),
                required = True,
            ),
            "timeout": DictElement(
                parameter_form = TimeSpan(
                    title = Title("Timeout"),
                    displayed_magnitudes=[TimeMagnitude.MILLISECOND, TimeMagnitude.SECOND],
                    prefill = DefaultValue(2.5),
                ),
            ),
            "warn": DictElement(
                parameter_form = TimeSpan(
                    title = Title("Warn, if time difference is equal or above"),
                    displayed_magnitudes=[TimeMagnitude.SECOND, TimeMagnitude.MINUTE, TimeMagnitude.HOUR],
                    prefill = DefaultValue(900.0),
                ),
            ),
            "crit": DictElement(
                parameter_form = TimeSpan(
                    title = Title("Crit, if time difference is equal or above"),
                    displayed_magnitudes=[TimeMagnitude.SECOND, TimeMagnitude.MINUTE, TimeMagnitude.HOUR],
                    prefill = DefaultValue(1200.0),
                ),
            ),
        }
    )


rule_spec_videotext = ActiveCheck(
    title = Title("Videotext timestamp monitoring"),
    topic = Topic.APPLICATIONS,
    name = "videotext",
    parameter_form = _form_active_check_videotext,
)
