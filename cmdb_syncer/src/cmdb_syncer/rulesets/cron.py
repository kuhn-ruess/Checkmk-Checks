#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import (
    Dictionary,
    DictElement,
    SimpleLevels,
    LevelDirection,
    InputHint,
    TimeSpan,
    TimeMagnitude
)

from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _parameter_form_quobyte_volumes():
    return Dictionary(
        title = Title("Quobyte volume levels"),
        elements = {
            "max_time_since_last_start": DictElement(
                parameter_form = SimpleLevels(
                    title = Title("Time since the job last start"),
                    level_direction = LevelDirection.UPPER,
                    form_spec_template = TimeSpan(
                        displayed_magnitudes=[TimeMagnitude.MINUTE, TimeMagnitude.HOUR],
                    ),
                    prefill_fixed_levels = InputHint((43200, 86400)),
                )
            ),
        },
    )


rule_spec_cmdbsyncer_cron = CheckParameters(
    name = "cmdb_syncer_cron",
    topic = Topic.OPERATING_SYSTEM,
    condition = HostAndItemCondition(item_title = Title("Job name")),
    parameter_form = _parameter_form_quobyte_volumes,
    title = Title("CMDB Syncer Cronjobs"),
)

