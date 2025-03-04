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
    MatchingScope,
    RegularExpression,
)
from cmk.rulesets.v1.form_specs.validators import LengthInRange
from cmk.rulesets.v1.rule_specs import (
    DiscoveryParameters,
    Topic,
)


def _valuespec_discovery_rule_lnx_sensors():
    return Dictionary(
        elements={
            "cpu_filters": DictElement(
                parameter_form = List(
                    title=Title("CPU names"),
                    element_template = Dictionary(
                        elements = {
                            "name": DictElement(
                                 parameter_form = RegularExpression(
                                     title = Title("RegEx name of CPU"),
                                     help_text = Help("Service name like Core0, Core(0-4), ..."),
                                     predefined_help_text=MatchingScope.INFIX,
                                     custom_validate=(LengthInRange(min_value=1),),
                                 ),
                                 required = True,
                            ),
                        },
                    ),
                ),
            ),
        },
    )


rule_spec_discover_lnx_sensors = DiscoveryParameters(
    title = Title("Sensors discovery"),
    name = "discover_lnx_sensors",
    topic = Topic.GENERAL,
    parameter_form = _valuespec_discovery_rule_lnx_sensors,
)
