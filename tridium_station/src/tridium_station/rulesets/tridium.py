#!/usr/bin/env python3
# WATO rulesets for the Tridium Niagara Station checks (cmk.rulesets.v1)

from cmk.rulesets.v1 import Help, Label, Title
from cmk.rulesets.v1.form_specs import (
    BooleanChoice,
    DefaultValue,
    DictElement,
    Dictionary,
    Float,
    LevelDirection,
    List,
    SimpleLevels,
    String,
)
from cmk.rulesets.v1.rule_specs import (
    CheckParameters,
    HostAndItemCondition,
    HostCondition,
    Topic,
)


def _form_tridium():
    return Dictionary(
        elements={
            "levels": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Check levels"),
                    form_spec_template=Float(unit_symbol="Units"),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=DefaultValue((5.0, 8.0)),
                ),
            ),
            "allowed_strings": DictElement(
                parameter_form=List(
                    title=Title("Allow the following strings in state"),
                    element_template=String(),
                ),
            ),
            "use_discovery": DictElement(
                parameter_form=BooleanChoice(
                    title=Title("Monitor discovery state"),
                    label=Label("Check for state at time of discovery"),
                    help_text=Help(
                        "This overwrites the 'Allow the following strings in state' rule."
                    ),
                ),
            ),
            "forced_strings": DictElement(
                parameter_form=List(
                    title=Title("Force alarm on following states"),
                    help_text=Help(
                        "Makes only sense in combination with 'Monitor discovery state'."
                    ),
                    element_template=String(),
                ),
            ),
        },
    )


rule_spec_tridium = CheckParameters(
    name="tridium",
    topic=Topic.ENVIRONMENTAL,
    parameter_form=_form_tridium,
    title=Title("Tridium Device"),
    condition=HostAndItemCondition(item_title=Title("Sensor name")),
)


def _form_tridium_special():
    return Dictionary(
        elements={
            "rule": DictElement(
                parameter_form=Dictionary(
                    title=Title("Use rule-based state"),
                    elements={
                        "if_state": DictElement(
                            parameter_form=String(title=Title("This state is allowed")),
                            required=True,
                        ),
                        "if_field": DictElement(
                            parameter_form=String(title=Title("If this field")),
                            required=True,
                        ),
                        "if_field_state": DictElement(
                            parameter_form=String(title=Title("has this state")),
                            required=True,
                        ),
                        "else_state": DictElement(
                            parameter_form=String(
                                title=Title("Otherwise require this state")
                            ),
                            required=True,
                        ),
                    },
                ),
            ),
            "states": DictElement(
                parameter_form=List(
                    title=Title("Allow the following strings in state"),
                    element_template=String(),
                ),
            ),
        },
    )


rule_spec_tridium_special = CheckParameters(
    name="tridium_special",
    topic=Topic.ENVIRONMENTAL,
    parameter_form=_form_tridium_special,
    title=Title("Tridium Special"),
    condition=HostAndItemCondition(item_title=Title("Sensor name")),
)


def _form_tridium_fuel():
    return Dictionary(
        elements={
            "levels": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Check levels"),
                    form_spec_template=Float(unit_symbol="Ltr"),
                    level_direction=LevelDirection.LOWER,
                    prefill_fixed_levels=DefaultValue((8.0, 5.0)),
                ),
            ),
        },
    )


rule_spec_tridium_fuel = CheckParameters(
    name="tridium_fuel",
    topic=Topic.ENVIRONMENTAL,
    parameter_form=_form_tridium_fuel,
    title=Title("Tridium Fuel"),
    condition=HostCondition(),
)
