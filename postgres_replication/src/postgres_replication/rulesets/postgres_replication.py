#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DataSize,
    DefaultValue,
    DictElement,
    Dictionary,
    IECMagnitude,
    LevelDirection,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _parameter_form_postgres_replication() -> Dictionary:
    return Dictionary(
        help_text=Help(
            "Upper levels for the replication lag (in bytes) of a PostgreSQL "
            "replication slot."
        ),
        elements={
            "levels": DictElement(
                required=True,
                parameter_form=SimpleLevels(
                    title=Title("Max Size"),
                    form_spec_template=DataSize(
                        displayed_magnitudes=[
                            IECMagnitude.BYTE,
                            IECMagnitude.KIBI,
                            IECMagnitude.MEBI,
                            IECMagnitude.GIBI,
                        ],
                    ),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=DefaultValue((31457280, 62914560)),
                ),
            ),
        },
    )


rule_spec_postgres_replication = CheckParameters(
    name="postgres_replication",
    title=Title("PostgreSQL Replication"),
    topic=Topic.APPLICATIONS,
    parameter_form=_parameter_form_postgres_replication,
    condition=HostAndItemCondition(item_title=Title("Slot Name")),
)
