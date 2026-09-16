#!/usr/bin/env python3
"""
IBM TS4300 - Cleaning cartridge check ruleset

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    Integer,
    LevelDirection,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostCondition, Topic


def _parameter_form():
    return Dictionary(
        title=Title("IBM TS4300 cleaning cartridges"),
        elements={
            "levels_cartridges": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Lower levels on the available cleaning cartridges"),
                    help_text=Help(
                        "Number of cartridges in the library whose barcode marks them "
                        "as cleaning media. A library without a cleaning cartridge "
                        "cannot answer a cleaning request of its drives."
                    ),
                    level_direction=LevelDirection.LOWER,
                    form_spec_template=Integer(),
                    prefill_fixed_levels=DefaultValue((1, 1)),
                ),
                required=True,
            ),
        },
    )


rule_spec_ibm_ts4300_cleaning = CheckParameters(
    name="ibm_ts4300_cleaning",
    topic=Topic.STORAGE,
    parameter_form=_parameter_form,
    title=Title("IBM TS4300 cleaning cartridges"),
    condition=HostCondition(),
)
