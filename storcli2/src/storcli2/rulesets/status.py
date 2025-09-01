#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    Dictionary,
    DictElement,
    List,
    String,
)
from cmk.rulesets.v1.form_specs.validators import LengthInRange
from cmk.rulesets.v1.rule_specs import (
    DiscoveryParameters,
    Topic,
)


def _valuespec_discovery_rule_storcli2_status():
    return Dictionary(
        elements={
            "filters": DictElement(
                parameter_form = List(
                    title=Title("Entries to ignore"),
                    help_text = Help("Which entries to ignore during discovery. Also wildcard (*) is supported at end of name."),
                    element_template=String(custom_validate = (LengthInRange(min_value=1),),),
                ),
                required = True,
            ),
        },
    )   


rule_spec_discover_storcli2_status = DiscoveryParameters(
    title = Title("StorCli2 Status discovery"),
    name = "discover_storcli2_status",
    topic = Topic.GENERAL,
    parameter_form = _valuespec_discovery_rule_storcli2_status,
)
