"""
Rulesets for the Rittal Blue e+ checks.
"""
from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    Float,
    LevelDirection,
    List,
    ServiceState,
    SimpleLevels,
    String,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _status_override() -> Dictionary:
    return Dictionary(
        elements={
            "status": DictElement(
                required=True,
                parameter_form=String(
                    title=Title("Reported status text"),
                    help_text=Help(
                        "Status text as shown by the check, e.g. 'open', "
                        "'warning', 'high warning', 'door open'."
                    ),
                ),
            ),
            "state": DictElement(
                required=True,
                parameter_form=ServiceState(
                    title=Title("Monitoring state"),
                    prefill=DefaultValue(ServiceState.WARN),
                ),
            ),
        },
    )


def _parameters_blue_e():
    return Dictionary(
        title=Title("Rittal Blue e+ unit health"),
        help_text=Help(
            "Override how Rittal CMC III component status codes map to "
            "Checkmk states. Any status not listed keeps the built-in "
            "default (OK/closed/standby/active → OK, warning/high warning/"
            "low warning → WARN, error/alarm/high alarm/low alarm/no power → "
            "CRIT)."
        ),
        elements={
            "status_states": DictElement(
                parameter_form=List(
                    title=Title("Status overrides"),
                    element_template=_status_override(),
                ),
            ),
        },
    )


def _parameters_blue_e_temp():
    return Dictionary(
        title=Title("Rittal Blue e+ temperature"),
        help_text=Help(
            "Upper temperature levels. If not set, the alarm/warning "
            "thresholds configured on the appliance itself are used."
        ),
        elements={
            "levels": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Upper temperature levels"),
                    form_spec_template=Float(unit_symbol="°C"),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=DefaultValue((70.0, 75.0)),
                ),
            ),
        },
    )


rule_spec_rittal_blue_e = CheckParameters(
    name="rittal_blue_e",
    topic=Topic.ENVIRONMENTAL,
    condition=HostAndItemCondition(item_title=Title("Blue e+ unit")),
    parameter_form=_parameters_blue_e,
    title=Title("Rittal Blue e+ unit health"),
)


rule_spec_rittal_blue_e_temp = CheckParameters(
    name="rittal_blue_e_temp",
    topic=Topic.ENVIRONMENTAL,
    condition=HostAndItemCondition(item_title=Title("Blue e+ temperature sensor")),
    parameter_form=_parameters_blue_e_temp,
    title=Title("Rittal Blue e+ temperature"),
)
