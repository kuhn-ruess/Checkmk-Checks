#!/usr/bin/env python3

"""
Service Group States Check Parameters

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.rulesets.v1 import Help, Label, Title
from cmk.rulesets.v1.form_specs import (
    BooleanChoice,
    CascadingSingleChoice,
    CascadingSingleChoiceElement,
    DefaultValue,
    DictElement,
    Dictionary,
    FixedValue,
    Integer,
    MultipleChoice,
    MultipleChoiceElement,
    Percentage,
    ServiceState,
)
from cmk.rulesets.v1.form_specs.validators import LengthInRange, NumberInRange
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _trigger_choice(title, help_text):
    """
    How many members of the group have to be affected before the
    service group service alarms
    """
    return CascadingSingleChoice(
        title=title,
        help_text=help_text,
        elements=[
            CascadingSingleChoiceElement(
                name="any",
                title=Title("One member is enough"),
                parameter_form=FixedValue(
                    value=None,
                    label=Label("Alarm as soon as a single member is affected"),
                ),
            ),
            CascadingSingleChoiceElement(
                name="all",
                title=Title("All members have to be affected"),
                parameter_form=FixedValue(
                    value=None,
                    label=Label("Alarm only when every member of the group is affected"),
                ),
            ),
            CascadingSingleChoiceElement(
                name="at_least",
                title=Title("At least this many members"),
                parameter_form=Integer(
                    label=Label("Members"),
                    prefill=DefaultValue(2),
                    custom_validate=(NumberInRange(min_value=1),),
                ),
            ),
            CascadingSingleChoiceElement(
                name="percent",
                title=Title("At least this share of the members"),
                parameter_form=Percentage(
                    prefill=DefaultValue(50.0),
                    custom_validate=(NumberInRange(min_value=0.1, max_value=100.0),),
                ),
            ),
        ],
        prefill=DefaultValue("any"),
    )


def _parameter_form_servicegroup_states() -> Dictionary:
    """
    Check parameters for one service group service
    """
    return Dictionary(
        help_text=Help(
            "Defines when the service of a monitored service group goes into a "
            "non OK state. The problem state trigger and the stale trigger are "
            "evaluated independently, each one can be switched off by removing it "
            "from this rule."
        ),
        elements={
            "problem": DictElement(
                parameter_form=Dictionary(
                    title=Title("Alarm on members in a problem state"),
                    elements={
                        "states": DictElement(
                            parameter_form=MultipleChoice(
                                title=Title("States counting as a problem"),
                                elements=[
                                    MultipleChoiceElement(name="warn", title=Title("WARN")),
                                    MultipleChoiceElement(name="crit", title=Title("CRIT")),
                                    MultipleChoiceElement(name="unknown", title=Title("UNKNOWN")),
                                ],
                                prefill=DefaultValue(["crit", "unknown"]),
                                custom_validate=(LengthInRange(min_value=1),),
                            ),
                            required=True,
                        ),
                        "mode": DictElement(
                            parameter_form=_trigger_choice(
                                Title("Trigger"),
                                Help(
                                    "How many members of the group have to be in one of the "
                                    "selected states before this service alarms."
                                ),
                            ),
                            required=True,
                        ),
                        "result": DictElement(
                            parameter_form=ServiceState(
                                title=Title("Resulting state"),
                                prefill=DefaultValue(ServiceState.CRIT),
                            ),
                            required=True,
                        ),
                    },
                ),
                required=False,
            ),
            "stale": DictElement(
                parameter_form=Dictionary(
                    title=Title("Alarm on stale members"),
                    elements={
                        "mode": DictElement(
                            parameter_form=_trigger_choice(
                                Title("Trigger"),
                                Help(
                                    "How many members of the group have to be stale "
                                    "before this service alarms."
                                ),
                            ),
                            required=True,
                        ),
                        "result": DictElement(
                            parameter_form=ServiceState(
                                title=Title("Resulting state"),
                                prefill=DefaultValue(ServiceState.WARN),
                            ),
                            required=True,
                        ),
                    },
                ),
                required=False,
            ),
            "only_hard_states": DictElement(
                parameter_form=BooleanChoice(
                    title=Title("Only count hard states"),
                    label=Label("Ignore members which are still in a soft state"),
                    prefill=DefaultValue(True),
                ),
                required=False,
            ),
            "ignore_acknowledged": DictElement(
                parameter_form=BooleanChoice(
                    title=Title("Ignore acknowledged members"),
                    label=Label("Do not count members with an acknowledged problem"),
                    prefill=DefaultValue(False),
                ),
                required=False,
            ),
            "ignore_downtime": DictElement(
                parameter_form=BooleanChoice(
                    title=Title("Ignore members in downtime"),
                    label=Label("Do not count members which are in a scheduled downtime"),
                    prefill=DefaultValue(True),
                ),
                required=False,
            ),
            "empty_group": DictElement(
                parameter_form=ServiceState(
                    title=Title("State when the service group is empty"),
                    prefill=DefaultValue(ServiceState.WARN),
                ),
                required=False,
            ),
        },
    )


rule_spec_servicegroup_states_parameters = CheckParameters(
    name="servicegroup_states",
    title=Title("Checkmk service group states"),
    topic=Topic.GENERAL,
    parameter_form=_parameter_form_servicegroup_states,
    condition=HostAndItemCondition(item_title=Title("Service group")),
)
