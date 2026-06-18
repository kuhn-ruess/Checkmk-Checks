#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    LevelDirection,
    MultipleChoice,
    MultipleChoiceElement,
    SimpleLevels,
    TimeMagnitude,
    TimeSpan,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic

_JOB_STATES = [
    ("A", "Canceled by user"),
    ("B", "Blocked"),
    ("C", "Created, but not running"),
    ("c", "Waiting for client resource"),
    ("D", "Verify differences"),
    ("d", "Waiting for maximum jobs"),
    ("E", "Terminated in error"),
    ("e", "Non-fatal error"),
    ("f", "fatal error"),
    ("F", "Waiting on File Daemon"),
    ("j", "Waiting for job resource"),
    ("M", "Waiting for mount"),
    ("m", "Waiting for new media"),
    ("p", "Waiting for higher priority jobs to finish"),
    ("R", "Running"),
    ("S", "Scan"),
    ("s", "Waiting for storage resource"),
    ("T", "Terminated normally"),
    ("t", "Waiting for start time"),
    ("W", "Terminated with Warning"),
]


def _parameter_form_bacula_jobs() -> Dictionary:
    return Dictionary(
        elements={
            "max_age": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Age of last Backup"),
                    form_spec_template=TimeSpan(
                        displayed_magnitudes=[
                            TimeMagnitude.DAY,
                            TimeMagnitude.HOUR,
                            TimeMagnitude.MINUTE,
                        ],
                    ),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=DefaultValue((86400.0 * 5, 86400.0 * 7)),
                ),
            ),
            "ok_states": DictElement(
                parameter_form=MultipleChoice(
                    title=Title("States which result in OK"),
                    elements=[
                        MultipleChoiceElement(name=code, title=Title(text))  # noqa: B023
                        for code, text in _JOB_STATES
                    ],
                    prefill=DefaultValue(["T", "R"]),
                ),
            ),
            "crit_states": DictElement(
                parameter_form=MultipleChoice(
                    title=Title("States which result in Critical"),
                    elements=[
                        MultipleChoiceElement(name=code, title=Title(text))  # noqa: B023
                        for code, text in _JOB_STATES
                    ],
                    prefill=DefaultValue(["E", "f"]),
                ),
            ),
        },
    )


rule_spec_bacula_jobs = CheckParameters(
    name="bacula_jobs",
    title=Title("Bacula Jobs"),
    topic=Topic.APPLICATIONS,
    parameter_form=_parameter_form_bacula_jobs,
    condition=HostAndItemCondition(item_title=Title("Job Name")),
)
