#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.rulesets.v1 import (
        Title,
)

from cmk.rulesets.v1.form_specs import (
        Dictionary,
        DictElement,
        SimpleLevels,
        Integer,
        LevelDirection,
        InputHint,
)

from cmk.rulesets.v1.rule_specs import (
        CheckParameters,
        HostCondition,
        Topic,
)


def as400_tcp_connections():
    return Dictionary(
        elements={
            "connection_levels": DictElement(
                parameter_form=SimpleLevels[int](
                    title=Title("Connections"),
                    form_spec_template=Integer(unit_symbol="Connections"),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=InputHint(value=(900000, 950000)),
                )
            ),
        }
    )


rule_spec_as400_tcp_connections = CheckParameters(
    name="as400_tcp_connections",
    topic=Topic.APPLICATIONS,
    condition=HostCondition(),
    parameter_form=as400_tcp_connections,
    title=Title("AS400 TCP Connections"),
)
