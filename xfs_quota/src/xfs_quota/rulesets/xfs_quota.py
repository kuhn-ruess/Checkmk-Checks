#!/usr/bin/env python3
"""
XFS project quotas: check parameters

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    CascadingSingleChoice,
    CascadingSingleChoiceElement,
    DataSize,
    DefaultValue,
    DictElement,
    Dictionary,
    Float,
    IECMagnitude,
    Integer,
    LevelDirection,
    Percentage,
    ServiceState,
    SimpleLevels,
    SingleChoice,
    SingleChoiceElement,
    TimeMagnitude,
    TimeSpan,
)
from cmk.rulesets.v1.form_specs.validators import NumberInRange
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic

SIZES = (IECMagnitude.KIBI, IECMagnitude.MEBI, IECMagnitude.GIBI, IECMagnitude.TEBI)


def _space_levels() -> CascadingSingleChoice:
    return CascadingSingleChoice(
        title=Title("Levels for used or free space"),
        help_text=Help(
            "Levels relative to the quota limit (see <i>Limit used as quota size</i>), "
            "like the levels of the filesystem check. Percentage levels can be adjusted "
            "by the magic factor."
        ),
        elements=(
            CascadingSingleChoiceElement(
                name="used_percent",
                title=Title("Percentage of used space"),
                parameter_form=SimpleLevels(
                    form_spec_template=Percentage(),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=DefaultValue((80.0, 90.0)),
                ),
            ),
            CascadingSingleChoiceElement(
                name="used_absolute",
                title=Title("Absolute used space"),
                parameter_form=SimpleLevels(
                    form_spec_template=DataSize(displayed_magnitudes=SIZES),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=DefaultValue((800 * 1024**2, 900 * 1024**2)),
                ),
            ),
            CascadingSingleChoiceElement(
                name="free_percent",
                title=Title("Percentage of free space"),
                parameter_form=SimpleLevels(
                    form_spec_template=Percentage(),
                    level_direction=LevelDirection.LOWER,
                    prefill_fixed_levels=DefaultValue((20.0, 10.0)),
                ),
            ),
            CascadingSingleChoiceElement(
                name="free_absolute",
                title=Title("Absolute free space"),
                parameter_form=SimpleLevels(
                    form_spec_template=DataSize(displayed_magnitudes=SIZES),
                    level_direction=LevelDirection.LOWER,
                    prefill_fixed_levels=DefaultValue((200 * 1024**2, 100 * 1024**2)),
                ),
            ),
        ),
        prefill=DefaultValue("used_percent"),
    )


def _magic() -> Dictionary:
    return Dictionary(
        title=Title("Magic factor (automatic level adaptation for large quotas)"),
        help_text=Help(
            "Adjusts percentage levels to the size of the quota, the same way as the "
            "filesystem check does: quotas larger than the reference size get more "
            "lenient levels, smaller ones stricter levels. A factor of 1.0 disables "
            "the adaptation. Absolute levels are not changed."
        ),
        elements={
            "factor": DictElement(
                required=True,
                parameter_form=Float(
                    title=Title("Magic factor"),
                    custom_validate=(NumberInRange(min_value=0.1, max_value=1.0),),
                    prefill=DefaultValue(0.8),
                ),
            ),
            "normsize": DictElement(
                required=True,
                parameter_form=Integer(
                    title=Title("Reference size"),
                    unit_symbol="GiB",
                    custom_validate=(NumberInRange(min_value=1),),
                    prefill=DefaultValue(20),
                ),
            ),
            "minimum_warn": DictElement(
                required=True,
                parameter_form=Percentage(
                    title=Title("Never lower the warning level below"),
                    prefill=DefaultValue(50.0),
                ),
            ),
            "minimum_crit": DictElement(
                required=True,
                parameter_form=Percentage(
                    title=Title("Never lower the critical level below"),
                    prefill=DefaultValue(60.0),
                ),
            ),
        },
    )


def _parameter_form() -> Dictionary:
    return Dictionary(
        help_text=Help(
            "Monitors XFS project (directory) quotas reported by the agent plug-in "
            "<tt>xfs_quota</tt>. Sizes are evaluated in bytes, the agent reports them "
            "in KiB blocks."
        ),
        elements={
            "levels": DictElement(parameter_form=_space_levels()),
            "magic": DictElement(parameter_form=_magic()),
            "limit": DictElement(
                parameter_form=SingleChoice(
                    title=Title("Limit used as quota size"),
                    help_text=Help(
                        "The limit that counts as 100 percent for the space and inode "
                        "levels and the trend. If the selected limit is not set, the other "
                        "one is used. Without any limit only the used space is shown."
                    ),
                    elements=(
                        SingleChoiceElement(name="hard", title=Title("Hard limit")),
                        SingleChoiceElement(name="soft", title=Title("Soft limit")),
                    ),
                    prefill=DefaultValue("hard"),
                ),
            ),
            "state_soft": DictElement(
                parameter_form=ServiceState(
                    title=Title("State if the soft limit is exceeded"),
                    prefill=DefaultValue(ServiceState.WARN),
                ),
            ),
            "state_hard": DictElement(
                parameter_form=ServiceState(
                    title=Title("State if the hard limit is reached"),
                    help_text=Help("No more data can be written to the project then."),
                    prefill=DefaultValue(ServiceState.CRIT),
                ),
            ),
            "inode_levels": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Levels for used inodes"),
                    help_text=Help("Percentage of the inode limit. Only used if an inode limit is set."),
                    form_spec_template=Percentage(),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=DefaultValue((80.0, 90.0)),
                ),
            ),
            "trend_range": DictElement(
                parameter_form=Integer(
                    title=Title("Time range for trend computation"),
                    help_text=Help(
                        "The growth is averaged over this time range. It is the base for "
                        "the trend levels and the time left until the quota is full."
                    ),
                    unit_symbol="hours",
                    custom_validate=(NumberInRange(min_value=1),),
                    prefill=DefaultValue(24),
                ),
            ),
            "trend_bytes": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Levels on trends in bytes per time range"),
                    form_spec_template=DataSize(displayed_magnitudes=SIZES),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=DefaultValue((100 * 1024**2, 200 * 1024**2)),
                ),
            ),
            "trend_perc": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Levels on trends in percent per time range"),
                    form_spec_template=Percentage(),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=DefaultValue((5.0, 10.0)),
                ),
            ),
            "trend_timeleft": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Levels on the time left until the quota is full"),
                    form_spec_template=TimeSpan(
                        displayed_magnitudes=(TimeMagnitude.DAY, TimeMagnitude.HOUR)
                    ),
                    level_direction=LevelDirection.LOWER,
                    prefill_fixed_levels=DefaultValue((7 * 86400.0, 2 * 86400.0)),
                ),
            ),
        },
    )


rule_spec_xfs_quota = CheckParameters(
    name="xfs_quota",
    title=Title("XFS project quotas"),
    topic=Topic.STORAGE,
    parameter_form=_parameter_form,
    condition=HostAndItemCondition(item_title=Title("Project name")),
)
