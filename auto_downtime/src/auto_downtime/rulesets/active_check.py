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
    Password,
    RegularExpression,
    String,
    TimeMagnitude,
    TimeSpan,
    validators,
)
from cmk.rulesets.v1.rule_specs import ActiveCheck, Topic


def _validate_action(value):
    """Require at least one action and no conflicting actions."""
    if not any(
        key in value for key in ("downtime", "acknowledge", "remove_downtime", "remove_acknowledge")
    ):
        raise validators.ValidationError(
            Message("Enable at least one action: a downtime, an acknowledgement or their removal.")
        )
    if "downtime" in value and "remove_downtime" in value:
        raise validators.ValidationError(
            Message("A rule cannot schedule and remove downtimes at the same time.")
        )
    if "acknowledge" in value and "remove_acknowledge" in value:
        raise validators.ValidationError(
            Message("A rule cannot acknowledge and remove acknowledgements at the same time.")
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
            "host_regex": DictElement(
                parameter_form=RegularExpression(
                    title=Title("Host name"),
                    help_text=Help("Regular expression for the host name. Without it all hosts match."),
                    predefined_help_text=MatchingScope.PREFIX,
                ),
            ),
            "service_regex": DictElement(
                parameter_form=RegularExpression(
                    title=Title("Service name"),
                    help_text=Help("Regular expression for the service name. Use <tt>.*</tt> for all services."),
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
                    help_text=Help(
                        "Fixed downtime from now on. Not set again while the service is in a downtime."
                    ),
                    elements={
                        "duration": DictElement(
                            parameter_form=_time_span(Title("Duration of the downtime"), None, 3600.0),
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
                        "reports the end of a maintenance."
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
                    help_text=Help(
                        "Only services in state WARN, CRIT or UNKNOWN are acknowledged, and only "
                        "if they are not acknowledged yet."
                    ),
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
                                    "Keep the acknowledgement comment after the acknowledgement is removed."
                                ),
                            ),
                            required=True,
                        ),
                        "notify": DictElement(
                            parameter_form=BooleanChoice(label=Label("Send acknowledgement notification")),
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
            "remove_acknowledge": DictElement(
                parameter_form=Dictionary(
                    title=Title("Remove the acknowledgement"),
                    help_text=Help(
                        "Removes the acknowledgement of the service, for example when its "
                        "summary reports that the acknowledged problem is gone while the "
                        "service stays in a problem state for another reason."
                    ),
                    elements={},
                ),
            ),
            "comment": DictElement(
                parameter_form=String(
                    title=Title("Comment"),
                    help_text=Help(
                        "Comment of the downtime and the acknowledgement. Without it the comment "
                        "names the matching regular expression."
                    ),
                ),
            ),
        },
    )


def _parameters_auto_downtime():
    return Dictionary(
        title=Title("Automatic downtime and acknowledgement"),
        help_text=Help(
            "Queries the services of the Checkmk site via the REST API on every check interval. "
            "For each service whose name and summary match a rule, a downtime is scheduled, the "
            "problem is acknowledged, or downtimes and acknowledgements are removed. All matching "
            "rules apply. If several rules match with the same action, or with the opposite "
            "action (schedule and remove a downtime, acknowledge and remove the acknowledgement), "
            "the first of them wins."
        ),
        elements={
            "description": DictElement(
                parameter_form=String(
                    title=Title("Service name of this check"),
                    prefill=DefaultValue("Auto downtime"),
                    custom_validate=(validators.LengthInRange(min_value=1),),
                ),
                required=True,
            ),
            "url": DictElement(
                parameter_form=String(
                    title=Title("Checkmk URL"),
                    help_text=Help(
                        "Base URL of the Checkmk site, for example "
                        "<tt>https://monitoring.example.com/mysite</tt>. Without it the local "
                        "site is used."
                    ),
                    field_size=60,
                ),
            ),
            "username": DictElement(
                parameter_form=String(
                    title=Title("Automation user"),
                    help_text=Help(
                        "User for the REST API. It needs permission to see the services and to "
                        "set downtimes and acknowledgements on them."
                    ),
                    custom_validate=(validators.LengthInRange(min_value=1),),
                ),
                required=True,
            ),
            "secret": DictElement(
                parameter_form=Password(title=Title("Automation secret")),
                required=True,
            ),
            "verify_ssl": DictElement(
                parameter_form=BooleanChoice(
                    label=Label("Verify the SSL certificate"),
                    prefill=DefaultValue(True),
                ),
                required=True,
            ),
            "rules": DictElement(
                parameter_form=List(
                    title=Title("Rules"),
                    element_template=_rule_element(),
                    add_element_label=Label("Add rule"),
                    custom_validate=(validators.LengthInRange(min_value=1),),
                ),
                required=True,
            ),
        },
    )


rule_spec_auto_downtime = ActiveCheck(
    title=Title("Automatic downtime and acknowledgement by plugin output"),
    topic=Topic.GENERAL,
    parameter_form=_parameters_auto_downtime,
    name="auto_downtime",
)
