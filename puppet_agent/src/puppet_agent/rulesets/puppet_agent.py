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
    TimeMagnitude,
    TimeSpan,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostCondition, Topic


def _count_levels(title: str) -> DictElement:
    return DictElement(
        required=True,
        parameter_form=SimpleLevels(
            title=Title(title),
            form_spec_template=Integer(),
            level_direction=LevelDirection.UPPER,
            prefill_fixed_levels=DefaultValue((10, 15)),
        ),
    )


def _parameter_form_puppet_agent() -> Dictionary:
    return Dictionary(
        help_text=Help("Levels for the status of the local Puppet agent."),
        elements={
            "last_run": DictElement(
                required=True,
                parameter_form=SimpleLevels(
                    title=Title("Time since last run"),
                    form_spec_template=TimeSpan(
                        displayed_magnitudes=[
                            TimeMagnitude.HOUR,
                            TimeMagnitude.MINUTE,
                            TimeMagnitude.SECOND,
                        ],
                    ),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=DefaultValue((1600.0, 3200.0)),
                ),
            ),
            "events_failure": _count_levels("Event Failures"),
            "resources_changed": _count_levels("Resources Changed"),
            "resources_failed": _count_levels("Resources Failed"),
            "resources_failed_to_restart": _count_levels("Resources Failed to restart"),
            "resources_out_of_sync": _count_levels("Resources out of Sync"),
            "resources_restarted": _count_levels("Resources Restarted"),
            "resources_scheduled": _count_levels("Resources Scheduled"),
        },
    )


rule_spec_puppet_agent = CheckParameters(
    name="puppet_agent",
    title=Title("Puppet Agent"),
    topic=Topic.APPLICATIONS,
    parameter_form=_parameter_form_puppet_agent,
    condition=HostCondition(),
)
