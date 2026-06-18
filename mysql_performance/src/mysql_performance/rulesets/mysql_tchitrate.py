#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
# Copyright Bastian Kuhn 2018  mail@bastian-kuhn.de
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    LevelDirection,
    Percentage,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _parameter_form_mysql_tchitrate() -> Dictionary:
    return Dictionary(
        elements={
            "levels": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Levels on MySQL thread cache hitrate"),
                    help_text=Help(
                        "Upper levels on the MySQL thread cache hitrate "
                        "(threads created per connection, in percent)."
                    ),
                    form_spec_template=Percentage(),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=DefaultValue((80.0, 90.0)),
                ),
            ),
        },
    )


rule_spec_mysql_tchitrate = CheckParameters(
    name="mysql_tchitrate",
    title=Title("MySQL Thread Cache Hitrate"),
    topic=Topic.APPLICATIONS,
    parameter_form=_parameter_form_mysql_tchitrate,
    condition=HostAndItemCondition(item_title=Title("MySQL Instance")),
)
