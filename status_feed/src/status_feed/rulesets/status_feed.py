#!/usr/bin/env python3
"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de

Check parameters for the status feed check.
"""
from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    ServiceState,
    SingleChoice,
    SingleChoiceElement,
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
        help_text=Help(
            "Two evaluation modes. By default (AWS-style per-service feeds) "
            "the age of the newest entry decides the state: a fresh entry "
            "means an event is in flight. In incident mode (Statuspage-style "
            "history feeds such as Scrivito, which keep resolved incidents "
            "forever) the lifecycle of the newest entry decides instead."
        ),
        elements={
            "incident_mode": DictElement(
                parameter_form=SingleChoice(
                    title=Title("Evaluation mode"),
                    help_text=Help(
                        "Age mode (default) alerts on recent entries; incident "
                        "mode classifies the newest entry as active or resolved."
                    ),
                    elements=[
                        SingleChoiceElement(
                            name="age",
                            title=Title("Age mode (AWS per-service feeds)"),
                        ),
                        SingleChoiceElement(
                            name="incident",
                            title=Title("Incident mode (Statuspage/history feeds)"),
                        ),
                    ],
                    prefill=DefaultValue("age"),
                ),
                required=False,
            ),
            "active_incident_state": DictElement(
                parameter_form=ServiceState(
                    title=Title("State on an active incident (incident mode)"),
                    help_text=Help(
                        "State reported when the newest entry is classified as "
                        "an active incident. Only used in incident mode."
                    ),
                    prefill=DefaultValue(ServiceState.CRIT),
                ),
                required=False,
            ),
            "event_age_warn": DictElement(
                parameter_form=TimeSpan(
                    title=Title("Warn if newest event is younger than (age mode)"),
                    help_text=Help(
                        "Any event published within this window raises a WARN "
                        "state. Defaults to seven days."
                    ),
                    displayed_magnitudes=magnitudes,
                    prefill=DefaultValue(7.0 * 24 * 3600),
                ),
                required=False,
            ),
            "event_age_crit": DictElement(
                parameter_form=TimeSpan(
                    title=Title("Critical if newest event is younger than (age mode)"),
                    help_text=Help(
                        "Any event published within this window raises a CRIT "
                        "state. Defaults to one day."
                    ),
                    displayed_magnitudes=magnitudes,
                    prefill=DefaultValue(24.0 * 3600),
                ),
                required=False,
            ),
        },
    )


rule_spec_status_feed = CheckParameters(
    name="status_feed",
    topic=Topic.CLOUD,
    condition=HostAndItemCondition(
        item_title=Title("Feed name"),
        item_form=String(),
    ),
    parameter_form=_parameter_form,
    title=Title("Status RSS/Atom feeds"),
)
