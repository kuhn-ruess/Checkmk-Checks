#!/usr/bin/python
"""
AS 400 Checks
Bastian Kuhn, bastian.kuhn@kuhn-ruess.de
https://kuhn-ruess.de Checkmk Consulting and Development
"""
from cmk.rulesets.v1 import (
        Title,
)

from cmk.rulesets.v1.form_sepcs import (
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

def _parameter_as400_jobs() -> Dictionary:
    return Dictionary(
            elements={
                "jobs_levels": DictElement(
                    parameter_form=SimpleLevels[int](
                        title=Title("Job"),
                        form_spec_template=Integer(unit_symbol="Jobs"),
                        level_direction=LevelDirection.UPPER,
                        prefill_fixed_levels=InputHint(value=(0, 0)),
                    )
                ),
            }
        )

rule_spec_as400_jobs = CheckParameters(
    name="as400_jobs",
    topic=Topic.APPLICATIONS,
    condition=HostCondition(),
    parameter_form=_parameter_as400_jobs,
    title=Title("AS400 Jobs"),
)

def _parameter_as400_users():
    return Dictionary(
            elements={
                "user_levels": DictElement(
                    parameter_form=SimpleLevels[int](
                        title=Title("Users"),
                        form_spec_template=Integer(unit_symbol="Users"),
                        level_direction=LevelDirection.UPPER,
                        prefill_fixed_levels=InputHint(value=(0, 0)),
                    )
                ),
            }
        )

rule_spec_as400_users = CheckParameters(
    name="as400_users",
    topic=Topic.APPLICATIONS,
    condition=HostCondition(),
    parameter_form=_parameter_as400_users,
    title=Title("AS400 Users"),
)

def _parameter_as400_tcp_connections():
    return Dictionary(
            elements={
                "connection_levels": DictElement(
                    parameter_form=SimpleLevels[int](
                        title=Title("Connections"),
                        form_spec_template=Integer(unit_symbol="Connections"),
                        level_direction=LevelDirection.UPPER,
                        prefill_fixed_levels=InputHint(value=(0, 0)),
                    )
                ),
            }
        )

rule_spec_as400_connections = CheckParameters(
    name="as400_tcp_connections",
    topic=Topic.APPLICATIONS,
    condition=HostCondition(),
    parameter_form=_parameter_as400_tcp_connections,
    title=Title("AS400 TCP Connections"),
)
