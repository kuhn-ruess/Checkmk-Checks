#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.rulesets.v1 import Help, Label, Message, Title
from cmk.rulesets.v1.form_specs import (
    BooleanChoice,
    DefaultValue,
    DictElement,
    Dictionary,
    List,
    MatchingScope,
    RegularExpression,
    String,
    TimeMagnitude,
    TimeSpan,
    validators,
)
from cmk.rulesets.v1.rule_specs import (
    NotificationParameters,
    Topic,
)


def _validate_action(value):
    """Require at least one action and no conflicting downtime actions."""
    if not any(key in value for key in ("downtime", "acknowledge", "remove_downtime")):
        raise validators.ValidationError(
            Message("Enable a downtime, an acknowledgement or the removal of downtimes.")
        )
    if "downtime" in value and "remove_downtime" in value:
        raise validators.ValidationError(
            Message("A rule cannot schedule and remove downtimes at the same time.")
        )


def _time_span(title, help_text, prefill):
    return TimeSpan(
        title=title,
        help_text=help_text,
        displayed_magnitudes=[TimeMagnitude.DAY, TimeMagnitude.HOUR, TimeMagnitude.MINUTE],
        prefill=DefaultValue(prefill),
        custom_validate=(validators.NumberInRange(min_value=60),),
    )


def _rule_element():
    return Dictionary(
        custom_validate=(_validate_action,),
        elements={
            "service_regex": DictElement(
                parameter_form=RegularExpression(
                    title=Title("Service name"),
                    help_text=Help(
                        "Regular expression for the service name. Use <tt>.*</tt> for all "
                        "services the notification rule lets through."
                    ),
                    predefined_help_text=MatchingScope.PREFIX,
                    prefill=DefaultValue(".*"),
                    custom_validate=(validators.LengthInRange(min_value=1),),
                ),
                required=True,
            ),
            "output_regex": DictElement(
                parameter_form=RegularExpression(
                    title=Title("Text in the summary"),
                    help_text=Help(
                        "Regular expression searched in the summary (plugin output) of the "
                        "service. The rule only applies if it is found. Case-sensitive, "
                        "prefix it with <tt>(?i)</tt> to ignore the case."
                    ),
                    predefined_help_text=MatchingScope.INFIX,
                    custom_validate=(validators.LengthInRange(min_value=1),),
                ),
                required=True,
            ),
            "downtime": DictElement(
                parameter_form=Dictionary(
                    title=Title("Schedule a downtime"),
                    help_text=Help("Fixed downtime for the service, starting now."),
                    elements={
                        "duration": DictElement(
                            parameter_form=_time_span(
                                Title("Duration of the downtime"), None, 3600.0
                            ),
                            required=True,
                        ),
                    },
                ),
            ),
            "remove_downtime": DictElement(
                parameter_form=Dictionary(
                    title=Title("Remove downtimes"),
                    help_text=Help(
                        "Removes the downtimes of the service, for example when its summary "
                        "reports the end of a maintenance. Checkmk sends no notifications while "
                        "the service is in a downtime, so here this only removes downtimes that "
                        "have not started yet."
                    ),
                    elements={
                        "comment_regex": DictElement(
                            parameter_form=RegularExpression(
                                title=Title("Only downtimes with comment"),
                                help_text=Help(
                                    "Regular expression searched in the comment of the "
                                    "downtime. Leave it empty to remove all downtimes of the "
                                    "service."
                                ),
                                predefined_help_text=MatchingScope.INFIX,
                            ),
                            required=True,
                        ),
                    },
                ),
            ),
            "acknowledge": DictElement(
                parameter_form=Dictionary(
                    title=Title("Acknowledge the problem"),
                    elements={
                        "sticky": DictElement(
                            parameter_form=BooleanChoice(
                                label=Label("Sticky"),
                                help_text=Help(
                                    "Keep the acknowledgement until the service is OK again, "
                                    "also when it changes between WARN and CRIT."
                                ),
                                prefill=DefaultValue(True),
                            ),
                            required=True,
                        ),
                        "persistent": DictElement(
                            parameter_form=BooleanChoice(
                                label=Label("Persistent comment"),
                                help_text=Help(
                                    "Keep the acknowledgement comment after the "
                                    "acknowledgement is removed."
                                ),
                            ),
                            required=True,
                        ),
                        "notify": DictElement(
                            parameter_form=BooleanChoice(
                                label=Label("Send acknowledgement notification"),
                            ),
                            required=True,
                        ),
                        "expire": DictElement(
                            parameter_form=_time_span(
                                Title("Expire after"),
                                Help(
                                    "Remove the acknowledgement after this time. Needs the "
                                    "Checkmk Micro Core (commercial editions)."
                                ),
                                86400.0,
                            ),
                        ),
                    },
                ),
            ),
            "comment": DictElement(
                parameter_form=String(
                    title=Title("Comment"),
                    help_text=Help(
                        "Comment of the downtime and the acknowledgement. Without it the "
                        "comment names the matching regular expression."
                    ),
                ),
            ),
        },
    )


def _parameters_auto_downtime():
    return Dictionary(
        title=Title("Automatic downtime and acknowledgement"),
        help_text=Help(
            "Schedules a downtime for a service, acknowledges its problem or both, when its "
            "name and the text in its summary match one of the rules. All matching rules "
            "apply. If several rules match with the same action, or one schedules and another "
            "removes a downtime, the first of them wins. Only service problem notifications "
            "are handled."
        ),
        elements={
            "rules": DictElement(
                parameter_form=List(
                    title=Title("Rules"),
                    element_template=_rule_element(),
                    add_element_label=Label("Add rule"),
                    custom_validate=(validators.LengthInRange(min_value=1),),
                ),
                required=True,
            ),
            "author": DictElement(
                parameter_form=String(
                    title=Title("Author of downtime and acknowledgement"),
                    prefill=DefaultValue("auto_downtime"),
                ),
            ),
        },
    )


rule_spec_auto_downtime = NotificationParameters(
    title=Title("Automatic downtime and acknowledgement"),
    topic=Topic.NOTIFICATIONS,
    parameter_form=_parameters_auto_downtime,
    name="auto_downtime",
)
