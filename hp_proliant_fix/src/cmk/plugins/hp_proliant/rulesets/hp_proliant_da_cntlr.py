#!/usr/bin/env python3
# Copyright (C) 2026 Kuhn & Rueß GmbH - License: GNU General Public License v2
#
# Check parameters for the (overridden) hp_proliant_da_cntlr check. Lets the
# state reported for the "other" enum value be remapped per column. Defaults to
# WARN everywhere, i.e. the behaviour of the built-in check.
#
# Motivation: HPE ProLiant Gen11 / iLO 6 firmware reports
# cpqDaCntlrBoardCondition = other(1) for healthy controllers, which otherwise
# pins the "HW Controller" service to WARN permanently.

from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    ServiceState,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _parameter_form() -> Dictionary:
    return Dictionary(
        help_text=Help(
            "Maps the state that the HP ProLiant controller check reports for the "
            "<tt>other</tt> enum value of each condition/status column. The default "
            "is WARN (the behaviour of the built-in check). On ProLiant Gen11 / "
            "iLO 6, healthy controllers often report Board-Condition <tt>other</tt>; "
            "set that to OK to avoid a permanent false WARN."
        ),
        elements={
            "condition_other_state": DictElement(
                required=True,
                parameter_form=ServiceState(
                    title=Title("State when Condition is 'other'"),
                    prefill=DefaultValue(ServiceState.WARN),
                ),
            ),
            "board_condition_other_state": DictElement(
                required=True,
                parameter_form=ServiceState(
                    title=Title("State when Board-Condition is 'other'"),
                    help_text=Help(
                        "ProLiant Gen11 / iLO 6 commonly reports this as 'other' for "
                        "healthy controllers; set to OK to suppress the false WARN."
                    ),
                    prefill=DefaultValue(ServiceState.WARN),
                ),
            ),
            "board_status_other_state": DictElement(
                required=True,
                parameter_form=ServiceState(
                    title=Title("State when Board-Status is 'other'"),
                    prefill=DefaultValue(ServiceState.WARN),
                ),
            ),
        },
    )


rule_spec_hp_proliant_da_cntlr = CheckParameters(
    name="hp_proliant_da_cntlr",
    title=Title("HP ProLiant RAID controller"),
    topic=Topic.SERVER_HARDWARE,
    parameter_form=_parameter_form,
    condition=HostAndItemCondition(item_title=Title("Controller index")),
)
