#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    Dictionary,
    DictElement,
    Integer,
    LevelDirection,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostCondition, Topic


def _formspec_palo_alto_gp_tunnels():
    return Dictionary(
        title=Title("Palo Alto GlobalProtect Tunnels"),
        help_text=Help(
            "Warn/critical levels for the remaining free GlobalProtect tunnel slots."
        ),
        elements={
            "levels_remaining": DictElement(
                required=True,
                parameter_form=SimpleLevels(
                    title=Title("Remaining free slots"),
                    level_direction=LevelDirection.LOWER,
                    form_spec_template=Integer(),
                    prefill_fixed_levels=DefaultValue((50, 15)),
                ),
            ),
        },
    )


rule_spec_palo_alto_gp_tunnels = CheckParameters(
    name="palo_alto_gp_tunnels",
    topic=Topic.APPLICATIONS,
    condition=HostCondition(),
    parameter_form=_formspec_palo_alto_gp_tunnels,
    title=Title("Palo Alto GlobalProtect tunnels"),
)
