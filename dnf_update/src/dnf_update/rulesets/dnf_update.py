#!/usr/bin/env python3
"""
DNF updates: check parameters

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    CascadingSingleChoice,
    CascadingSingleChoiceElement,
    DefaultValue,
    DictElement,
    Dictionary,
    FixedValue,
    Integer,
    ServiceState,
    SingleChoice,
    SingleChoiceElement,
)
from cmk.rulesets.v1.form_specs.validators import NumberInRange
from cmk.rulesets.v1.rule_specs import CheckParameters, HostCondition, Topic


def _parameter_form() -> Dictionary:
    return Dictionary(
        help_text=Help(
            "Evaluates pending dnf updates. The checks run in this order: reachability "
            "of the repositories, the veto file, the update week and the window after "
            "the last run of the dnf-automatic timer. Only when all of them pass, "
            "pending updates and a required reboot are evaluated; otherwise the "
            "service shows why the update check is skipped."
        ),
        elements={
            "window": DictElement(
                parameter_form=CascadingSingleChoice(
                    title=Title("Days after the update timer"),
                    help_text=Help(
                        "Pending updates are only evaluated within this number of days "
                        "after the last run of the dnf-automatic timer. On the day of the "
                        "run itself the check is skipped. Without a timer that ever ran, "
                        "updates are always evaluated."
                    ),
                    elements=(
                        CascadingSingleChoiceElement(
                            name="days",
                            title=Title("Only within this number of days"),
                            parameter_form=Integer(
                                unit_symbol="days",
                                custom_validate=(NumberInRange(min_value=1),),
                                prefill=DefaultValue(3),
                            ),
                        ),
                        CascadingSingleChoiceElement(
                            name="always",
                            title=Title("Always"),
                            parameter_form=FixedValue(value=None),
                        ),
                    ),
                    prefill=DefaultValue("days"),
                ),
            ),
            "update_week": DictElement(
                parameter_form=SingleChoice(
                    title=Title("Update week"),
                    help_text=Help(
                        "Evaluate updates only in even or odd ISO calendar weeks of the "
                        "monitored host, for example when hosts of one zone get their "
                        "updates in even weeks. Use the conditions of the rule to set it "
                        "per group of hosts."
                    ),
                    elements=(
                        SingleChoiceElement(name="any", title=Title("Every week")),
                        SingleChoiceElement(name="even", title=Title("Even calendar weeks")),
                        SingleChoiceElement(name="odd", title=Title("Odd calendar weeks")),
                    ),
                    prefill=DefaultValue("any"),
                ),
            ),
            "state_security": DictElement(
                parameter_form=ServiceState(
                    title=Title("State if security updates are available"),
                    prefill=DefaultValue(ServiceState.CRIT),
                ),
            ),
            "state_normal": DictElement(
                parameter_form=ServiceState(
                    title=Title("State if non-security updates are available"),
                    prefill=DefaultValue(ServiceState.WARN),
                ),
            ),
            "state_reboot": DictElement(
                parameter_form=ServiceState(
                    title=Title("State if a reboot is required"),
                    help_text=Help(
                        "Uses <tt>dnf needs-restarting -r</tt> (dnf-plugins-core). Without "
                        "it, the running kernel is compared with the newest installed one."
                    ),
                    prefill=DefaultValue(ServiceState.CRIT),
                ),
            ),
            "state_veto": DictElement(
                parameter_form=ServiceState(
                    title=Title("State if the veto file exists"),
                    help_text=Help(
                        "The veto file disables automatic updates, the update check is "
                        "skipped then. The path is set in the agent rule "
                        "<i>DNF updates (Linux)</i>."
                    ),
                    prefill=DefaultValue(ServiceState.CRIT),
                ),
            ),
            "state_repo": DictElement(
                parameter_form=ServiceState(
                    title=Title("State if a repository is not reachable"),
                    prefill=DefaultValue(ServiceState.CRIT),
                ),
            ),
        },
    )


rule_spec_dnf_update = CheckParameters(
    name="dnf_update",
    title=Title("DNF updates"),
    topic=Topic.OPERATING_SYSTEM,
    parameter_form=_parameter_form,
    condition=HostCondition(),
)
