#!/usr/bin/env python3
# Copyright (C) 2021 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from collections.abc import Mapping

from cmk.rulesets.v1 import Help, Title, Label
from cmk.rulesets.v1.form_specs import (
    BooleanChoice,
    DefaultValue,
    DictElement,
    Dictionary,
    List,
    ServiceState,
    String,
    validators,
)
from cmk.rulesets.v1.rule_specs import (
    CheckParameters,
    HostAndItemCondition,
    HostCondition,
    Topic,
)

# Discovery is handled by Checkmk's built-in ``discovery_alertmanager`` ruleset;
# this package only overrides the check plugins to add severity remapping.


# introduced in version 2.3
def migrate_non_identifier_key(raw_value: object) -> Mapping[str, object]:
    if not isinstance(raw_value, dict):
        raise TypeError("Invalid type. map should be a dict.")

    if "n/a" in raw_value:
        raw_value["not_applicable"] = raw_value.pop("n/a")

    return raw_value


def form_alert_remapping():
    return List(
        element_template=Dictionary(
            elements={
                "rule_names": DictElement(
                    parameter_form=List(
                        element_template=String(prefill=DefaultValue("Watchdog")),
                        title=Title("Alert rule names"),
                        help_text=Help("A list of rule names as defined in Alertmanager."),
                    ),
                    required=True,
                ),
                "map": DictElement(
                    parameter_form=Dictionary(
                        title=Title("States"),
                        elements={
                            "inactive": DictElement(
                                parameter_form=ServiceState(
                                    title=Title("inactive"), prefill=DefaultValue(2)
                                ),
                                required=True,
                            ),
                            "pending": DictElement(
                                parameter_form=ServiceState(
                                    title=Title("pending"), prefill=DefaultValue(2)
                                ),
                                required=True,
                            ),
                            "firing": DictElement(
                                parameter_form=ServiceState(
                                    title=Title("firing"), prefill=DefaultValue(0)
                                ),
                                required=True,
                            ),
                            "none": DictElement(
                                parameter_form=ServiceState(
                                    title=Title("none"), prefill=DefaultValue(2)
                                ),
                                required=True,
                            ),
                            "not_applicable": DictElement(
                                parameter_form=ServiceState(
                                    title=Title("n/a"), prefill=DefaultValue(2)
                                ),
                                required=True,
                            ),
                        },
                        migrate=migrate_non_identifier_key,
                    ),
                    required=True,
                ),
            },
        ),
        title=Title("Remap alert rule states"),
        help_text=Help("Configure the monitoring state for Alertmanager rules."),
        custom_validate=(validators.LengthInRange(min_value=1),),
    )

def form_severity_remapping():
    return Dictionary(
        elements={
            "info": DictElement(
                parameter_form=String(
                    title=Title("Information"), prefill=DefaultValue("info"),
                ),
                required=True,
            ),
            "warning": DictElement(
                parameter_form=String(
                    title=Title("Warning"), prefill=DefaultValue("warning"),
                ),
                required=True,
            ),
            "alert": DictElement(
                parameter_form=String(
                    title=Title("Alert"), prefill=DefaultValue("alert"),
                ),
                required=True,
            ),
            "critical": DictElement(
                parameter_form=String(
                    title=Title("Critical"), prefill=DefaultValue("critical"),
                ),
                required=True,
            ),
            "error": DictElement(
                parameter_form=String(
                    title=Title("Error"), prefill=DefaultValue("error"),
                ),
                required=True,
            ),
            "none": DictElement(
                parameter_form=String(
                    title=Title("None"), prefill=DefaultValue("none"),
                ),
                required=True,
            ),
            "na": DictElement(
                parameter_form=String(
                    title=Title("N/A"), prefill=DefaultValue("not_applicable"),
                ),
                required=True,
            ),
        },
        title=Title("Remap severity names"),
        help_text=Help("Configure the Severity State Name for Alertmanager Events."),
        custom_validate=(validators.LengthInRange(min_value=1),),
    )

def form_severity_state():
    return Dictionary(
        elements={
            "sev_state": DictElement(
                parameter_form=BooleanChoice(label=Label("Activate")),
                required=True,
            ),
        },
        title=Title("Use the severity states to remap alerts."),
        help_text=Help("Severity levels map firing rules automatically to the configured Severity."),

    )

def _check_parameters_form_alertmanager():
    return Dictionary(
        title=Title("Alertmanager rule state"),
        elements={
            "alert_remapping": DictElement(parameter_form=form_alert_remapping()),
            "severity_remapping": DictElement(parameter_form=form_severity_remapping()),
            "severity_state": DictElement(parameter_form=form_severity_state()),
        },
    )


rule_spec_alertmanager_rule_state = CheckParameters(
    name="alertmanager_rule_state_custom",
    topic=Topic.APPLICATIONS,
    parameter_form=_check_parameters_form_alertmanager,
    title=Title("Alertmanager rule states (extended)"),
    condition=HostAndItemCondition(
        item_title=Title("Name of Alert rules/Alert rule groups"),
    ),
)

rule_spec_alertmanager_rule_state_summary = CheckParameters(
    name="alertmanager_rule_state_summary_custom",
    topic=Topic.APPLICATIONS,
    parameter_form=_check_parameters_form_alertmanager,
    title=Title("Alertmanager rule states (summary, extended)"),
    condition=HostCondition(),
)
