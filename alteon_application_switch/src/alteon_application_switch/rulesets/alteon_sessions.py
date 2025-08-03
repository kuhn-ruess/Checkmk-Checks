#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    String,
    Float,
    LevelDirection,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _parameter_valuespec_alteon_sessions():
    return Dictionary(
        elements={
            "alteon_session_tresholds": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Thresholds (warn/crit) for Alteon Sessions per SP core"),
                    help_text=Help("The provided thresholds are used for Averages of 1, 4 and 64 seconds. The service is Warning/Critical if one of these values exceeds the threshold"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Float(unit_symbol="%"),
                    prefill_fixed_levels=DefaultValue((80.0, 90.0)),
                ),
                required=False,
            ),
            "alteon_session_ssl_tresholds": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Thresholds (warn/crit) for Alteon SSL Sessions"),
                    help_text=Help("The provided thresholds are only used for Current SSL Sessions. The service is Warning/Critical if this value exceeds the threshold"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Float(unit_symbol="%"),
                    prefill_fixed_levels=DefaultValue((80.0, 90.0)),
                ),
                required=False,
            ),
            "alteon_slb_sessions_tresholds": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Thresholds (warn/crit) for Alteon SLB Sessions"),
                    help_text=Help("The provided thresholds are used for all Performance Values of SLB Sessions. The service is Warning/Critical if one of this values exceeds the threshold"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Float(unit_symbol="%"),
                    prefill_fixed_levels=DefaultValue((80.0, 90.0)),
                ),
                required=False,
            ),
        }
    )


rule_spec_alteon_sessions = CheckParameters(
    name="alteon_sessions",
    topic=Topic.APPLICATIONS,
    condition=HostAndItemCondition(
        item_title=Title("Core"),
        item_form=String(),
    ),
    parameter_form=_parameter_valuespec_alteon_sessions,
    title=Title("Alteon Sessions"),
)


rule_spec_alteon_sessions = CheckParameters(
    name="alteon_sessions",
    topic=Topic.APPLICATIONS,
    condition=HostAndItemCondition(
        item_title=Title("Core"),
        item_form=String(),
    ),
    parameter_form=_parameter_valuespec_alteon_sessions,
    title=Title("Alteon Sessions"),
)
