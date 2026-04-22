"""
ERA vServer check parameters (CPU/Memory/Drive/LAN utilisation thresholds).
"""
from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    Integer,
    LevelDirection,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _percent_levels(title, defaults):
    return SimpleLevels(
        title=Title(title),
        level_direction=LevelDirection.UPPER,
        form_spec_template=Integer(unit_symbol="%"),
        prefill_fixed_levels=DefaultValue(defaults),
    )


def _count_levels(title, defaults):
    return SimpleLevels(
        title=Title(title),
        level_direction=LevelDirection.UPPER,
        form_spec_template=Integer(),
        prefill_fixed_levels=DefaultValue(defaults),
    )


def _parameters():
    return Dictionary(
        title=Title("ERA vServer thresholds"),
        elements={
            "cpu_load":  DictElement(parameter_form=_percent_levels("CPU load",      (80, 90))),
            "memory":    DictElement(parameter_form=_percent_levels("Memory usage",  (80, 90))),
            "drive_c":   DictElement(parameter_form=_percent_levels("Drive C usage", (80, 90))),
            "drive_d":   DictElement(parameter_form=_percent_levels("Drive D usage", (80, 90))),
            "lan1":      DictElement(parameter_form=_percent_levels("LAN1 usage",    (80, 90))),
            "lan2":      DictElement(parameter_form=_percent_levels("LAN2 usage",    (80, 90))),
            "mlat":      DictElement(parameter_form=_count_levels("MLAT target count",   (10000, 20000))),
            "adsb":      DictElement(parameter_form=_count_levels("ADS-B target count",  (10000, 20000))),
        },
    )


rule_spec_era_vserver = CheckParameters(
    name="era_vserver",
    topic=Topic.OPERATING_SYSTEM,
    condition=HostAndItemCondition(item_title=Title("Target Processor index")),
    parameter_form=_parameters,
    title=Title("ERA vServer"),
)
