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
    Float,
    InputHint,
    Integer,
    LevelDirection,
    SimpleLevels,
    SingleChoice,
    SingleChoiceElement,
)
from cmk.rulesets.v1.rule_specs import (
    CheckParameters,
    HostAndItemCondition,
    Topic,
)


def _valuespec_mysql_status():
    return Dictionary(
        title = Title("Settings for MySQL status check"),
        elements = {
            "levels": DictElement(
                parameter_form = SimpleLevels(
                    title = Title("Rate/Unit levels"),
                    level_direction = LevelDirection.UPPER,
                    form_spec_template = Integer(),
                    prefill_fixed_levels = InputHint((5, 8)),
                ),
            ),
            "target_state": DictElement(
                parameter_form = SingleChoice(
                    title = Title("Target state"),
                    elements = [
                        SingleChoiceElement(
                            title=Title("ON is OK"),
                            name="on"
                        ),
                        SingleChoiceElement(
                            title=Title("OFF is OK"),
                            name="off"
                        ),
                    ],
                ),
            ),
        },
    )


rule_spec_mysql_status = CheckParameters(
    title = Title("Settings for MySQL status check"),
    name = "mysql_status",
    condition = HostAndItemCondition(item_title = Title("Variable name")),
    topic = Topic.APPLICATIONS,
    parameter_form = _valuespec_mysql_status,
)


def _valuespec_mysql_innodb_buffer_pool_utilization():
    return Dictionary(
        title = Title("Settings for MySQL InnoDB buffer pool utilization check"),
        help_text = Help(
            "The InnoDB buffer pool utilization is calculated as "
            "(pages_total - pages_free) / pages_total * 100. "
            "Note that high utilization (>90%) is normal and desirable for production "
            "databases — a full buffer pool means MySQL is caching data effectively. "
            "Only alert if the pool is persistently at 100% with no free pages, "
            "which may indicate the buffer pool size needs to be increased."
        ),
        elements = {
            "levels": DictElement(
                parameter_form = SimpleLevels(
                    title = Title("Upper levels for buffer pool utilization (%)"),
                    level_direction = LevelDirection.UPPER,
                    form_spec_template = Float(unit_symbol="%"),
                    prefill_fixed_levels = InputHint((95.0, 99.0)),
                ),
            ),
        },
    )


rule_spec_mysql_innodb_buffer_pool_utilization = CheckParameters(
    title = Title("MySQL InnoDB buffer pool utilization"),
    name = "mysql_innodb_buffer_pool_utilization",
    condition = HostAndItemCondition(item_title = Title("Instance name")),
    topic = Topic.APPLICATIONS,
    parameter_form = _valuespec_mysql_innodb_buffer_pool_utilization,
)
