#!/usr/bin/env python3

"""
Cisco Portsecurity Check Parameters Ruleset
"""

from cmk.rulesets.v1 import Title, Help
from cmk.rulesets.v1.form_specs import (
    Dictionary,
    DictElement,
    List,
    String,
)

from cmk.rulesets.v1.rule_specs import (
    CheckParameters,
    Topic,
    HostCondition,
)


def _parameter_valuespec_cisco_portsec():
    """
    Parameter form specification for Cisco Portsecurity Check
    """
    return Dictionary(
        title=Title("Cisco Portsecurity Exceptions"),
        help_text=Help("Configure exceptions for Cisco Portsecurity monitoring"),
        elements={
            "exceptions": DictElement(
                parameter_form=List(
                    element_template=String(),
                    title=Title("Do not check the following Interfaces"),
                    help_text=Help("List of interface names or aliases to exclude. Alias names also match with startswith."),
                ),
            ),
        },
    )


rule_spec_cisco_portsec = CheckParameters(
    name="cisco_portsec",
    topic=Topic.NETWORKING,
    parameter_form=_parameter_valuespec_cisco_portsec,
    title=Title("Cisco Portsecurity Status"),
    condition=HostCondition(),
)