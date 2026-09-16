#!/usr/bin/env python3
"""
IBM TS4300 - Tape drive check ruleset

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    LevelDirection,
    ServiceState,
    SimpleLevels,
    TimeMagnitude,
    TimeSpan,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _parameter_form():
    return Dictionary(
        title=Title("IBM TS4300 tape drives"),
        elements={
            "needs_cleaning": DictElement(
                parameter_form=ServiceState(
                    title=Title("State when the drive requests cleaning"),
                    help_text=Help(
                        "The drive raises this flag itself. As long as a cleaning "
                        "cartridge is available and automatic cleaning is enabled, "
                        "the library clears the flag on its own."
                    ),
                    prefill=DefaultValue(ServiceState.WARN),
                ),
                required=True,
            ),
            "levels_operating_time": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Levels on the total operating time"),
                    help_text=Help(
                        "Total power-on time the drive reports over its whole life. "
                        "Useful to plan the replacement of drives before they wear out."
                    ),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=TimeSpan(
                        displayed_magnitudes=[TimeMagnitude.DAY, TimeMagnitude.HOUR],
                    ),
                    prefill_fixed_levels=DefaultValue((40000.0 * 3600, 50000.0 * 3600)),
                ),
                required=False,
            ),
        },
    )


rule_spec_ibm_ts4300_drives = CheckParameters(
    name="ibm_ts4300_drives",
    topic=Topic.STORAGE,
    parameter_form=_parameter_form,
    title=Title("IBM TS4300 tape drives"),
    condition=HostAndItemCondition(item_title=Title("Drive")),
)
