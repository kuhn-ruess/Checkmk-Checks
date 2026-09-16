#!/usr/bin/env python3
"""
IBM TS4300 - Media slot check ruleset

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
    Percentage,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _parameter_form():
    return Dictionary(
        title=Title("IBM TS4300 media slots"),
        elements={
            "levels_used": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Levels on the used slots"),
                    help_text=Help(
                        "Share of the media locations of this type that hold a "
                        "cartridge. Storage slots are discovered with levels so a "
                        "library running out of space is noticed early. The I/O "
                        "station is discovered without levels, because a full mail "
                        "slot is a normal state on many sites - set levels here if "
                        "cartridges are not supposed to stay in the I/O station."
                    ),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Percentage(),
                    prefill_fixed_levels=DefaultValue((90.0, 95.0)),
                ),
                required=True,
            ),
        },
    )


rule_spec_ibm_ts4300_slots = CheckParameters(
    name="ibm_ts4300_slots",
    topic=Topic.STORAGE,
    parameter_form=_parameter_form,
    title=Title("IBM TS4300 media slots"),
    condition=HostAndItemCondition(item_title=Title("Slot type")),
)
