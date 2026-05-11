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
    LevelDirection,
    SIMagnitude,
    ServiceState,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _parameter_form_vertiv_acs8000_serial_port():
    rate_levels = SimpleLevels(
        title=Title("Upper levels for byte rate"),
        level_direction=LevelDirection.UPPER,
        form_spec_template=DataSize(displayed_magnitudes=[SIMagnitude.BYTE, SIMagnitude.KILO, SIMagnitude.MEGA]),
        prefill_fixed_levels=DefaultValue((1_000_000, 10_000_000)),
    )

    return Dictionary(
        title=Title("Vertiv ACS serial port"),
        help_text=Help("Configure rate thresholds and connection-state mappings for serial ports on a Vertiv Avocent ACS 8000."),
        elements={
            "tx_bytes_rate": DictElement(parameter_form=rate_levels),
            "rx_bytes_rate": DictElement(parameter_form=rate_levels),
            "state_mapping": DictElement(
                parameter_form=Dictionary(
                    title=Title("Monitoring state per connection-state value"),
                    help_text=Help(
                        "Override how the integer values reported in column 23 of acsSerialPortTable "
                        "are mapped to a Checkmk service state."
                    ),
                    elements={
                        "value_1": DictElement(
                            parameter_form=ServiceState(
                                title=Title("Value 1 (active)"),
                                prefill=DefaultValue(0),
                            ),
                        ),
                        "value_2": DictElement(
                            parameter_form=ServiceState(
                                title=Title("Value 2 (idle)"),
                                prefill=DefaultValue(0),
                            ),
                        ),
                    },
                ),
            ),
        },
    )


rule_spec_vertiv_acs8000_serial_port = CheckParameters(
    name="vertiv_acs8000_serial_port",
    topic=Topic.NETWORKING,
    condition=HostAndItemCondition(item_title=Title("Serial port")),
    parameter_form=_parameter_form_vertiv_acs8000_serial_port,
    title=Title("Vertiv ACS serial port"),
)
