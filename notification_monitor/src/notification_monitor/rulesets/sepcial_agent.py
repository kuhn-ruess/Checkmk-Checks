#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
from cmk.rulesets.v1 import Title, Help
from cmk.rulesets.v1.form_specs import (
    Dictionary,
    DictElement,
    String,
    TimeSpan,
    TimeMagnitude,
    DefaultValue,
)
from cmk.rulesets.v1.form_specs.validators import LengthInRange
from cmk.rulesets.v1.rule_specs import SpecialAgent, Topic


def _valuespec_special_agent_notification_monitor():
    """
    Notification Counter Special Agent Konfiguration
    """

    return Dictionary(
        title = Title("Service counter"),
        help_text = Help("This rule activates special agent for service counting"),
        elements = {
            "path": DictElement(
                parameter_form = String(
                    title = Title("Path to Checkmk Site"),
                    help_text = Help("This is needed to access the Web Site of "\
                                     "the central site, even if plugin is running on remote site."\
                                     "Example: https://server/site/"),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required = True,
            ),
            "command_regex": DictElement(
                parameter_form = String(
                    title = Title("Regex to Filter Notifcation Command"),
                    help_text = Help("You can see the Command Names in your Notification Setup"),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required = True,
            ),
            "timeout": DictElement(
                parameter_form = TimeSpan(
                    title = Title("Timeout"),
                    displayed_magnitudes=[TimeMagnitude.MILLISECOND, TimeMagnitude.SECOND],
                    prefill = DefaultValue(2.5),
                ),
                required = True,
            ),
        },
    )


rule_spec_service_counter = SpecialAgent(
    name = "notification_monitor",
    topic = Topic.APPLICATIONS,
    parameter_form = _valuespec_special_agent_notification_monitor,
    title = Title("Notification Monitor"),
)
