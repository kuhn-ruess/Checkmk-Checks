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
    MultipleChoice,
    MultipleChoiceElement,
)
from cmk.rulesets.v1.form_specs.validators import LengthInRange
from cmk.rulesets.v1.rule_specs import (
    DiscoveryParameters,
    Topic,
)


def _valuespec_discovery_rule_lnx_sensors():
    return Dictionary(
        elements={
            "filters": DictElement(
                parameter_form = MultipleChoice(
                    title=Title("Sensors to discover"),
                    help_text = Help("Which items to discovery."),
                    elements = [
                        MultipleChoiceElement(
                            name="cpu",
                            title=Title("CPU"),
                        ),
                    ],
                ),
                required = True,
            ),
        },
    )


rule_spec_discover_lnx_sensors = DiscoveryParameters(
    title = Title("Sensors discovery"),
    name = "discover_lnx_sensors",
    topic = Topic.GENERAL,
    parameter_form = _valuespec_discovery_rule_lnx_sensors,
)
