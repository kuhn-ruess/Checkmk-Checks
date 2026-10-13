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
    InputHint,
    Integer,
    LevelDirection,
    ServiceState,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostCondition, Topic


def _count_levels(title, help_text, prefill):
    """
    Upper levels on a counter
    """
    return SimpleLevels(
        title = title,
        help_text = help_text,
        level_direction = LevelDirection.UPPER,
        form_spec_template = Integer(),
        prefill_fixed_levels = InputHint(prefill),
    )


def _parameter_form_cmdb_syncer_eda():
    return Dictionary(
        title = Title("CMDB Syncer Event Driven Ansible events"),
        help_text = Help(
            "An event streak starts when a host matches an EDA Event Rule and counts every "
            "send of that event. It ends when the host no longer gets the event, then the "
            "playbook had an effect. A streak that is still open after the repeat threshold "
            "of its EDA account (default 3 sends) is repeating."
        ),
        elements = {
            "repeating": DictElement(
                parameter_form = _count_levels(
                    Title("Repeating events"),
                    Help("Number of events that were sent at least as often as the repeat "
                         "threshold of their account and the host still matches. "
                         "Default: WARN at 1, CRIT at 10."),
                    (1, 10),
                ),
            ),
            "repeating_hosts": DictElement(
                parameter_form = _count_levels(
                    Title("Hosts with repeating events"),
                    Help("Number of distinct hosts with at least one repeating event. "
                         "No levels by default."),
                    (1, 5),
                ),
            ),
            "failing_state": DictElement(
                parameter_form = ServiceState(
                    title = Title("State if events are failing"),
                    help_text = Help("Applied when at least one open streak was rejected by "
                                     "the event stream on its last send. Default: CRIT."),
                    prefill = DefaultValue(ServiceState.CRIT),
                ),
            ),
            "failed_24h": DictElement(
                parameter_form = _count_levels(
                    Title("Events rejected in the last 24 hours"),
                    Help("Events the event stream did not accept in the last 24 hours. "
                         "No levels by default."),
                    (1, 10),
                ),
            ),
            "max_sends": DictElement(
                parameter_form = _count_levels(
                    Title("Most sends of a single event"),
                    Help("Highest number of sends of any open streak. No levels by default."),
                    (5, 10),
                ),
            ),
        },
    )


rule_spec_cmdb_syncer_eda = CheckParameters(
    name = "cmdb_syncer_eda",
    topic = Topic.OPERATING_SYSTEM,
    condition = HostCondition(),
    parameter_form = _parameter_form_cmdb_syncer_eda,
    title = Title("CMDB Syncer Event Driven Ansible"),
)
