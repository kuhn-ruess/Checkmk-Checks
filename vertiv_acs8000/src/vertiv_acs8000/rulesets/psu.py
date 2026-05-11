#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    ServiceState,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostCondition, Topic


def _parameter_form_vertiv_acs8000_psu():
    return Dictionary(
        title=Title("Vertiv ACS power supply"),
        help_text=Help(
            "Map the PowerSupplyState values reported by acsPowerSupplyStatePw1/Pw2 "
            "(.1.3.6.1.4.1.10418.26.2.1.8.{2,3}.0) to a Checkmk service state. "
            "ACS8000-MIB defines 1=statePowerOn, 2=statePowerOff, 9999=powerNotInstalled."
        ),
        elements={
            "state_mapping": DictElement(
                parameter_form=Dictionary(
                    title=Title("Monitoring state per raw value"),
                    elements={
                        "value_1": DictElement(
                            parameter_form=ServiceState(
                                title=Title("Value 1 (statePowerOn)"),
                                prefill=DefaultValue(0),
                            ),
                        ),
                        "value_2": DictElement(
                            parameter_form=ServiceState(
                                title=Title("Value 2 (statePowerOff)"),
                                prefill=DefaultValue(2),
                            ),
                        ),
                        "value_9999": DictElement(
                            parameter_form=ServiceState(
                                title=Title("Value 9999 (powerNotInstalled)"),
                                prefill=DefaultValue(1),
                            ),
                        ),
                    },
                ),
            ),
        },
    )


rule_spec_vertiv_acs8000_psu = CheckParameters(
    name="vertiv_acs8000_psu",
    topic=Topic.ENVIRONMENTAL,
    condition=HostCondition(),
    parameter_form=_parameter_form_vertiv_acs8000_psu,
    title=Title("Vertiv ACS power supply"),
)
